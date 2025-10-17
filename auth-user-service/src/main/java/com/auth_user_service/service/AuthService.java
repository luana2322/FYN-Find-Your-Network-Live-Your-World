package com.auth_user_service.service;

import com.auth_user_service.dto.*;

public interface AuthService {
    AuthResponse register(RegisterRequest request);
    AuthResponse login(AuthRequest request);
    AuthResponse refreshToken(RefreshRequest request);
    void logout(String token);
    void forgotPassword(ForgotPasswordRequest request);
    void resetPassword(ResetPasswordRequest request);
    void verifyEmail(VerifyRequest request);
}
