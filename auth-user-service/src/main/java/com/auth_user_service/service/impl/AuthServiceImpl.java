package com.auth_user_service.service.impl;

import com.auth_user_service.dto.*;
import com.auth_user_service.exception.*;
import com.auth_user_service.model.RefreshToken;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.RefreshTokenRepository;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.AuthService;
import com.auth_user_service.service.EmailService;
import com.auth_user_service.service.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserRepository userRepository;
    private final RefreshTokenRepository refreshTokenRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final EmailService emailService;

    @Override
    @Transactional
    public AuthResponse register(RegisterRequest request) {
        // Check if user already exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateResourceException("User", "email", request.getEmail());
        }
        if (request.getPhone() != null && userRepository.existsByPhone(request.getPhone())) {
            throw new DuplicateResourceException("User", "phone", request.getPhone());
        }

        // Create new user
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .phone(request.getPhone())
                .password(passwordEncoder.encode(request.getPassword()))
                .isActive(true)
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();

        user = userRepository.save(user);

        // Send verification email
        if (request.isUseOtp()) {
            String verificationCode = generateVerificationCode();
            emailService.sendVerificationEmail(user.getEmail(), verificationCode);
            // Store verification code in Redis or database
        }

        // Generate tokens
        UserDetails userDetails = createUserDetails(user);
        String accessToken = jwtService.generateToken(userDetails);
        String refreshToken = jwtService.generateRefreshToken(userDetails);

        // Save refresh token
        saveRefreshToken(user, refreshToken);

        return AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .user(UserResponse.builder()
                        .id(user.getId())
                        .username(user.getUsername())
                        .email(user.getEmail())
                        .phone(user.getPhone())
                        .avatarUrl(user.getAvatarUrl())
                        .bio(user.getBio())
                        .build())
                .build();
    }

    @Override
    public AuthResponse login(AuthRequest request) {
        // Authenticate user
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.getIdentifier(),
                        request.getPassword()
                )
        );

        // Get user details
        User user = userRepository.findByEmail(request.getIdentifier())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getIdentifier()));

        if (!user.getIsActive()) {
            throw new UnauthorizedException("Account is deactivated");
        }

        // Generate tokens
        UserDetails userDetails = createUserDetails(user);
        String accessToken = jwtService.generateToken(userDetails);
        String refreshToken = jwtService.generateRefreshToken(userDetails);

        // Save refresh token
        saveRefreshToken(user, refreshToken);

        return AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .user(UserResponse.builder()
                        .id(user.getId())
                        .username(user.getUsername())
                        .email(user.getEmail())
                        .phone(user.getPhone())
                        .avatarUrl(user.getAvatarUrl())
                        .bio(user.getBio())
                        .build())
                .build();
    }

    @Override
    @Transactional
    public AuthResponse refreshToken(RefreshRequest request) {
        String refreshToken = request.getRefreshToken();

        // Validate refresh token
        if (!jwtService.isTokenValid(refreshToken, null)) {
            throw new InvalidTokenException("Invalid refresh token");
        }

        // Find refresh token in database
        RefreshToken storedToken = refreshTokenRepository.findByToken(refreshToken)
                .orElseThrow(() -> new InvalidTokenException("Refresh token not found"));

        if (storedToken.getExpiryDate().isBefore(Instant.now())) {
            refreshTokenRepository.delete(storedToken);
            throw new InvalidTokenException("Refresh token expired");
        }

        // Get user
        User user = userRepository.findById(storedToken.getUserId())
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", storedToken.getUserId()));

        // Generate new tokens
        UserDetails userDetails = createUserDetails(user);
        String newAccessToken = jwtService.generateToken(userDetails);
        String newRefreshToken = jwtService.generateRefreshToken(userDetails);

        // Update refresh token
        refreshTokenRepository.delete(storedToken);
        saveRefreshToken(user, newRefreshToken);

        return AuthResponse.builder()
                .accessToken(newAccessToken)
                .refreshToken(newRefreshToken)
                .user(UserResponse.builder()
                        .id(user.getId())
                        .username(user.getUsername())
                        .email(user.getEmail())
                        .phone(user.getPhone())
                        .avatarUrl(user.getAvatarUrl())
                        .bio(user.getBio())
                        .build())
                .build();
    }

    @Override
    public void logout(String token) {
        jwtService.blacklistToken(token);
    }

    @Override
    public void forgotPassword(ForgotPasswordRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getEmail()));

        String resetCode = generateVerificationCode();
        try {
            emailService.sendPasswordResetEmail(user.getEmail(), resetCode);
        } catch (Exception e) {
            throw new EmailServiceException("Failed to send password reset email", e);
        }
        // Store reset code in Redis or database
    }

    @Override
    public void resetPassword(ResetPasswordRequest request) {
        // Validate reset code
        // Update password
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getEmail()));

        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        user.setUpdatedAt(Instant.now());
        userRepository.save(user);
    }

    @Override
    public void verifyEmail(VerifyRequest request) {
        // Validate verification code
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", request.getEmail()));

        // Mark email as verified
        user.setUpdatedAt(Instant.now());
        userRepository.save(user);
    }

    private UserDetails createUserDetails(User user) {
        return org.springframework.security.core.userdetails.User.builder()
                .username(user.getEmail())
                .password(user.getPassword())
                .authorities(new org.springframework.security.core.authority.SimpleGrantedAuthority("USER"))
                .build();
    }

    private void saveRefreshToken(User user, String refreshToken) {
        RefreshToken token = RefreshToken.builder()
                .userId(user.getId())
                .token(refreshToken)
                .expiryDate(Instant.now().plusSeconds(7 * 24 * 60 * 60)) // 7 days
                .build();
        refreshTokenRepository.save(token);
    }

    private String generateVerificationCode() {
        return String.valueOf(100000 + (int) (Math.random() * 900000)); // 6-digit code
    }
}
