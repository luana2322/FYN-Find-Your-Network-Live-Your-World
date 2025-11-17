package com.auth_user_service.repository;

import com.auth_user_service.model.VerificationCode;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.Optional;

/**
 * Repository for managing verification codes (email verification and password reset).
 */
@Repository
public interface VerificationCodeRepository extends JpaRepository<VerificationCode, Long> {

    /**
     * Find the most recent valid verification code for an email and type
     */
    Optional<VerificationCode> findTopByEmailAndTypeAndUsedFalseOrderByCreatedAtDesc(
        String email,
        VerificationCode.CodeType type
    );

    /**
     * Find a specific verification code by email, code, and type
     */
    Optional<VerificationCode> findByEmailAndCodeAndType(
        String email,
        String code,
        VerificationCode.CodeType type
    );

    /**
     * Delete all expired verification codes (cleanup task)
     */
    @Modifying
    @Query("DELETE FROM VerificationCode v WHERE v.expiryDate < :now")
    int deleteExpiredCodes(Instant now);

    /**
     * Delete all verification codes for a specific email
     */
    @Modifying
    void deleteByEmail(String email);

    /**
     * Delete all used verification codes older than a specific date
     */
    @Modifying
    @Query("DELETE FROM VerificationCode v WHERE v.used = true AND v.createdAt < :before")
    int deleteUsedCodesBefore(Instant before);
}
