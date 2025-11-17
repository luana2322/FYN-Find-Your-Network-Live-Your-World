package com.auth_user_service.repository;

import com.auth_user_service.model.BlacklistedToken;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.Instant;

/**
 * Repository for managing blacklisted JWT tokens.
 * Replaces Redis-based token blacklisting.
 */
@Repository
public interface BlacklistedTokenRepository extends JpaRepository<BlacklistedToken, Long> {

    /**
     * Check if a token with the given JTI is blacklisted
     */
    boolean existsByJti(String jti);

    /**
     * Delete all expired blacklisted tokens (cleanup task)
     */
    @Modifying
    @Query("DELETE FROM BlacklistedToken b WHERE b.expiryDate < :now")
    int deleteExpiredTokens(Instant now);
}
