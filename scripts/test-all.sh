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
