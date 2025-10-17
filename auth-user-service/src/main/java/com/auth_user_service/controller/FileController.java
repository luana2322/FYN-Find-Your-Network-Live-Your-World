package com.auth_user_service.controller;

import com.auth_user_service.service.StorageService;
import com.auth_user_service.util.ResponseUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
public class FileController {

    private final StorageService storageService;

    @PostMapping("/upload/avatar")
    public ResponseEntity<?> uploadAvatar(Authentication authentication, 
                                        @RequestParam("file") MultipartFile file) {
        try {
            String email = authentication.getName();
            String avatarUrl = storageService.uploadAvatar(email, file);
            
            Map<String, Object> result = new HashMap<>();
            result.put("avatarUrl", avatarUrl);
            
            return ResponseUtil.success(result, "Avatar uploaded successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @DeleteMapping("/avatar")
    public ResponseEntity<?> deleteAvatar(Authentication authentication) {
        try {
            String email = authentication.getName();
            storageService.deleteAvatar(email);
            return ResponseUtil.success(null, "Avatar deleted successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }
}
