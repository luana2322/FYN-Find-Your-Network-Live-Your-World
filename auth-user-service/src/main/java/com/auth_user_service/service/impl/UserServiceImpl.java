package com.auth_user_service.service.impl;

import com.auth_user_service.dto.UpdateProfileRequest;
import com.auth_user_service.dto.UserResponse;
import com.auth_user_service.exception.DuplicateResourceException;
import com.auth_user_service.exception.ResourceNotFoundException;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    @Override
    public UserResponse getCurrentUserProfile(Authentication authentication) {
        String email = authentication.getName();
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));
        
        return convertToUserResponse(user);
    }

    @Override
    @Transactional
    public UserResponse updateProfile(Authentication authentication, UpdateProfileRequest request) {
        String email = authentication.getName();
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

        // Update fields if provided
        if (request.getUsername() != null && !request.getUsername().trim().isEmpty()) {
            user.setUsername(request.getUsername());
        }
        if (request.getBio() != null) {
            user.setBio(request.getBio());
        }
        if (request.getPhone() != null && !request.getPhone().trim().isEmpty()) {
            // Check if phone is already taken by another user
            if (userRepository.existsByPhone(request.getPhone()) && 
                !user.getPhone().equals(request.getPhone())) {
                throw new DuplicateResourceException("User", "phone", request.getPhone());
            }
            user.setPhone(request.getPhone());
        }

        user.setUpdatedAt(Instant.now());
        user = userRepository.save(user);

        return convertToUserResponse(user);
    }

    @Override
    public UserResponse getUserById(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", userId));
        
        return convertToUserResponse(user);
    }

    @Override
    public List<UserResponse> searchUsers(String query, int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        List<User> users = userRepository.search(query);
        
        return users.stream()
                .map(this::convertToUserResponse)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public void deactivateAccount(Authentication authentication) {
        String email = authentication.getName();
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));
        
        user.setIsActive(false);
        user.setUpdatedAt(Instant.now());
        userRepository.save(user);
    }

    private UserResponse convertToUserResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .phone(user.getPhone())
                .avatarUrl(user.getAvatarUrl())
                .bio(user.getBio())
                .build();
    }
}
