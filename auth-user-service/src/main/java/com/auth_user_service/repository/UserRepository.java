package com.auth_user_service.repository;

import com.auth_user_service.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository for User entity.
 * Provides database access methods for user management.
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * Find user by email address
     */
    Optional<User> findByEmail(String email);

    /**
     * Find user by phone number
     */
    Optional<User> findByPhone(String phone);

    /**
     * Find user by username
     */
    Optional<User> findByUsername(String username);

    /**
     * Check if a user with the given email exists
     */
    boolean existsByEmail(String email);

    /**
     * Check if a user with the given phone exists
     */
    boolean existsByPhone(String phone);

    /**
     * Check if a user with the given username exists
     */
    boolean existsByUsername(String username);

    /**
     * Search users by name, username, email, or phone
     * Searches across first name, last name, username, email, and phone fields
     */
    @Query("SELECT u FROM User u WHERE " +
           "LOWER(u.firstName) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
           "LOWER(u.lastName) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
           "LOWER(u.username) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
           "LOWER(u.email) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
           "LOWER(u.phone) LIKE LOWER(CONCAT('%', :q, '%'))")
    List<User> search(@Param("q") String q);

    /**
     * Find all active users
     */
    List<User> findByIsActiveTrue();
}
