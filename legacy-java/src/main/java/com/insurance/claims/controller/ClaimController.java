package com.insurance.claims.controller;

import com.insurance.claims.dto.ClaimRequest;
import com.insurance.claims.model.Claim;
import com.insurance.claims.service.ClaimService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.Optional;

@RestController
@RequestMapping("/claims")
@Validated
public class ClaimController {
    
    private final ClaimService claimService;
    
    @Autowired
    public ClaimController(ClaimService claimService) {
        this.claimService = claimService;
    }
    
    /**
     * Submits a new insurance claim
     * 
     * @param claimRequest the claim request containing customer ID, claim type, and description
     * @return ResponseEntity with the created claim and HTTP 201 status
     */
    @PostMapping
    public ResponseEntity<Claim> submitClaim(@Valid @RequestBody ClaimRequest claimRequest) {
        Claim createdClaim = claimService.createClaim(claimRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdClaim);
    }
    
    /**
     * Retrieves the status and details of a specific claim
     * 
     * @param id the ID of the claim to retrieve
     * @return ResponseEntity with the claim if found (HTTP 200) or HTTP 404 if not found
     */
    @GetMapping("/{id}")
    public ResponseEntity<Claim> getClaimById(@PathVariable @NotNull Long id) {
        Optional<Claim> claim = claimService.getClaimById(id);
        
        if (claim.isPresent()) {
            return ResponseEntity.ok(claim.get());
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * Health check endpoint to verify the service is running
     * 
     * @return ResponseEntity with service status
     */
    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Claims API is running. Total claims: " + claimService.getClaimsCount());
    }
}
