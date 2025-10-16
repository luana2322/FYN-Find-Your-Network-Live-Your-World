package com.auth_user_service.dto;

import lombok.Data;

@Data
public class ForgotPasswordRequest {
    private String identifier; // email
}