package com.auth_user_service.dto;

import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * Request DTO for updating user profile information.
 */
@Data
public class UpdateProfileRequest {

    @Size(min = 3, max = 50, message = "Username must be between 3 and 50 characters")
    private String username;

    @Size(max = 100, message = "First name must not exceed 100 characters")
    private String firstName;

    @Size(max = 100, message = "Last name must not exceed 100 characters")
    private String lastName;

    @Size(max = 1000, message = "Bio must not exceed 1000 characters")
    private String bio;

    @Size(min = 10, max = 20, message = "Phone number must be between 10 and 20 characters")
    private String phone;
}
