package com.insurance.claims.service;

import com.insurance.claims.dto.ClaimRequest;
import com.insurance.claims.model.Claim;
import com.insurance.claims.model.ClaimStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

public class ClaimServiceTest {
    
    private ClaimService claimService;
    
    @BeforeEach
    public void setUp() {
        claimService = new ClaimService();
    }
    
    @Test
    public void testCreateClaim_ValidRequest_ReturnsClaimWithId() {
        ClaimRequest request = new ClaimRequest(12345L, "Auto", "Car accident on highway");
        
        Claim createdClaim = claimService.createClaim(request);
        
        assertNotNull(createdClaim);
        assertNotNull(createdClaim.getId());
        assertEquals(12345L, createdClaim.getCustomerId());
        assertEquals("Auto", createdClaim.getClaimType());
        assertEquals("Car accident on highway", createdClaim.getDescription());
        assertEquals(ClaimStatus.SUBMITTED, createdClaim.getStatus());
        assertNotNull(createdClaim.getCreatedAt());
        assertNotNull(createdClaim.getUpdatedAt());
    }
    
    @Test
    public void testGetClaimById_ExistingClaim_ReturnsClaim() {
        ClaimRequest request = new ClaimRequest(12345L, "Auto", "Car accident on highway");
        Claim createdClaim = claimService.createClaim(request);
        
        Optional<Claim> retrievedClaim = claimService.getClaimById(createdClaim.getId());
        
        assertTrue(retrievedClaim.isPresent());
        assertEquals(createdClaim.getId(), retrievedClaim.get().getId());
        assertEquals(createdClaim.getCustomerId(), retrievedClaim.get().getCustomerId());
    }
    
    @Test
    public void testGetClaimById_NonExistingClaim_ReturnsEmpty() {
        Optional<Claim> retrievedClaim = claimService.getClaimById(999L);
        
        assertFalse(retrievedClaim.isPresent());
    }
    
    @Test
    public void testUpdateClaimStatus_ExistingClaim_UpdatesStatus() {
        ClaimRequest request = new ClaimRequest(12345L, "Auto", "Car accident on highway");
        Claim createdClaim = claimService.createClaim(request);
        
        Optional<Claim> updatedClaim = claimService.updateClaimStatus(createdClaim.getId(), ClaimStatus.UNDER_REVIEW);
        
        assertTrue(updatedClaim.isPresent());
        assertEquals(ClaimStatus.UNDER_REVIEW, updatedClaim.get().getStatus());
    }
    
    @Test
    public void testGetClaimsCount_NoClaimsInitially_ReturnsZero() {
        assertEquals(0, claimService.getClaimsCount());
    }
    
    @Test
    public void testGetClaimsCount_AfterCreatingClaims_ReturnsCorrectCount() {
        ClaimRequest request1 = new ClaimRequest(12345L, "Auto", "Car accident");
        ClaimRequest request2 = new ClaimRequest(67890L, "Home", "Fire damage");
        
        claimService.createClaim(request1);
        claimService.createClaim(request2);
        
        assertEquals(2, claimService.getClaimsCount());
    }
}
