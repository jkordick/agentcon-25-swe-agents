package com.insurance.claims.dto;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

public class ClaimRequest {
    
    @NotNull(message = "Customer ID is required")
    private Long customerId;
    
    @NotBlank(message = "Claim type is required")
    private String claimType;
    
    @NotBlank(message = "Description is required")
    private String description;
    
    public ClaimRequest() {
    }
    
    public ClaimRequest(Long customerId, String claimType, String description) {
        this.customerId = customerId;
        this.claimType = claimType;
        this.description = description;
    }
    
    public Long getCustomerId() {
        return customerId;
    }
    
    public void setCustomerId(Long customerId) {
        this.customerId = customerId;
    }
    
    public String getClaimType() {
        return claimType;
    }
    
    public void setClaimType(String claimType) {
        this.claimType = claimType;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
}
