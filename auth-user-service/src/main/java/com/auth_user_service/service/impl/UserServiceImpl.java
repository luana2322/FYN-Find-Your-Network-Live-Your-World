package com.auth_user_service.service.impl;

import com.auth_user_service.dto.profile.ProfileResponse;
import com.auth_user_service.dto.profile.UpdateProfileRequest;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    @Override
    public ProfileResponse getProfile(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return mapToProfileResponse(user);
    }

    @Override
    public ProfileResponse updateProfile(Long userId, UpdateProfileRequest request) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        user.setFullName(request.getFullName());
        user.setBio(request.getBio());
        userRepository.save(user);
        return mapToProfileResponse(user);
    }

    @Override
    public void updateAvatar(Long userId, String avatarUrl) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        user.setAvatarUrl(avatarUrl);
        userRepository.save(user);
    }

    private ProfileResponse mapToProfileResponse(User user) {
        ProfileResponse resp = new ProfileResponse();
        resp.setId(user.getId());
        resp.setUsername(user.getUsername());
        resp.setEmail(user.getEmail());
        resp.setPhone(user.getPhone());
        resp.setFullName(user.getFullName());
        resp.setBio(user.getBio());
        resp.setAvatarUrl(user.getAvatarUrl());
        return resp;
    }
}