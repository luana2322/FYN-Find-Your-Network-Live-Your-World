package com.auth_user_service.dto;

import lombok.Data;
import jakarta.validation.constraints.*;
import javax.validation.constraints.Size;

@Data
public class RegisterRequest {
    @NotBlank
    private String username;
    @Email
    private String email;
    private String phone;
    @NotBlank @Size(min = 6) private String password;
    private boolean useOtp = false;
}