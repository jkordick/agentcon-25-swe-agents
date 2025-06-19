#!/bin/bash

echo "🚀 Setting up AgentCon 2025 Multi-Language Insurance Services Development Environment..."

# Navigate to workspace root
cd /workspaces/agentcon-25-swe-agents

# Setup Java Maven dependencies
echo "📦 Installing Java dependencies..."
cd legacy-java
mvn dependency:resolve
mvn compile
cd ..

# Setup Node.js dependencies  
echo "📦 Installing Node.js dependencies..."
cd legacy-node
npm install
cd ..

# Setup Python dependencies
echo "📦 Installing Python dependencies..."
cd legacy-python
pip install -r requirements.txt
# Install additional development tools
pip install pytest-cov black flake8 mypy
cd ..

# Create useful scripts directory
mkdir -p scripts

# Create a script to start all services
cat > scripts/start-all.sh << 'EOF'
#!/bin/bash

echo "🎯 Starting all legacy insurance services..."

# Start Java Claims API (Spring Boot)
echo "Starting Java Claims API on port 8080..."
cd legacy-java && mvn spring-boot:run &
JAVA_PID=$!

# Start Node.js Quote API
echo "Starting Node.js Quote API on port 3000..."
cd ../legacy-node && npm start &
NODE_PID=$!

# Start Python Customer API (assuming it runs on port 5000)
echo "Starting Python Customer API on port 5000..."
cd ../legacy-python && python main.py &
PYTHON_PID=$!

cd ..

echo "🎉 All services started!"
echo "Java Claims API: http://localhost:8080"
echo "Node.js Quote API: http://localhost:3000" 
echo "Python Customer API: http://localhost:5000"
echo ""
echo "To stop all services, run: scripts/stop-all.sh"

# Save PIDs for cleanup
echo $JAVA_PID > .java_pid
echo $NODE_PID > .node_pid  
echo $PYTHON_PID > .python_pid

wait
EOF

# Create a script to stop all services
cat > scripts/stop-all.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping all services..."

# Kill processes by PID if files exist
if [ -f .java_pid ]; then
    kill $(cat .java_pid) 2>/dev/null
    rm .java_pid
fi

if [ -f .node_pid ]; then
    kill $(cat .node_pid) 2>/dev/null
    rm .node_pid
fi

if [ -f .python_pid ]; then
    kill $(cat .python_pid) 2>/dev/null
    rm .python_pid
fi

# Also kill by port in case PIDs don't work
pkill -f "spring-boot:run" 2>/dev/null
pkill -f "node index.js" 2>/dev/null
pkill -f "python main.py" 2>/dev/null

echo "✅ All services stopped!"
EOF

# Create a script to run all tests
cat > scripts/test-all.sh << 'EOF'
#!/bin/bash

echo "🧪 Running all tests..."

echo "Testing Java Claims API..."
cd legacy-java && mvn test
JAVA_RESULT=$?

echo "Testing Node.js Quote API..."
cd ../legacy-node && npm test
NODE_RESULT=$?

echo "Testing Python Customer API..."
cd ../legacy-python && python -m pytest
PYTHON_RESULT=$?

cd ..

echo ""
echo "📊 Test Results:"
echo "Java: $([ $JAVA_RESULT -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"
echo "Node.js: $([ $NODE_RESULT -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"
echo "Python: $([ $PYTHON_RESULT -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")"

# Exit with error if any tests failed
if [ $JAVA_RESULT -ne 0 ] || [ $NODE_RESULT -ne 0 ] || [ $PYTHON_RESULT -ne 0 ]; then
    exit 1
fi
EOF

# Make scripts executable
chmod +x scripts/*.sh

# Create a basic HTTP client test file for manual API testing
cat > api-tests.http << 'EOF'
### Test Java Claims API
GET http://localhost:8080/health
Accept: application/json

### Test Node.js Quote API  
GET http://localhost:3000/health
Accept: application/json

### Test Python Customer API
GET http://localhost:5000/health
Accept: application/json

### Create a new claim (Java API)
POST http://localhost:8080/api/claims
Content-Type: application/json

{
  "policyNumber": "POL123456",
  "description": "Car accident on highway",
  "amount": 5000.00
}

### Get a quote (Node.js API)
POST http://localhost:3000/api/quote
Content-Type: application/json

{
  "age": 30,
  "vehicleType": "sedan",
  "coverage": "comprehensive"
}
EOF

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "📖 Quick Start Guide:"
echo "  • Start all services: ./scripts/start-all.sh"
echo "  • Stop all services: ./scripts/stop-all.sh"
echo "  • Run all tests: ./scripts/test-all.sh"
echo "  • Test APIs manually: Use api-tests.http with REST Client extension"
echo ""
echo "🔧 Individual service commands:"
echo "  • Java: cd legacy-java && mvn spring-boot:run"
echo "  • Node.js: cd legacy-node && npm start"
echo "  • Python: cd legacy-python && python main.py"
echo ""
echo "Happy coding! 🚀"
