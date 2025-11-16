package com.auth_user_service.dto.auth;

import lombok.Data;

@Data
public class AuthResponse {
    private String accessToken;
    private String refreshToken;
    private Long userId;
    private String username;
}