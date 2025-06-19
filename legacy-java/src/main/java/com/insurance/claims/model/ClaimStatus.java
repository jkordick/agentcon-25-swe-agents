package com.insurance.claims.model;

public enum ClaimStatus {
    SUBMITTED("Submitted"),
    UNDER_REVIEW("Under Review"),
    APPROVED("Approved"),
    DENIED("Denied"),
    CLOSED("Closed");
    
    private final String displayName;
    
    ClaimStatus(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }
}
