package com.auth_user_service.controller;

import com.auth_user_service.dto.auth.AuthResponse;
import com.auth_user_service.dto.auth.LoginRequest;
import com.auth_user_service.dto.auth.RegisterRequest;
import com.auth_user_service.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public AuthResponse register(@RequestBody RegisterRequest request){
        return authService.register(request);
    }

    @PostMapping("/login")
    public AuthResponse login(@RequestBody LoginRequest request){
        return authService.login(request);
    }

    @PostMapping("/refresh")
    public AuthResponse refresh(@RequestParam String refreshToken){
        return authService.refreshToken(refreshToken);
    }
}