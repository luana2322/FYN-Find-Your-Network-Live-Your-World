package com.auth_user_service.dto;

import lombok.Data;

@Data
public class UpdateProfileRequest {
    private String username;
    private String bio;
    private String avatarUrl;
    private String phone;
}