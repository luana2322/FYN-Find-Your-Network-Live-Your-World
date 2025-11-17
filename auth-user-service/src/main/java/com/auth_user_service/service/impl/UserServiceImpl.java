package com.auth_user_service.service.impl;

import com.auth_user_service.dto.UpdateProfileRequest;
import com.auth_user_service.dto.UserResponse;
import com.auth_user_service.exception.DuplicateResourceException;
import com.auth_user_service.exception.ResourceNotFoundException;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * User service implementation.
 * Handles user profile management and search functionality.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    @Override
    public UserResponse getCurrentUserProfile(Authentication authentication) {
        String email = authentication.getName();
        log.info("Getting profile for user: {}", email);

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

        return convertToUserResponse(user);
    }

    @Override
    @Transactional
    public UserResponse updateProfile(Authentication authentication, UpdateProfileRequest request) {
        String email = authentication.getName();
        log.info("Updating profile for user: {}", email);

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

        // Update username if provided and different
        if (request.getUsername() != null && !request.getUsername().trim().isEmpty()) {
            if (!user.getUsername().equals(request.getUsername())
                    && userRepository.existsByUsername(request.getUsername())) {
                throw new DuplicateResourceException("User", "username", request.getUsername());
            }
            user.setUsername(request.getUsername());
        }

        // Update first name if provided
        if (request.getFirstName() != null) {
            user.setFirstName(request.getFirstName().trim().isEmpty() ? null : request.getFirstName());
        }

        // Update last name if provided
        if (request.getLastName() != null) {
            user.setLastName(request.getLastName().trim().isEmpty() ? null : request.getLastName());
        }

        // Update bio if provided
        if (request.getBio() != null) {
            user.setBio(request.getBio().trim().isEmpty() ? null : request.getBio());
        }

        // Update phone if provided and different
        if (request.getPhone() != null && !request.getPhone().trim().isEmpty()) {
            if (!request.getPhone().equals(user.getPhone())
                    && userRepository.existsByPhone(request.getPhone())) {
                throw new DuplicateResourceException("User", "phone", request.getPhone());
            }
            user.setPhone(request.getPhone());
        }

        user = userRepository.save(user);
        log.info("Profile updated successfully for user: {}", email);

        return convertToUserResponse(user);
    }

    @Override
    public UserResponse getUserById(Long userId) {
        log.info("Getting user by ID: {}", userId);

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", userId));

        return convertToUserResponse(user);
    }

    @Override
    public List<UserResponse> searchUsers(String query, int page, int size) {
        log.info("Searching users with query: {}, page: {}, size: {}", query, page, size);

        // Validate pagination parameters
        if (page < 0) page = 0;
        if (size < 1 || size > 100) size = 10;

        List<User> users = userRepository.search(query);

        // Manual pagination since repository method returns List
        int start = page * size;
        int end = Math.min(start + size, users.size());

        if (start >= users.size()) {
            return List.of();
        }

        return users.subList(start, end).stream()
                .map(this::convertToUserResponse)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public void deactivateAccount(Authentication authentication) {
        String email = authentication.getName();
        log.info("Deactivating account for user: {}", email);

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

        user.setIsActive(false);
        userRepository.save(user);

        log.info("Account deactivated successfully for user: {}", email);
    }

    /**
     * Convert User entity to UserResponse DTO
     */
    private UserResponse convertToUserResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .phone(user.getPhone())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .avatarUrl(user.getAvatarUrl())
                .bio(user.getBio())
                .emailVerified(user.getEmailVerified())
                .build();
    }
}
