package com.auth_user_service.controller;

import com.auth_user_service.service.FollowService;
import com.auth_user_service.util.ResponseUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/follows")
@RequiredArgsConstructor
public class FollowController {
    @Autowired
    private  FollowService followService;

    @PostMapping("/{followeeId}")
    public ResponseEntity<?> followUser(Authentication authentication, @PathVariable Long followeeId) {
        try {
            followService.followUser(authentication, followeeId);
            return ResponseUtil.success(null, "User followed successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @DeleteMapping("/{followeeId}")
    public ResponseEntity<?> unfollowUser(Authentication authentication, @PathVariable Long followeeId) {
        try {
            followService.unfollowUser(authentication, followeeId);
            return ResponseUtil.success(null, "User unfollowed successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @GetMapping("/{userId}/followers")
    public ResponseEntity<?> getFollowers(@PathVariable Long userId) {
        try {
            List<Long> followers = followService.getFollowers(userId);
            return ResponseUtil.success(followers, "Followers retrieved successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @GetMapping("/{userId}/following")
    public ResponseEntity<?> getFollowing(@PathVariable Long userId) {
        try {
            List<Long> following = followService.getFollowing(userId);
            return ResponseUtil.success(following, "Following list retrieved successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @GetMapping("/{userId}/is-following")
    public ResponseEntity<?> isFollowing(Authentication authentication, @PathVariable Long userId) {
        try {
            boolean isFollowing = followService.isFollowing(authentication, userId);
            Map<String, Object> result = new HashMap<>();
            result.put("isFollowing", isFollowing);
            return ResponseUtil.success(result, "Follow status retrieved successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }

    @GetMapping("/{userId}/stats")
    public ResponseEntity<?> getFollowStats(@PathVariable Long userId) {
        try {
            Map<String, Object> stats = new HashMap<>();
            stats.put("followersCount", followService.getFollowersCount(userId));
            stats.put("followingCount", followService.getFollowingCount(userId));
            return ResponseUtil.success(stats, "Follow stats retrieved successfully");
        } catch (Exception e) {
            return ResponseUtil.error(e.getMessage());
        }
    }
}
