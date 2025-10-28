#!/usr/bin/env python3
"""
Simple Customer Profile Service using Python's built-in http.server
Compatible with Python 3.8+
"""

import json
import re
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from models import Customer, validate_customer_update
from database import customer_db


class CustomerProfileHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, status_code, data, content_type='application/json'):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if isinstance(data, dict):
            response_data = json.dumps(data, indent=2)
        else:
            response_data = str(data)
        
        self.wfile.write(response_data.encode('utf-8'))
    
    def _send_error_response(self, status_code, message):
        """Send error response"""
        error_data = {"error": message}
        self._send_response(status_code, error_data)
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self._send_response(200, {})
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                self._handle_root()
            elif self.path == '/health':
                self._handle_health()
            elif self.path.startswith('/customers/'):
                self._handle_get_customer()
            elif self.path.startswith('/risk-assessment/age-range'):
                self._handle_risk_assessment()
            else:
                self._send_error_response(404, "Not found")
        except Exception as e:
            print(f"Error handling GET request: {e}")
            self._send_error_response(500, "Internal server error")
    
    def do_PATCH(self):
        """Handle PATCH requests"""
        try:
            if self.path.startswith('/customers/'):
                self._handle_update_customer()
            else:
                self._send_error_response(404, "Not found")
        except Exception as e:
            print(f"Error handling PATCH request: {e}")
            self._send_error_response(500, "Internal server error")
    
    def _handle_root(self):
        """Handle root endpoint"""
        response_data = {
            "service": "Customer Profile Service",
            "version": "1.0.0",
            "endpoints": [
                "GET /customers/{id} - Fetch customer profile",
                "PATCH /customers/{id} - Update customer profile",
                "GET /health - Health check",
                "GET /risk-assessment/age-range?age={age} - Get risk assessment information for age range"
            ]
        }
        self._send_response(200, response_data)
    
    def _handle_health(self):
        """Handle health check"""
        response_data = {
            "status": "healthy",
            "service": "customer-profile-service",
            "timestamp": datetime.now().isoformat()
        }
        self._send_response(200, response_data)
    
    def _handle_get_customer(self):
        """Handle GET /customers/{id}"""
        # Extract customer ID from path
        match = re.match(r'/customers/(\d+)', self.path)
        if not match:
            self._send_error_response(400, "Invalid customer ID")
            return
        
        try:
            customer_id = int(match.group(1))
        except ValueError:
            self._send_error_response(400, "Customer ID must be a number")
            return
        
        if customer_id < 1:
            self._send_error_response(400, "Customer ID must be a positive integer")
            return
        
        customer = customer_db.get_customer(customer_id)
        if customer is None:
            self._send_error_response(404, f"Customer with ID {customer_id} not found")
            return
        
        self._send_response(200, customer.to_dict())
    
    def _handle_update_customer(self):
        """Handle PATCH /customers/{id}"""
        # Extract customer ID from path
        match = re.match(r'/customers/(\d+)', self.path)
        if not match:
            self._send_error_response(400, "Invalid customer ID")
            return
        
        try:
            customer_id = int(match.group(1))
        except ValueError:
            self._send_error_response(400, "Customer ID must be a number")
            return
        
        if customer_id < 1:
            self._send_error_response(400, "Customer ID must be a positive integer")
            return
        
        # Check if customer exists
        if customer_db.get_customer(customer_id) is None:
            self._send_error_response(404, f"Customer with ID {customer_id} not found")
            return
        
        # Get request body
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No JSON data provided")
                return
            
            raw_data = self.rfile.read(content_length)
            json_data = json.loads(raw_data.decode('utf-8'))
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON data")
            return
        except Exception as e:
            self._send_error_response(400, f"Error reading request data: {str(e)}")
            return
        
        # Validate update data
        validation_errors = validate_customer_update(json_data)
        if validation_errors:
            self._send_error_response(422, f"Validation error: {', '.join(validation_errors)}")
            return
        
        # Check if at least one field is provided
        updatable_fields = {'phone_number', 'address', 'email'}
        provided_fields = set(json_data.keys()) & updatable_fields
        if not provided_fields:
            self._send_error_response(400, "At least one updatable field must be provided (phone_number, address, email)")
            return
        
        # Update customer
        updated_customer = customer_db.update_customer(customer_id, json_data)
        self._send_response(200, updated_customer.to_dict())
    
    def _handle_risk_assessment(self):
        """Handle GET /risk-assessment/age-range?age={age}"""
        # Parse query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Check if age parameter is provided
        if 'age' not in query_params:
            self._send_error_response(400, "Missing required parameter 'age'")
            return
        
        try:
            age = int(query_params['age'][0])
        except (ValueError, IndexError):
            self._send_error_response(400, "Age must be a valid integer")
            return
        
        # Easter egg for age 1337
        if age == 1337:
            response_data = {
                "age": age,
                "message": "🎉 You found the easter egg! 🎉",
                "joke": "Why do programmers prefer dark mode? Because light attracts bugs! 🐛💡",
                "elite_status": "1337 - You are truly elite!"
            }
            self._send_response(200, response_data)
            return
        
        # Validate age range
        if age < 0:
            self._send_error_response(400, "Age must be a non-negative integer")
            return
        
        if age > 150:
            self._send_error_response(400, "Age must be 150 or less")
            return
        
        # Determine age range and risk assessment
        if age < 18:
            age_range = "Under 18"
            risk_level = "Low"
            risk_factors = ["Limited driving experience", "Parental supervision typically required"]
            premium_modifier = "Standard with parental discount"
        elif age < 25:
            age_range = "18-24"
            risk_level = "High"
            risk_factors = ["Statistically higher accident rates", "Less driving experience", "Higher likelihood of risky behavior"]
            premium_modifier = "Increased by 50-100%"
        elif age < 40:
            age_range = "25-39"
            risk_level = "Low to Medium"
            risk_factors = ["Generally responsible driving behavior", "Established driving history"]
            premium_modifier = "Standard rate"
        elif age < 60:
            age_range = "40-59"
            risk_level = "Low"
            risk_factors = ["Extensive driving experience", "Lower accident rates", "Mature decision-making"]
            premium_modifier = "Reduced by 10-20%"
        elif age < 75:
            age_range = "60-74"
            risk_level = "Medium"
            risk_factors = ["Potential health-related concerns", "Slower reaction times", "Senior discount eligibility"]
            premium_modifier = "Standard rate with senior discount"
        else:
            age_range = "75+"
            risk_level = "High"
            risk_factors = ["Increased health concerns", "Vision and mobility challenges", "Higher accident severity"]
            premium_modifier = "Increased by 30-50%"
        
        response_data = {
            "age": age,
            "age_range": age_range,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "premium_modifier": premium_modifier,
            "description": f"Risk assessment for customers in the {age_range} age range"
        }
        
        self._send_response(200, response_data)
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port=8000):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomerProfileHandler)
    
    print(f"Customer Profile Service starting on http://localhost:{port}")
    print("Available endpoints:")
    print("  GET  /              - Service information")
    print("  GET  /health        - Health check")
    print("  GET  /customers/{id} - Get customer profile")
    print("  PATCH /customers/{id} - Update customer profile")
    print("  GET  /risk-assessment/age-range?age={age} - Get risk assessment by age")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.shutdown()


if __name__ == "__main__":
    run_server()
