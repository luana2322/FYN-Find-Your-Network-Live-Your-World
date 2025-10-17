package com.auth_user_service.service;

import org.springframework.web.multipart.MultipartFile;

public interface StorageService {
    String uploadAvatar(String email, MultipartFile file);
    void deleteAvatar(String email);
    String getAvatarUrl(String email);
}
