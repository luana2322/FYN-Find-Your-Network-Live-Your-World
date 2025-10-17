package com.auth_user_service.service;

import com.auth_user_service.dto.UpdateProfileRequest;
import com.auth_user_service.dto.UserResponse;
import com.auth_user_service.model.User;
import org.springframework.security.core.Authentication;

import java.util.List;

public interface UserService {
    UserResponse getCurrentUserProfile(Authentication authentication);
    UserResponse updateProfile(Authentication authentication, UpdateProfileRequest request);
    UserResponse getUserById(Long userId);
    List<UserResponse> searchUsers(String query, int page, int size);
    void deactivateAccount(Authentication authentication);
}
