package com.auth_user_service.controller;

import com.auth_user_service.dto.follow.FollowResponse;
import com.auth_user_service.service.FollowService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/follow")
@RequiredArgsConstructor
public class FollowController {

    private final FollowService followService;

    @PostMapping("/{followingId}")
    public void follow(@AuthenticationPrincipal Long userId, @PathVariable Long followingId){
        followService.follow(userId, followingId);
    }

    @DeleteMapping("/{followingId}")
    public void unfollow(@AuthenticationPrincipal Long userId, @PathVariable Long followingId){
        followService.unfollow(userId, followingId);
    }

    @GetMapping("/followers")
    public List<FollowResponse> listFollowers(@AuthenticationPrincipal Long userId){
        return followService.listFollowers(userId);
    }

    @GetMapping("/following")
    public List<FollowResponse> listFollowing(@AuthenticationPrincipal Long userId){
        return followService.listFollowing(userId);
    }
}