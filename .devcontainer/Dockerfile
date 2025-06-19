FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install additional system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        curl \
        wget \
        unzip \
        vim \
        nano \
        htop \
        tree \
        jq \
        build-essential \
        pkg-config \
        libssl-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Create workspace directory
RUN mkdir -p /workspaces/agentcon-25-swe-agents
WORKDIR /workspaces/agentcon-25-swe-agents

# Set environment variables for development
ENV JAVA_HOME=/usr/lib/jvm/msopenjdk-current
ENV PATH=$JAVA_HOME/bin:$PATH
ENV NODE_ENV=development
ENV PYTHONPATH=/workspaces/agentcon-25-swe-agents/legacy-python

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# The base image already creates the vscode user, so we just need to ensure proper permissions
RUN chown -R $USERNAME:$USERNAME /workspaces
