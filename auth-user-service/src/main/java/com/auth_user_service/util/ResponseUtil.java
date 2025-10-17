package com.auth_user_service.util;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class ResponseUtil {
    
    public static ResponseEntity<Map<String, Object>> success(Object data, String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", message);
        response.put("data", data);
        response.put("timestamp", Instant.now());
        return ResponseEntity.ok(response);
    }
    
    public static ResponseEntity<Map<String, Object>> success(Object data) {
        return success(data, "Operation successful");
    }
    
    public static ResponseEntity<Map<String, Object>> error(String message) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        response.put("message", message);
        response.put("timestamp", Instant.now());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }
    
    public static ResponseEntity<Map<String, Object>> error(String message, HttpStatus status) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        response.put("message", message);
        response.put("timestamp", Instant.now());
        return ResponseEntity.status(status).body(response);
    }
}
