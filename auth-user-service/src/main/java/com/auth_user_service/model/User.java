package com.auth_user_service.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name="users")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
      @Id
      @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  @Column(unique=true)
  private String email;
  @Column(unique=true)
  private String phone;
  @Column(unique=true)
  private String username;
  private String password;
  private String avatarUrl;
  @Column(columnDefinition = "TEXT")
  private String bio;
  private Boolean isActive = true;
  private Instant createdAt;
  private Instant updatedAt;
}
