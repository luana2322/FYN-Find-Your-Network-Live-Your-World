package com.auth_user_service.controller;

import com.auth_user_service.dto.UpdateProfileRequest;
import com.auth_user_service.dto.UserResponse;
import com.auth_user_service.service.UserService;
import com.auth_user_service.util.ResponseUtil;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    @Autowired
    private UserService userService;

    @GetMapping("/profile")
    public ResponseEntity<?> getCurrentUserProfile(Authentication authentication) {
        try {
            UserResponse user = userService.getCurrentUserProfile(authentication);
            return ResponseUtil.success(user, "Profile retrieved successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @PutMapping("/profile")
    public ResponseEntity<?> updateProfile(Authentication authentication, 
                                          @Valid @RequestBody UpdateProfileRequest request) {
        try {
            UserResponse user = userService.updateProfile(authentication, request);
            return ResponseUtil.success(user, "Profile updated successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @GetMapping("/{userId}")
    public ResponseEntity<?> getUserById(@PathVariable Long userId) {
        try {
            UserResponse user = userService.getUserById(userId);
            return ResponseUtil.success(user, "User retrieved successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @GetMapping("/search")
    public ResponseEntity<?> searchUsers(@RequestParam String q,
                                       @RequestParam(defaultValue = "0") int page,
                                       @RequestParam(defaultValue = "10") int size) {
        try {
            List<UserResponse> users = userService.searchUsers(q, page, size);
            return ResponseUtil.success(users, "Search completed successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @DeleteMapping("/profile")
    public ResponseEntity<?> deactivateAccount(Authentication authentication) {
        try {
            userService.deactivateAccount(authentication);
            return ResponseUtil.success(null, "Account deactivated successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }
}
