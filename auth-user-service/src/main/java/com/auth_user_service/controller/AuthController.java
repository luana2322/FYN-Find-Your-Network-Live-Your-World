package com.auth_user_service.controller;

import com.auth_user_service.dto.*;
import com.auth_user_service.service.AuthService;
import com.auth_user_service.util.ResponseUtil;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    @Autowired
    private  AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        try {
            AuthResponse response = authService.register(request);
            return ResponseUtil.success(response, "Registration successful");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody AuthRequest request) {
        try {
            AuthResponse response = authService.login(request);
            return ResponseUtil.success(response, "Login successful");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PostMapping("/refresh")
    public ResponseEntity<?> refreshToken(@Valid @RequestBody RefreshRequest request) {
        try {
            AuthResponse response = authService.refreshToken(request);
            return ResponseUtil.success(response, "Token refreshed successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout(HttpServletRequest request) {
        try {
            String token = extractTokenFromRequest(request);
            authService.logout(token);
            return ResponseUtil.success(null, "Logout successful");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<?> forgotPassword(@Valid @RequestBody ForgotPasswordRequest request) {
        try {
            authService.forgotPassword(request);
            return ResponseUtil.success(null, "Password reset email sent");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PostMapping("/reset-password")
    public ResponseEntity<?> resetPassword(@Valid @RequestBody ResetPasswordRequest request) {
        try {
            authService.resetPassword(request);
            return ResponseUtil.success(null, "Password reset successful");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PostMapping("/verify-email")
    public ResponseEntity<?> verifyEmail(@Valid @RequestBody VerifyRequest request) {
        try {
            authService.verifyEmail(request);
            return ResponseUtil.success(null, "Email verified successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    private String extractTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        throw new RuntimeException("No token found");
    }
}
