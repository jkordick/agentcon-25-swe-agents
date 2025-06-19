package com.insurance.claims.service;

import com.insurance.claims.dto.ClaimRequest;
import com.insurance.claims.model.Claim;
import com.insurance.claims.model.ClaimStatus;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class ClaimService {
    
    private final Map<Long, Claim> claimsStorage = new HashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    public ClaimService() {
        initializeHardcodedClaims();
    }
    
    /**
     * Initializes the service with 3 hardcoded claims for testing purposes
     */
    private void initializeHardcodedClaims() {
        // Claim 1: Auto insurance claim
        Claim claim1 = new Claim(12345L, "Auto", "Car accident on highway - rear-end collision");
        claim1.setId(idGenerator.getAndIncrement());
        claim1.setStatus(ClaimStatus.UNDER_REVIEW);
        claimsStorage.put(claim1.getId(), claim1);
        
        // Claim 2: Home insurance claim
        Claim claim2 = new Claim(67890L, "Home", "Water damage from burst pipe in basement");
        claim2.setId(idGenerator.getAndIncrement());
        claim2.setStatus(ClaimStatus.APPROVED);
        claimsStorage.put(claim2.getId(), claim2);
        
        // Claim 3: Health insurance claim
        Claim claim3 = new Claim(11111L, "Health", "Emergency room visit for broken arm");
        claim3.setId(idGenerator.getAndIncrement());
        claim3.setStatus(ClaimStatus.SUBMITTED);
        claimsStorage.put(claim3.getId(), claim3);
    }
    
    /**
     * Creates a new claim from the provided request
     * 
     * @param claimRequest the claim request containing customer ID, type, and description
     * @return the created claim with assigned ID and initial status
     */
    public Claim createClaim(ClaimRequest claimRequest) {
        Claim claim = new Claim(
                claimRequest.getCustomerId(),
                claimRequest.getClaimType(),
                claimRequest.getDescription()
        );
        
        Long claimId = idGenerator.getAndIncrement();
        claim.setId(claimId);
        
        claimsStorage.put(claimId, claim);
        
        return claim;
    }
    
    /**
     * Retrieves a claim by its ID
     * 
     * @param claimId the ID of the claim to retrieve
     * @return an Optional containing the claim if found, or empty if not found
     */
    public Optional<Claim> getClaimById(Long claimId) {
        return Optional.ofNullable(claimsStorage.get(claimId));
    }
    
    /**
     * Updates the status of an existing claim
     * 
     * @param claimId the ID of the claim to update
     * @param newStatus the new status to set
     * @return an Optional containing the updated claim if found, or empty if not found
     */
    public Optional<Claim> updateClaimStatus(Long claimId, ClaimStatus newStatus) {
        Claim claim = claimsStorage.get(claimId);
        if (claim != null) {
            claim.setStatus(newStatus);
            return Optional.of(claim);
        }
        return Optional.empty();
    }
    
    /**
     * Returns the total number of claims in storage
     * 
     * @return the count of claims
     */
    public int getClaimsCount() {
        return claimsStorage.size();
    }
}
