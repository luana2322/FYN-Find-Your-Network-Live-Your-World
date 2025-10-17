package com.auth_user_service.service.impl;

import com.auth_user_service.exception.BusinessLogicException;
import com.auth_user_service.exception.ResourceNotFoundException;
import com.auth_user_service.model.Follow;
import com.auth_user_service.model.User;
import com.auth_user_service.repository.FollowRepository;
import com.auth_user_service.repository.UserRepository;
import com.auth_user_service.service.FollowService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FollowServiceImpl implements FollowService {

    private final FollowRepository followRepository;
    private final UserRepository userRepository;

    @Override
    @Transactional
    public void followUser(Authentication authentication, Long followeeId) {
        String email = authentication.getName();
        User follower = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));
        
        User followee = userRepository.findById(followeeId)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", followeeId));

        if (follower.getId().equals(followeeId)) {
            throw new BusinessLogicException("Cannot follow yourself");
        }

        // Check if already following
        if (followRepository.existsByFollowerIdAndFolloweeId(follower.getId(), followeeId)) {
            throw new BusinessLogicException("Already following this user");
        }

        Follow follow = Follow.builder()
                .followerId(follower.getId())
                .followeeId(followeeId)
                .build();

        followRepository.save(follow);
    }

    @Override
    @Transactional
    public void unfollowUser(Authentication authentication, Long followeeId) {
        String email = authentication.getName();
        User follower = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

        Follow follow = followRepository.findByFollowerIdAndFolloweeId(follower.getId(), followeeId)
                .orElseThrow(() -> new BusinessLogicException("Not following this user"));

        followRepository.delete(follow);
    }

    @Override
    public List<Long> getFollowers(Long userId) {
        return followRepository.findByFolloweeId(userId)
                .stream()
                .map(Follow::getFollowerId)
                .collect(Collectors.toList());
    }

    @Override
    public List<Long> getFollowing(Long userId) {
        return followRepository.findByFollowerId(userId)
                .stream()
                .map(Follow::getFolloweeId)
                .collect(Collectors.toList());
    }

    @Override
    public boolean isFollowing(Authentication authentication, Long followeeId) {
        String email = authentication.getName();
        User follower = userRepository.findByEmail(email)
                .orElseThrow(() -> new ResourceNotFoundException("User", "email", email));

        return followRepository.existsByFollowerIdAndFolloweeId(follower.getId(), followeeId);
    }

    @Override
    public int getFollowersCount(Long userId) {
        return followRepository.countByFolloweeId(userId);
    }

    @Override
    public int getFollowingCount(Long userId) {
        return followRepository.countByFollowerId(userId);
    }
}
