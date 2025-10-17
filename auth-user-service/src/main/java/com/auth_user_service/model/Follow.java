package com.auth_user_service.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "follows", uniqueConstraints = @UniqueConstraint(columnNames = {"follower_id","followee_id"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Follow {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(name = "follower_id") private Long followerId;
    @Column(name = "followee_id") private Long followeeId;
    private Instant createdAt = Instant.now();
}