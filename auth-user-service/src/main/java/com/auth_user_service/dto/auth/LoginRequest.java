package com.auth_user_service.dto.auth;

import lombok.Data;

@Data
public class LoginRequest {
    private String usernameOrEmailOrPhone;
    private String password;
}