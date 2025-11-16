package com.auth_user_service.service;

import com.auth_user_service.dto.follow.FollowResponse;

import java.util.List;

public interface FollowService {
    void follow(Long followerId, Long followingId);
    void unfollow(Long followerId, Long followingId);
    List<FollowResponse> listFollowers(Long userId);
    List<FollowResponse> listFollowing(Long userId);
}