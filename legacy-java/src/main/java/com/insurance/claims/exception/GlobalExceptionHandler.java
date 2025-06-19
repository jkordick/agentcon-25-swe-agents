package com.insurance.claims.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import javax.validation.ConstraintViolationException;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {
    
    /**
     * Handles validation errors for request body validation
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationExceptions(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        
        ErrorResponse errorResponse = new ErrorResponse(
                "Validation failed",
                "One or more fields have validation errors",
                LocalDateTime.now(),
                errors
        );
        
        return ResponseEntity.badRequest().body(errorResponse);
    }
    
    /**
     * Handles constraint violation exceptions
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolationException(ConstraintViolationException ex) {
        ErrorResponse errorResponse = new ErrorResponse(
                "Constraint violation",
                ex.getMessage(),
                LocalDateTime.now(),
                null
        );
        
        return ResponseEntity.badRequest().body(errorResponse);
    }
    
    /**
     * Handles general exceptions
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        ErrorResponse errorResponse = new ErrorResponse(
                "Internal server error",
                "An unexpected error occurred",
                LocalDateTime.now(),
                null
        );
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
    }
    
    /**
     * Error response structure
     */
    public static class ErrorResponse {
        private String error;
        private String message;
        private LocalDateTime timestamp;
        private Map<String, String> validationErrors;
        
        public ErrorResponse(String error, String message, LocalDateTime timestamp, Map<String, String> validationErrors) {
            this.error = error;
            this.message = message;
            this.timestamp = timestamp;
            this.validationErrors = validationErrors;
        }
        
        // Getters
        public String getError() {
            return error;
        }
        
        public String getMessage() {
            return message;
        }
        
        public LocalDateTime getTimestamp() {
            return timestamp;
        }
        
        public Map<String, String> getValidationErrors() {
            return validationErrors;
        }
    }
}
