package com.insurance.claims.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.insurance.claims.dto.ClaimRequest;
import com.insurance.claims.model.ClaimStatus;
import com.insurance.claims.service.ClaimService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ClaimController.class)
public class ClaimControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private ClaimService claimService;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    public void testSubmitClaim_ValidRequest_ReturnsCreated() throws Exception {
        ClaimRequest request = new ClaimRequest(12345L, "Auto", "Car accident on highway");
        
        mockMvc.perform(post("/claims")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated());
    }
    
    @Test
    public void testSubmitClaim_InvalidRequest_ReturnsBadRequest() throws Exception {
        ClaimRequest request = new ClaimRequest(null, "", ""); // Invalid request
        
        mockMvc.perform(post("/claims")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }
    
    @Test
    public void testGetClaim_ExistingId_ReturnsOk() throws Exception {
        mockMvc.perform(get("/claims/1"))
                .andExpect(status().isOk());
    }
    
    @Test
    public void testHealthCheck_ReturnsOk() throws Exception {
        mockMvc.perform(get("/claims/health"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Claims API is running")));
    }
}
