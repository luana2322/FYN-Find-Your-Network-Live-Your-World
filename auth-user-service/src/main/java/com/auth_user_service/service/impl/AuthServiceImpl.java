package com.auth_user_service.service.impl;

import com.auth_user_service.dto.*;
import com.auth_user_service.exception.*;
import com.auth_user_service.model.RefreshToken;
import com.auth_user_service.model.User;
import com.auth_user_service.model.VerificationCode;
import com.auth_user_service.repository.RefreshTokenRepository;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.repository.VerificationCodeRepository;
import com.auth_user_service.service.AuthService;
import com.auth_user_service.service.EmailService;
import com.auth_user_service.service.JwtService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Random;

/**
 * Authentication service implementation.
 * Handles user registration, login, logout, token refresh, and password management.
 */

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private static final Logger log = LoggerFactory.getLogger(AuthServiceImpl.class);
    private final UserRepository userRepository;
    private final RefreshTokenRepository refreshTokenRepository;
    private final VerificationCodeRepository verificationCodeRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final EmailService emailService;

    @Value("${app.otp.expiration:300000}")
    private long otpExpiration;

    @Override
    @Transactional
    public AuthResponse register(RegisterRequest request) {
        log.info("Registering new user with email: {}", request.getEmail());

        // Check if user already exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateResourceException("User", "email", request.getEmail());
        }
        if (request.getPhone() != null && !request.getPhone().isBlank()
            && userRepository.existsByPhone(request.getPhone())) {
            throw new DuplicateResourceException("User", "phone", request.getPhone());
        }
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new DuplicateResourceException("User", "username", request.getUsername());
        }

        // Create new user
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .phone(request.getPhone())
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .password(passwordEncoder.encode(request.getPassword()))
                .isActive(true)
                .emailVerified(false)
                .build();

        user = userRepository.save(user);
        log.info("User registered successfully with ID: {}", user.getId());

        // Send verification email if requested
        if (request.isUseOtp()) {
            sendVerificationEmail(user.getEmail());
        }

        // Generate tokens
        UserDetails userDetails = createUserDetails(user);
        String accessToken = jwtService.generateToken(userDetails);
        String refreshToken = jwtService.generateRefreshToken(userDetails);

        // Save refresh token
        saveRefreshToken(user, refreshToken);

        return buildAuthResponse(user, accessToken, refreshToken);
    }

    @Override
    @Transactional
    public AuthResponse login(AuthRequest request) {
        log.info("User login attempt for identifier: {}", request.getIdentifier());

        // Authenticate user
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getIdentifier(),
                        request.getPassword()
                )
        );

        // Get user details (support email or username login)
        User user = userRepository.findByEmail(request.getIdentifier())
                .or(() -> userRepository.findByUsername(request.getIdentifier()))
                .orElseThrow(() -> new ResourceNotFoundException("User", "identifier", request.getIdentifier()));

        if (!user.getIsActive()) {
            throw new UnauthorizedException("Account is deactivated");
        }

        // Generate tokens
        UserDetails userDetails = createUserDetails(user);
        String accessToken = jwtService.generateToken(userDetails);
        String refreshToken = jwtService.generateRefreshToken(userDetails);

        // Save refresh token
        saveRefreshToken(user, refreshToken);

        log.info("User logged in successfully: {}", user.getEmail());
        return buildAuthResponse(user, accessToken, refreshToken);
    }

    @Override
    @Transactional
    public AuthResponse refreshToken(RefreshRequest request) {
        String refreshToken = request.getRefreshToken();
        log.info("Refresh token request received");

        // Validate refresh token format
        if (!jwtService.isTokenValid(refreshToken, null)) {
            throw new InvalidTokenException("Invalid refresh token");
        }

        // Find refresh token in database
        RefreshToken storedToken = refreshTokenRepository.findByToken(refreshToken)
                .orElseThrow(() -> new InvalidTokenException("Refresh token not found"));

        // Check if token is valid (not expired and not revoked)
        if (!storedToken.isValid()) {
            refreshTokenRepository.delete(storedToken);
            throw new InvalidTokenException("Refresh token expired or revoked");
        }

        // Get user
        User user = userRepository.findById(storedToken.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", storedToken.getUserId()));

        // Generate new tokens
        UserDetails userDetails = createUserDetails(user);
        String newAccessToken = jwtService.generateToken(userDetails);
        String newRefreshToken = jwtService.generateRefreshToken(userDetails);

        // Delete old refresh token and save new one
        refreshTokenRepository.delete(storedToken);
        saveRefreshToken(user, newRefreshToken);

        log.info("Tokens refreshed successfully for user: {}", user.getEmail());
        return buildAuthResponse(user, newAccessToken, newRefreshToken);
    }

    @Override
    @Transactional
    public void logout(String token) {
        log.info("User logout request received");

        try {
            // Blacklist the access token
            jwtService.blacklistToken(token);

            // Extract username and revoke all refresh tokens for this user
            String username = jwtService.extractUsername(token);
            User user = userRepository.findByEmail(username)
                    .orElseThrow(() -> new ResourceNotFoundException("User", "email", username));

            // Revoke all refresh tokens for this user
            refreshTokenRepository.findByToken(token).ifPresent(refreshToken -> {
                refreshToken.setRevoked(true);
                refreshTokenRepository.save(refreshToken);
            });

            log.info("User logged out successfully: {}", username);
        } catch (Exception e) {
            log.error("Error during logout: {}", e.getMessage());
            throw new BusinessLogicException("Logout failed", e);
        }
    }

    @Override
    @Transactional
    public void forgotPassword(ForgotPasswordRequest request) {
        log.info("Forgot password request for email: {}", request.getEmail());

        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getEmail()));

        // Generate and save password reset code
        String resetCode = generateVerificationCode();
        VerificationCode verificationCode = VerificationCode.builder()
                .email(user.getEmail())
                .code(resetCode)
                .type(VerificationCode.CodeType.PASSWORD_RESET)
                .expiryDate(Instant.now().plusMillis(otpExpiration))
                .used(false)
                .build();

        verificationCodeRepository.save(verificationCode);

        // Send password reset email
        try {
            emailService.sendPasswordResetEmail(user.getEmail(), resetCode);
            log.info("Password reset email sent to: {}", user.getEmail());
        } catch (Exception e) {
            log.error("Failed to send password reset email: {}", e.getMessage());
            throw new EmailServiceException("Failed to send password reset email", e);
        }
    }

    @Override
    @Transactional
    public void resetPassword(ResetPasswordRequest request) {
        log.info("Password reset request for email: {}", request.getEmail());

        // Find and validate reset code
        VerificationCode verificationCode = verificationCodeRepository
                .findByEmailAndCodeAndType(
                        request.getEmail(),
                        request.getCode(),
                        VerificationCode.CodeType.PASSWORD_RESET
                )
                .orElseThrow(() -> new InvalidTokenException("Invalid or expired reset code"));

        if (!verificationCode.isValid()) {
            throw new InvalidTokenException("Reset code has expired or been used");
        }

        // Update password
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getEmail()));

        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        userRepository.save(user);

        // Mark code as used
        verificationCode.setUsed(true);
        verificationCodeRepository.save(verificationCode);

        log.info("Password reset successfully for user: {}", user.getEmail());
    }

    @Override
    @Transactional
    public void verifyEmail(VerifyRequest request) {
        log.info("Email verification request for email: {}", request.getEmail());

        // Find and validate verification code
        VerificationCode verificationCode = verificationCodeRepository
                .findByEmailAndCodeAndType(
                        request.getEmail(),
                        request.getCode(),
                        VerificationCode.CodeType.EMAIL_VERIFICATION
                )
                .orElseThrow(() -> new InvalidTokenException("Invalid or expired verification code"));

        if (!verificationCode.isValid()) {
            throw new InvalidTokenException("Verification code has expired or been used");
        }

        // Mark email as verified
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getEmail()));

        user.setEmailVerified(true);
        userRepository.save(user);

        // Mark code as used
        verificationCode.setUsed(true);
        verificationCodeRepository.save(verificationCode);

        log.info("Email verified successfully for user: {}", user.getEmail());
    }

    /**
     * Send email verification code
     */
    private void sendVerificationEmail(String email) {
        String code = generateVerificationCode();

        VerificationCode verificationCode = VerificationCode.builder()
                .email(email)
                .code(code)
                .type(VerificationCode.CodeType.EMAIL_VERIFICATION)
                .expiryDate(Instant.now().plusMillis(otpExpiration))
                .used(false)
                .build();

        verificationCodeRepository.save(verificationCode);

        try {
            emailService.sendVerificationEmail(email, code);
            log.info("Verification email sent to: {}", email);
        } catch (Exception e) {
            log.error("Failed to send verification email: {}", e.getMessage());
            throw new EmailServiceException("Failed to send verification email", e);
        }
    }

    /**
     * Create Spring Security UserDetails from User entity
     */
    private UserDetails createUserDetails(User user) {
        return org.springframework.security.core.userdetails.User.builder()
                .username(user.getEmail())
                .password(user.getPassword())
                .authorities("ROLE_USER")
                .accountExpired(false)
                .accountLocked(!user.getIsActive())
                .credentialsExpired(false)
                .disabled(!user.getIsActive())
                .build();
    }

    /**
     * Save refresh token to database
     */
    private void saveRefreshToken(User user, String refreshToken) {
        RefreshToken token = RefreshToken.builder()
                .userId(user.getId())
                .token(refreshToken)
                .expiryDate(Instant.now().plusSeconds(7 * 24 * 60 * 60)) // 7 days
                .revoked(false)
                .build();
        refreshTokenRepository.save(token);
    }

    /**
     * Build authentication response with user data and tokens
     */
    private AuthResponse buildAuthResponse(User user, String accessToken, String refreshToken) {
        return AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .tokenType("Bearer")
                .user(UserResponse.builder()
                        .id(user.getId())
                        .username(user.getUsername())
                        .email(user.getEmail())
                        .phone(user.getPhone())
                        .firstName(user.getFirstName())
                        .lastName(user.getLastName())
                        .avatarUrl(user.getAvatarUrl())
                        .bio(user.getBio())
                        .emailVerified(user.getEmailVerified())
                        .build())
                .build();
    }

    /**
     * Generate 6-digit verification code
     */
    private String generateVerificationCode() {
        Random random = new Random();
        int code = 100000 + random.nextInt(900000);
        return String.valueOf(code);
    }
}
