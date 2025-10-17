package com.auth_user_service.repository;

import com.auth_user_service.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    Optional<User> findByPhone(String phone);
    boolean existsByEmail(String email);
    boolean existsByPhone(String phone);

    @Query("select u from User u where lower(u.username) like lower(concat('%',:q,'%')) or lower(u.email) like lower(concat('%',:q,'%')) or lower(u.phone) like lower(concat('%',:q,'%'))")
    List<User> search(String q);
}