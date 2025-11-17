package com.auth_user_service.service.impl;

import com.auth_user_service.model.BlacklistedToken;
import com.auth_user_service.repository.BlacklistedTokenRepository;
import com.auth_user_service.service.JwtService;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.security.Key;
import java.time.Instant;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.function.Function;

/**
 * JWT Service implementation.
 * Handles JWT token generation, validation, and blacklisting.
 * Uses database for token blacklisting instead of Redis.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class JwtServiceImpl implements JwtService {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.access-expiration}")
    private long accessExpiration;

    @Value("${jwt.refresh-expiration}")
    private long refreshExpiration;

    private final BlacklistedTokenRepository blacklistedTokenRepository;

    @Override
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    @Override
    public String generateToken(UserDetails userDetails) {
        return generateToken(new HashMap<>(), userDetails);
    }

    @Override
    public String generateToken(Map<String, Object> extraClaims, UserDetails userDetails) {
        return buildToken(extraClaims, userDetails, accessExpiration);
    }

    @Override
    public String generateRefreshToken(UserDetails userDetails) {
        return buildToken(new HashMap<>(), userDetails, refreshExpiration);
    }

    @Override
    public boolean isTokenValid(String token, UserDetails userDetails) {
        try {
            final String username = extractUsername(token);

            // If userDetails is provided, validate username matches
            if (userDetails != null && !username.equals(userDetails.getUsername())) {
                return false;
            }

            // Check if token is expired
            if (isTokenExpired(token)) {
                return false;
            }

            // Check if token is blacklisted
            if (isTokenBlacklisted(token)) {
                return false;
            }

            return true;
        } catch (Exception e) {
            log.error("Error validating token: {}", e.getMessage());
            return false;
        }
    }

    @Override
    public boolean isTokenExpired(String token) {
        try {
            return extractExpiration(token).before(new Date());
        } catch (Exception e) {
            log.error("Error checking token expiration: {}", e.getMessage());
            return true;
        }
    }

    @Override
    @Transactional
    public void blacklistToken(String token) {
        try {
            String jti = extractClaim(token, Claims::getId);
            Date expiration = extractExpiration(token);

            // Only blacklist if not already blacklisted
            if (!blacklistedTokenRepository.existsByJti(jti)) {
                BlacklistedToken blacklistedToken = BlacklistedToken.builder()
                        .jti(jti)
                        .expiryDate(expiration.toInstant())
                        .reason("User logout")
                        .build();

                blacklistedTokenRepository.save(blacklistedToken);
                log.info("Token with JTI {} has been blacklisted", jti);
            }
        } catch (Exception e) {
            log.error("Error blacklisting token: {}", e.getMessage());
            throw new RuntimeException("Failed to blacklist token", e);
        }
    }

    @Override
    public boolean isTokenBlacklisted(String token) {
        try {
            String jti = extractClaim(token, Claims::getId);
            return blacklistedTokenRepository.existsByJti(jti);
        } catch (Exception e) {
            log.error("Error checking if token is blacklisted: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Cleanup expired blacklisted tokens (can be called by scheduled task)
     */
    @Transactional
    public int cleanupExpiredBlacklistedTokens() {
        int deleted = blacklistedTokenRepository.deleteExpiredTokens(Instant.now());
        if (deleted > 0) {
            log.info("Cleaned up {} expired blacklisted tokens", deleted);
        }
        return deleted;
    }

    private String buildToken(Map<String, Object> extraClaims, UserDetails userDetails, long expiration) {
        return Jwts
                .builder()
                .setClaims(extraClaims)
                .setId(UUID.randomUUID().toString())
                .setSubject(userDetails.getUsername())
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + expiration))
                .signWith(getSignInKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    private <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        return Jwts
                .parserBuilder()
                .setSigningKey(getSignInKey())
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    private Key getSignInKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
