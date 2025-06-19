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
