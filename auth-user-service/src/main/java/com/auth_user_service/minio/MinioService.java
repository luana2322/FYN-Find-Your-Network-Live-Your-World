package com.auth_user_service.minio;

import io.minio.BucketExistsArgs;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import lombok.RequiredArgsConstructor;
import lombok.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;

@Service
@RequiredArgsConstructor

public class MinioService {

    @Value("${minio.url}")
    private String minioUrl;

    @Value("${minio.access-key}")
    private String accessKey;

    @Value("${minio.secret-key}")
    private String secretKey;

    @Value("${minio.bucket}")
    private String bucket;

    public String uploadAvatar(MultipartFile file, String filename) {
        try {
            MinioClient minioClient = MinioClient.builder()
                    .endpoint(minioUrl)
                    .credentials(accessKey, secretKey)
                    .build();
            boolean exists = minioClient.bucketExists(BucketExistsArgs.builder().bucket(bucket).build());
            if(!exists){
                minioClient.makeBucket(MakeBucketArgs.builder().bucket(bucket).build());
            }
            try(InputStream is = file.getInputStream()){
                minioClient.putObject(
                        PutObjectArgs.builder()
                                .bucket(bucket)
                                .object(filename)
                                .stream(is, is.available(), -1)
                                .contentType(file.getContentType())
                                .build()
                );
            }
            return minioUrl + "/" + bucket + "/" + filename;
        } catch (Exception e) {
            throw new RuntimeException("Failed to upload avatar", e);
        }
    }
}