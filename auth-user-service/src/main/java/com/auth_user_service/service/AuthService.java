package com.auth_user_service.service;

import com.auth_user_service.dto.auth.AuthResponse;
import com.auth_user_service.dto.auth.LoginRequest;
import com.auth_user_service.dto.auth.RegisterRequest;

public interface AuthService {
    AuthResponse register(RegisterRequest request);
    AuthResponse login(LoginRequest request);
    AuthResponse refreshToken(String refreshToken);
}