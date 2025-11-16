package com.auth_user_service.dto.follow;

import lombok.Data;

@Data
public class FollowResponse {
    private Long followerId;
    private Long followingId;
}