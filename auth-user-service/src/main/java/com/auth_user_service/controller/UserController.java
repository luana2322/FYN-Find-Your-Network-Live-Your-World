package com.auth_user_service.controller;

import com.auth_user_service.dto.profile.ProfileResponse;
import com.auth_user_service.dto.profile.UpdateProfileRequest;
import com.auth_user_service.minio.MinioService;
import com.auth_user_service.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final MinioService minioService;

    @GetMapping("/profile")
    public ProfileResponse getProfile(@AuthenticationPrincipal Long userId){
        return userService.getProfile(userId);
    }

    @PutMapping("/profile")
    public ProfileResponse updateProfile(@AuthenticationPrincipal Long userId,
                                         @RequestBody UpdateProfileRequest request){
        return userService.updateProfile(userId, request);
    }

    @PostMapping("/avatar")
    public void uploadAvatar(@AuthenticationPrincipal Long userId,
                             @RequestParam("file") MultipartFile file){
        String filename = "avatar_" + userId + "_" + file.getOriginalFilename();
        String url = minioService.uploadAvatar(file, filename);
        userService.updateAvatar(userId, url);
    }
}