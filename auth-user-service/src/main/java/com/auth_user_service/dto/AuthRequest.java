package com.auth_user_service.dto;

import lombok.Data;

@Data
public class AuthRequest {
    private String identifier; // email or phone
    private String password;
    private String deviceId;
}