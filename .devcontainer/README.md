# Development Environment

This project uses a VS Code Dev Container to provide a consistent development environment across all three legacy services.

## 🐳 Dev Container Features

The dev container includes:

- **Java 11** with Maven for the Claims API
- **Node.js 16** with npm/yarn for the Quote API  
- **Python 3.8** with pip for the Customer API
- **VS Code Extensions** for Java, Node.js, Python development
- **GitHub Copilot** for AI-assisted development
- **REST Client** for API testing
- **Docker-in-Docker** for containerization workflows

## 🚀 Quick Start

1. Open this repository in VS Code
2. When prompted, click "Reopen in Container" or run the "Dev Containers: Reopen in Container" command
3. Wait for the container to build and setup (first time takes ~5-10 minutes)
4. Once ready, use the provided scripts:

```bash
# Start all three services
./scripts/start-all.sh

# Run all tests
./scripts/test-all.sh

# Stop all services
./scripts/stop-all.sh
```

## 🔗 Service Endpoints

Once started, the services will be available at:

- **Java Claims API**: http://localhost:8080
- **Node.js Quote API**: http://localhost:3000
- **Python Customer API**: http://localhost:5000

## 🧪 Testing APIs

Use the included `api-tests.http` file with the REST Client extension to manually test the APIs, or run the automated tests:

```bash
# Test individual services
cd legacy-java && mvn test
cd legacy-node && npm test  
cd legacy-python && python -m pytest
```

## 🛠️ Development Tips

- The dev container automatically installs dependencies for all three services
- Port forwarding is configured for all service ports
- File exclusions are set to hide build artifacts (`target/`, `node_modules/`, `__pycache__/`)
- Java, Node.js, and Python language servers are pre-configured

## 🔧 Manual Setup (Alternative)

If you prefer not to use the dev container, ensure you have:
- Java 11 + Maven
- Node.js 16 + npm
- Python 3.8 + pip
- Your preferred IDE with appropriate language extensions

## 📝 Notes

- The dev container uses the official Microsoft dev container base image
- All three language runtimes are installed in a single container for convenience
- GitHub Copilot extensions are included to assist with the legacy code analysis tasks
