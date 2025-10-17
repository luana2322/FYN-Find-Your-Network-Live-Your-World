package com.auth_user_service.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "refresh_tokens")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RefreshToken {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) 
    private Long id;
    
    @Column(unique = true) 
    private String token;
    
    @Column(name = "user_id")
    private Long userId;
    
    @Column(name = "expiry_date")
    private Instant expiryDate;
    
    private boolean revoked = false;
    private String deviceId;
    private Instant createdAt = Instant.now();
}