package com.flightontime.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, Object> body = new HashMap<>();
        body.put("error", "Bad Request");
        body.put("message", ex.getBindingResult().getFieldErrors()
                .stream()
                .map(e -> e.getField() + " " + e.getDefaultMessage())
                .toList());
        body.put("timestamp", System.currentTimeMillis());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(body);
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, Object>> handleRuntime(RuntimeException ex) {
        Map<String, Object> body = new HashMap<>();
        body.put("error", "Service Unavailable");
        body.put("message", ex.getMessage());
        body.put("timestamp", System.currentTimeMillis());
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(body);
    }
}