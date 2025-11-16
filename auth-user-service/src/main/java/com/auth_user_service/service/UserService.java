package com.auth_user_service.service;

import com.auth_user_service.dto.profile.ProfileResponse;
import com.auth_user_service.dto.profile.UpdateProfileRequest;

public interface UserService {
    ProfileResponse getProfile(Long userId);
    ProfileResponse updateProfile(Long userId, UpdateProfileRequest request);
    void updateAvatar(Long userId, String avatarUrl);
}