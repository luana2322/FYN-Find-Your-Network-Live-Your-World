package com.auth_user_service.security;


import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.security.Key;
import java.util.Date;
import java.util.UUID;
@Component
public class JwtTokenProvider {

    @Value("${jwt.secret}") private String jwtSecret;
    @Value("${jwt.access-exp-ms}") private long accessExpMs;

    private Key getKey() { return Keys.hmacShaKeyFor(jwtSecret.getBytes()); }

    public String generateAccessToken(String subject) {
        Date now = new Date();
        Date exp = new Date(now.getTime() + accessExpMs);
        return Jwts.builder()
                .setId(UUID.randomUUID().toString())
                .setSubject(subject)
                .setIssuedAt(now)
                .setExpiration(exp)
                .signWith(getKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public boolean validateToken(String token) {
        try { Jwts.parserBuilder().setSigningKey(getKey()).build().parseClaimsJws(token); return true; }
        catch (JwtException | IllegalArgumentException ex) { return false; }
    }

    public String getSubject(String token) {
        return Jwts.parserBuilder().setSigningKey(getKey()).build().parseClaimsJws(token).getBody().getSubject();
    }

    public String getJti(String token) {
        return Jwts.parserBuilder().setSigningKey(getKey()).build().parseClaimsJws(token).getBody().getId();
    }

    public long getAccessExpMs() { return accessExpMs; }
}