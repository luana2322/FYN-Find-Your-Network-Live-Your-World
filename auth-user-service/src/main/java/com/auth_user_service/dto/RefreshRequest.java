package com.auth_user_service.dto;

import lombok.Data;

@Data
public class RefreshRequest {
    private String refreshToken;
    private String deviceId;
}