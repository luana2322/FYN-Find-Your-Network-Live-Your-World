package com.auth_user_service.model;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "users") // PostgreSQL table names usually lowercase
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Works well with PostgreSQL SERIAL
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(unique = true)
    private String email;

    @Column(unique = true)
    private String phone;

    @Column(nullable = false)
    private String password;

    private String avatarUrl;
    private String bio;
    private String fullName;
}