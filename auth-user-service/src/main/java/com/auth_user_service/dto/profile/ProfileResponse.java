package com.auth_user_service.dto.profile;


import lombok.Data;

@Data
public class ProfileResponse {
    private Long id;
    private String username;
    private String email;
    private String phone;
    private String fullName;
    private String bio;
    private String avatarUrl;
}