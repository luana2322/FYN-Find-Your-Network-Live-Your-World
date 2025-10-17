package com.auth_user_service.service;

import org.springframework.security.core.Authentication;

import java.util.List;

public interface FollowService {
    void followUser(Authentication authentication, Long followeeId);
    void unfollowUser(Authentication authentication, Long followeeId);
    List<Long> getFollowers(Long userId);
    List<Long> getFollowing(Long userId);
    boolean isFollowing(Authentication authentication, Long followeeId);
    int getFollowersCount(Long userId);
    int getFollowingCount(Long userId);
}
