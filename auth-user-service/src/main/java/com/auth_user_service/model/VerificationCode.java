package com.auth_user_service.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

/**
 * Entity for storing email verification codes and password reset codes.
 * Replaces Redis-based OTP storage with database persistence.
 */
@Entity
@Table(name = "verification_codes", indexes = {
    @Index(name = "idx_email", columnList = "email"),
    @Index(name = "idx_code", columnList = "code"),
    @Index(name = "idx_expiry", columnList = "expiryDate")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class VerificationCode {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false, length = 10)
    private String code;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private CodeType type;

    @Column(nullable = false)
    private Instant expiryDate;

    @Column(nullable = false)
    private boolean used = false;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    /**
     * Type of verification code
     */
    public enum CodeType {
        EMAIL_VERIFICATION,
        PASSWORD_RESET
    }

    @PrePersist
    protected void onCreate() {
        if (createdAt == null) {
            createdAt = Instant.now();
        }
    }

    /**
     * Check if the verification code has expired
     */
    public boolean isExpired() {
        return Instant.now().isAfter(expiryDate);
    }

    /**
     * Check if the verification code is valid (not expired and not used)
     */
    public boolean isValid() {
        return !used && !isExpired();
    }
}
