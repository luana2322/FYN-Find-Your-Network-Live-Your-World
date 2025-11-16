package com.auth_user_service.service.impl;

import com.auth_user_service.dto.auth.AuthResponse;
import com.auth_user_service.dto.auth.LoginRequest;
import com.auth_user_service.dto.auth.RegisterRequest;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.AuthService;
import com.auth_user_service.util.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public AuthResponse register(RegisterRequest request) {
        User user = User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .phone(request.getPhone())
                .password(passwordEncoder.encode(request.getPassword()))
                .build();
        userRepository.save(user);
        String access = jwtUtil.generateToken(user.getId());
        String refresh = jwtUtil.generateRefreshToken(user.getId());
        return createAuthResponse(user, access, refresh);
    }

    @Override
    public AuthResponse login(LoginRequest request) {
        User user = userRepository.findByUsername(request.getUsernameOrEmailOrPhone())
                .or(() -> userRepository.findByEmail(request.getUsernameOrEmailOrPhone()))
                .or(() -> userRepository.findByPhone(request.getUsernameOrEmailOrPhone()))
                .orElseThrow(() -> new RuntimeException("User not found"));
        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid credentials");
        }
        String access = jwtUtil.generateToken(user.getId());
        String refresh = jwtUtil.generateRefreshToken(user.getId());
        return createAuthResponse(user, access, refresh);
    }

    @Override
    public AuthResponse refreshToken(String refreshToken) {
        Long userId = jwtUtil.validateRefreshToken(refreshToken);
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        String access = jwtUtil.generateToken(user.getId());
        String refresh = jwtUtil.generateRefreshToken(user.getId());
        return createAuthResponse(user, access, refresh);
    }

    private AuthResponse createAuthResponse(User user, String access, String refresh) {
        AuthResponse resp = new AuthResponse();
        resp.setUserId(user.getId());
        resp.setUsername(user.getUsername());
        resp.setAccessToken(access);
        resp.setRefreshToken(refresh);
        return resp;
    }
}