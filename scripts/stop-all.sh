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
