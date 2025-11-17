package com.auth_user_service.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

/**
 * Entity for storing blacklisted JWT tokens.
 * Replaces Redis-based token blacklisting with database persistence.
 * Used during logout to invalidate tokens before their natural expiration.
 */
@Entity
@Table(name = "blacklisted_tokens", indexes = {
    @Index(name = "idx_jti", columnList = "jti", unique = true),
    @Index(name = "idx_expiry", columnList = "expiryDate")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BlacklistedToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * JWT ID (jti claim) - unique identifier for the token
     */
    @Column(nullable = false, unique = true, length = 100)
    private String jti;

    /**
     * When the token expires (after this, no need to check blacklist)
     */
    @Column(nullable = false)
    private Instant expiryDate;

    /**
     * When the token was blacklisted
     */
    @Column(nullable = false, updatable = false)
    private Instant blacklistedAt;

    /**
     * Optional: reason for blacklisting
     */
    private String reason;

    @PrePersist
    protected void onCreate() {
        if (blacklistedAt == null) {
            blacklistedAt = Instant.now();
        }
    }

    /**
     * Check if this blacklist entry is still relevant
     * (can be cleaned up if token already expired)
     */
    public boolean isExpired() {
        return Instant.now().isAfter(expiryDate);
    }
}
