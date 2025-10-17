package com.auth_user_service.service.impl;

import com.auth_user_service.exception.FileUploadException;
import com.auth_user_service.exception.ResourceNotFoundException;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.StorageService;
import io.minio.BucketExistsArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.RemoveObjectArgs;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.time.Instant;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class StorageServiceImpl implements StorageService {

    private final MinioClient minioClient;
    private final UserRepository userRepository;

    @Value("${minio.bucket.name}")
    private String bucketName;

    @Override
    public String uploadAvatar(String email, MultipartFile file) {
        try {
            // Validate file
            if (file.isEmpty()) {
                throw new FileUploadException("File is empty");
            }

            // Check file type
            String contentType = file.getContentType();
            if (contentType == null || !contentType.startsWith("image/")) {
                throw new FileUploadException("File must be an image");
            }

            // Check file size (max 5MB)
            if (file.getSize() > 5 * 1024 * 1024) {
                throw new FileUploadException("File size must be less than 5MB");
            }

            // Ensure bucket exists
            ensureBucketExists();

            // Generate unique filename
            String fileName = "avatars/" + email + "/" + UUID.randomUUID() + "_" + file.getOriginalFilename();

            // Upload file to MinIO
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucketName)
                            .object(fileName)
                            .stream(file.getInputStream(), file.getSize(), -1)
                            .contentType(contentType)
                            .build()
            );

            // Generate public URL
            String avatarUrl = "/api/files/avatar/" + fileName;

            // Update user's avatar URL in database
            User user = userRepository.findByEmail(email)
                    .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));
            user.setAvatarUrl(avatarUrl);
            user.setUpdatedAt(Instant.now());
            userRepository.save(user);

            log.info("Avatar uploaded successfully for user: {}", email);
            return avatarUrl;

        } catch (Exception e) {
            log.error("Failed to upload avatar for user: {}", email, e);
            throw new FileUploadException("Failed to upload avatar: " + e.getMessage(), e);
        }
    }

    @Override
    public void deleteAvatar(String email) {
        try {
            User user = userRepository.findByEmail(email)
                    .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

            if (user.getAvatarUrl() != null && !user.getAvatarUrl().isEmpty()) {
                // Extract object name from URL
                String objectName = user.getAvatarUrl().replace("/api/files/avatar/", "");
                
                // Delete from MinIO
                minioClient.removeObject(
                        RemoveObjectArgs.builder()
                                .bucket(bucketName)
                                .object(objectName)
                                .build()
                );

                // Update user's avatar URL
                user.setAvatarUrl(null);
                user.setUpdatedAt(Instant.now());
                userRepository.save(user);

                log.info("Avatar deleted successfully for user: {}", email);
            }
        } catch (Exception e) {
            log.error("Failed to delete avatar for user: {}", email, e);
            throw new FileUploadException("Failed to delete avatar: " + e.getMessage(), e);
        }
    }

    @Override
    public String getAvatarUrl(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));
        return user.getAvatarUrl();
    }

    private void ensureBucketExists() {
        try {
            boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucketName).build());
            if (!exists) {
                minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucketName).build());
                log.info("Created bucket: {}", bucketName);
            }
        } catch (Exception e) {
            log.error("Failed to ensure bucket exists: {}", bucketName, e);
            throw new FileUploadException("Failed to create bucket: " + e.getMessage(), e);
        }
    }
}
