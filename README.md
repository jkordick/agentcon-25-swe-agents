# 👾 AgentCon 2025 Berlin: from a chaotic legacy insurance services collection to new a shiny new application with the help of GitHub Copilot SWE-Agent

brought to you by @jkordick and @AlxWachtel

Welcome to a hands-on demo showcasing the power of **software engineering agents**, starting with GitHub Copilot. In this repo, we explore how AI can help analyze, debug, and modernize legacy systems — across multiple languages and architectures.

## 🧩 What’s Inside?

This project contains **three containerized “legacy” backends** from the insurance industry:

| Service | Language | Purpose |
|--------|----------|---------|
| `legacy-java` | Java 11 (Spring Boot, Maven) | Handles insurance claim submission and tracking |
| `legacy-python` | Python 3.12+ | Manages customer profile data |
| `legacy-node` | Node.js 16 (Express) | Calculates policy quotes based on input criteria |

Each backend is accompanied by:
- A `technical-documentation.md`: describing the system architecture and API design
- A `user-handbook.md`: meant for business users or external consumers

🚨 **But be warned:** One of these docs is lying to you. The documentation doesn’t always match reality — just like in real life.

## 🤖 Part 1: AI-Assisted Reality Check

Use GitHub Copilot to:
- Navigate unfamiliar codebases
- Compare implementation vs documentation
- Identify deprecated endpoints or outdated logic
- Suggest fixes or updated documentation

🎯 Your mission: **Find the inconsistencies and bring clarity to the chaos.**

## 🚀 Part 2: From Legacy to Modern Architecture

Once the systems are understood, we’ll use agents to:
- Propose a unified domain model across services
- Scaffold a new, modernized application
- Generate code, documentation, and architecture patterns
- Reuse parts of the legacy code where helpful

Think of this as **agentic pair programming** across legacy and modern systems.

## 🛠️ Getting Started

### Option 1: VS Code Dev Container (Recommended)

For the best development experience with all tools pre-configured:

1. Open this repository in VS Code
2. When prompted, click "Reopen in Container" or run: `Dev Containers: Reopen in Container`
3. Wait for the container to build (first time takes ~5-10 minutes)
4. Start all services: `./scripts/start-all.sh`

The dev container includes Java 11, Node.js 16, Python 3.12+, and all necessary development tools including GitHub Copilot for AI assistance.

### Option 2: Local Installation

Ensure you have installed:
- Java 11 + Maven
- Node.js 16 + npm  
- Python 3.12+ + pip

Then start each service individually:

```bash
# Java Claims API
cd legacy-java && mvn spring-boot:run

# Node.js Quote API  
cd legacy-node && npm install && npm start

# Python Customer API
cd legacy-python && pip install -r requirements.txt && python main.py