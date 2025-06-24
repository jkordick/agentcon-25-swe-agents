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
from risk_assessment import calculate_customer_risk_profile


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
                if '/risk-profile' in self.path:
                    self._handle_get_risk_profile()
                else:
                    self._handle_get_customer()
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
                "GET /customers/{id}/risk-profile - Get customer risk assessment",
                "PATCH /customers/{id} - Update customer profile",
                "GET /health - Health check"
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
    
    def _handle_get_risk_profile(self):
        """Handle GET /customers/{id}/risk-profile"""
        # Extract customer ID from path
        match = re.match(r'/customers/(\d+)/risk-profile', self.path)
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
        
        try:
            # Calculate risk profile
            risk_profile = calculate_customer_risk_profile(customer.to_dict())
            self._send_response(200, risk_profile)
        except ValueError as e:
            # Customer has insufficient data for risk calculation
            self._send_error_response(422, str(e))
        except Exception as e:
            # Calculation error
            print(f"Risk calculation error for customer {customer_id}: {e}")
            self._send_error_response(500, "Risk calculation failed")
    
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
    print("  GET  /customers/{id}/risk-profile - Get customer risk assessment")
    print("  PATCH /customers/{id} - Update customer profile")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.shutdown()


if __name__ == "__main__":
    run_server()
