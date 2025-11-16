package com.auth_user_service.dto.profile;


import lombok.Data;

@Data
public class UpdateProfileRequest {
    private String fullName;
    private String bio;
}