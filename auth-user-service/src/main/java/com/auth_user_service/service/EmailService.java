package com.auth_user_service.service;

public interface EmailService {
    void sendVerificationEmail(String email, String verificationCode);
    void sendPasswordResetEmail(String email, String resetCode);
}
