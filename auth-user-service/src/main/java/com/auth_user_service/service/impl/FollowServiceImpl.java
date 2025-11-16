package com.auth_user_service.service.impl;


import com.auth_user_service.dto.follow.FollowResponse;
import com.auth_user_service.model.Follow;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.FollowRepository;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.FollowService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FollowServiceImpl implements FollowService {

    private final UserRepository userRepository;
    private final FollowRepository followRepository;

    @Override
    public void follow(Long followerId, Long followingId) {
        if(followerId.equals(followingId)) throw new RuntimeException("Cannot follow yourself");
        User follower = userRepository.findById(followerId)
                .orElseThrow(() -> new RuntimeException("Follower not found"));
        User following = userRepository.findById(followingId)
                .orElseThrow(() -> new RuntimeException("Following not found"));
        if(followRepository.findByFollowerAndFollowing(follower, following).isPresent()) return;
        Follow f = Follow.builder().follower(follower).following(following).build();
        followRepository.save(f);
    }

    @Override
    public void unfollow(Long followerId, Long followingId) {
        User follower = userRepository.findById(followerId)
                .orElseThrow(() -> new RuntimeException("Follower not found"));
        User following = userRepository.findById(followingId)
                .orElseThrow(() -> new RuntimeException("Following not found"));
        followRepository.findByFollowerAndFollowing(follower, following)
                .ifPresent(followRepository::delete);
    }

    @Override
    public List<FollowResponse> listFollowers(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return followRepository.findByFollowing(user)
                .stream()
                .map(f -> {
                    FollowResponse r = new FollowResponse();
                    r.setFollowerId(f.getFollower().getId());
                    r.setFollowingId(f.getFollowing().getId());
                    return r;
                }).collect(Collectors.toList());
    }

    @Override
    public List<FollowResponse> listFollowing(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return followRepository.findByFollower(user)
                .stream()
                .map(f -> {
                    FollowResponse r = new FollowResponse();
                    r.setFollowerId(f.getFollower().getId());
                    r.setFollowingId(f.getFollowing().getId());
                    return r;
                }).collect(Collectors.toList());
    }
}