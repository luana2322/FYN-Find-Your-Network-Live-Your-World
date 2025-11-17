package com.auth_user_service.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * Request DTO for email verification.
 */
@Data
public class VerifyRequest {

    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    private String email;

    @NotBlank(message = "Verification code is required")
    @Size(min = 6, max = 10, message = "Verification code must be between 6 and 10 characters")
    private String code;
}
