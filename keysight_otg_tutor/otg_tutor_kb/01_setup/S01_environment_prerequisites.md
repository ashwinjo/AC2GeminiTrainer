---
title: "Environment Prerequisites"
setup_id: "S01"
category: "setup"
objective: "Set up all required software, tools, and system configurations needed for OTG development and testing."
tags: ["prerequisites", "docker", "python", "setup", "environment"]
difficulty: "beginner"
---

# S01: Environment Prerequisites

## 🎯 Overview
This guide outlines all the prerequisites needed to set up a complete OTG development and testing environment. Following these requirements ensures smooth operation of all labs and exercises.

## 💻 System Requirements

### Minimum Hardware Requirements
| Component | Minimum | Recommended | High-Performance |
|-----------|---------|-------------|------------------|
| **CPU** | 2 cores, 2.0 GHz | 4 cores, 2.5 GHz | 8+ cores, 3.0+ GHz |
| **RAM** | 4 GB | 8 GB | 16+ GB |
| **Storage** | 20 GB free | 50 GB free | 100+ GB SSD |
| **Network** | 1 Gbps NIC | 10 Gbps NIC | 25+ Gbps NIC |

### Supported Operating Systems
- **Linux**: Ubuntu 20.04+, CentOS 8+, RHEL 8+, Debian 11+
- **macOS**: macOS 11.0+ (Big Sur or newer)
- **Windows**: Windows 10 Pro/Enterprise, Windows 11, Windows Server 2019+

## 🐳 Docker Requirements

### Docker Installation
**Linux (Ubuntu/Debian):**
```bash
# Update package index
sudo apt update

# Install Docker
sudo apt install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
docker-compose --version
```

**macOS:**
```bash
# Install Docker Desktop
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
# Start Docker Desktop from Applications
```

**Windows:**
```powershell
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Or use Chocolatey
choco install docker-desktop

# Or use winget
winget install Docker.DockerDesktop
```

### Docker Configuration
**Memory and CPU Allocation:**
- **Minimum**: 2 GB RAM, 2 CPU cores
- **Recommended**: 4 GB RAM, 4 CPU cores
- **High-Performance**: 8+ GB RAM, 8+ CPU cores

**Docker Daemon Settings (Linux):**
```json
# /etc/docker/daemon.json
{
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-address-pools": [
    {
      "base": "172.17.0.0/16",
      "size": 24
    }
  ]
}
```

## 🐍 Python Requirements

### Python Version
- **Required**: Python 3.8 or higher
- **Recommended**: Python 3.9 or 3.10
- **Latest**: Python 3.11+ (for best performance)

### Python Installation
**Linux (Ubuntu/Debian):**
```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.10

# Or use system Python (macOS 12.3+)
python3 --version

# Install pip if needed
curl https://bootstrap.pypa.io/get-pip.py | python3
```

**Windows:**
```powershell
# Download from python.org
# Or use Microsoft Store
# Or use Chocolatey
choco install python

# Or use winget
winget install Python.Python.3.10

# Verify installation
python --version
pip --version
```

### Virtual Environment Setup
```bash
# Create virtual environment
python3 -m venv otg-env

# Activate virtual environment
# Linux/macOS:
source otg-env/bin/activate

# Windows:
otg-env\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install common packages
pip install requests websocket-client pyyaml
```

## 📦 Required Python Packages

### Core OTG Packages
```bash
# Install OTG client
pip install otg-client

# Install additional OTG tools
pip install snappi
pip install ixnetwork-restpy  # For IxNetwork integration
```

### Development and Testing Packages
```bash
# Testing frameworks
pip install pytest pytest-asyncio

# HTTP clients
pip install requests aiohttp

# Data handling
pip install pandas numpy

# Configuration management
pip install pyyaml python-dotenv

# Logging and monitoring
pip install structlog prometheus-client

# Development tools
pip install black flake8 mypy
```

### Complete Requirements File
```txt
# requirements.txt - Complete OTG development environment

# Core OTG packages
otg-client>=1.0.0
snappi>=0.11.0

# HTTP and networking
requests>=2.28.0
aiohttp>=3.8.0
websocket-client>=1.4.0

# Data handling and analysis
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0

# Configuration and environment
pyyaml>=6.0
python-dotenv>=0.20.0

# Testing frameworks
pytest>=7.2.0
pytest-asyncio>=0.20.0
pytest-cov>=4.0.0

# Development tools
black>=22.0.0
flake8>=5.0.0
mypy>=0.991

# Logging and monitoring
structlog>=22.3.0
prometheus-client>=0.15.0

# Documentation
sphinx>=5.3.0
sphinx-rtd-theme>=1.1.0

# Optional: Jupyter for interactive development
jupyter>=1.0.0
ipython>=8.0.0
```

## 🌐 Network Configuration

### Port Requirements
**Default Ports Used:**
- **8080**: OTG API endpoint (HTTP)
- **8443**: OTG API endpoint (HTTPS)
- **9090**: gNMI interface
- **40051**: gRPC services
- **6633**: OpenFlow controller (if used)

**Firewall Configuration (Linux):**
```bash
# Using ufw
sudo ufw allow 8080/tcp
sudo ufw allow 8443/tcp
sudo ufw allow 9090/tcp

# Using iptables
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9090 -j ACCEPT
```

### Network Interface Requirements
**Virtual Interfaces (for testing):**
```bash
# Create virtual ethernet pairs
sudo ip link add veth0 type veth peer name veth1
sudo ip link add veth2 type veth peer name veth3
sudo ip link set veth0 up
sudo ip link set veth1 up
sudo ip link set veth2 up
sudo ip link set veth3 up

# Verify interfaces
ip link show | grep veth
```

**Docker Network Setup:**
```bash
# Create dedicated network for OTG testing
docker network create otg-test-net --subnet=172.20.0.0/16

# Verify network
docker network ls | grep otg
docker network inspect otg-test-net
```

## 🔧 Development Tools

### Code Editors and IDEs
**Recommended Options:**
1. **Visual Studio Code** with Python extension
2. **PyCharm** (Community or Professional)
3. **Vim/Neovim** with Python plugins
4. **Sublime Text** with Python packages

**VS Code Extensions:**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-vscode.docker",
    "redhat.vscode-yaml",
    "ms-toolsai.jupyter"
  ]
}
```

### Git Configuration
```bash
# Install Git (if not already installed)
# Linux: sudo apt install git
# macOS: brew install git
# Windows: winget install Git.Git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Optional Development Tools
```bash
# Docker Compose (for multi-container setups)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Kubernetes (for advanced deployments)
# Install kubectl, minikube, or kind

# Network analysis tools
sudo apt install tcpdump wireshark-qt  # Linux
brew install tcpdump wireshark  # macOS

# Performance monitoring
sudo apt install htop iotop nethogs  # Linux
brew install htop  # macOS
```

## 🧪 Environment Verification

### Verification Script
```bash
#!/bin/bash
# verify_environment.sh - Complete environment verification

echo "=== OTG Environment Verification ==="

# Check Python
echo "Checking Python..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }
pip3 --version || { echo "❌ pip not found"; exit 1; }
echo "✅ Python OK"

# Check Docker
echo "Checking Docker..."
docker --version || { echo "❌ Docker not found"; exit 1; }
docker info >/dev/null 2>&1 || { echo "❌ Docker daemon not running"; exit 1; }
echo "✅ Docker OK"

# Check Python packages
echo "Checking Python packages..."
python3 -c "import otg_client; print('✅ otg-client OK')" || echo "❌ otg-client not found"
python3 -c "import requests; print('✅ requests OK')" || echo "❌ requests not found"
python3 -c "import yaml; print('✅ pyyaml OK')" || echo "❌ pyyaml not found"

# Check network connectivity
echo "Checking network..."
ping -c 1 google.com >/dev/null 2>&1 && echo "✅ Internet connectivity OK" || echo "❌ No internet"

# Check ports
echo "Checking ports..."
netstat -tuln | grep :8080 >/dev/null && echo "⚠️  Port 8080 in use" || echo "✅ Port 8080 available"

# Check virtual interfaces (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Checking virtual interfaces..."
    ip link show | grep veth >/dev/null && echo "✅ Virtual interfaces OK" || echo "⚠️  No virtual interfaces"
fi

echo "=== Verification Complete ==="
```

### Python Environment Test
```python
#!/usr/bin/env python3
"""test_environment.py - Python environment verification"""

import sys
import importlib.util

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is too old (need 3.8+)")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def check_package(package_name):
    """Check if package is available"""
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ {package_name} not found")
        return False
    print(f"✅ {package_name} OK")
    return True

def main():
    print("=== Python Environment Test ===")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check required packages
    required_packages = [
        'otg_client',
        'requests', 
        'yaml',
        'json',
        'asyncio'
    ]
    
    all_good = True
    for package in required_packages:
        if not check_package(package):
            all_good = False
    
    if all_good:
        print("✅ All Python requirements satisfied")
        
        # Test OTG client import
        try:
            from otg_client import OtgClient
            print("✅ OTG client can be imported")
        except ImportError as e:
            print(f"❌ OTG client import failed: {e}")
            all_good = False
    
    if not all_good:
        print("\n📋 To fix missing packages:")
        print("pip install otg-client requests pyyaml")
        sys.exit(1)
    
    print("=== All tests passed! ===")

if __name__ == "__main__":
    main()
```

## 🚀 Quick Setup Script

### Automated Setup (Linux/macOS)
```bash
#!/bin/bash
# setup_otg_environment.sh - Automated OTG environment setup

set -e

echo "🚀 Setting up OTG development environment..."

# Update system packages
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python@3.10 docker
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv otg-env
source otg-env/bin/activate

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install otg-client requests pyyaml pytest black flake8

# Create virtual network interfaces (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Creating virtual network interfaces..."
    sudo ip link add veth0 type veth peer name veth1 2>/dev/null || true
    sudo ip link add veth2 type veth peer name veth3 2>/dev/null || true
    sudo ip link set veth0 up 2>/dev/null || true
    sudo ip link set veth1 up 2>/dev/null || true
    sudo ip link set veth2 up 2>/dev/null || true
    sudo ip link set veth3 up 2>/dev/null || true
fi

# Create Docker network
echo "Creating Docker network..."
docker network create otg-test-net --subnet=172.20.0.0/16 2>/dev/null || true

# Verify setup
echo "Verifying setup..."
python3 -c "import otg_client; print('✅ OTG client installed')"
docker --version
docker network ls | grep otg-test-net

echo "✅ Setup complete!"
echo ""
echo "To activate the environment:"
echo "source otg-env/bin/activate"
echo ""
echo "To test the setup:"
echo "python3 test_environment.py"
```

## 🔍 Troubleshooting Common Issues

### Permission Issues (Linux)
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker  # Or logout/login

# Fix Python package permissions
pip install --user otg-client  # Install for user only
```

### Port Conflicts
```bash
# Find processes using ports
lsof -i :8080
sudo kill -9 <PID>

# Use different ports
docker run -p 8081:8080 keysight/otg-controller
```

### Network Interface Issues
```bash
# Reset network interfaces
sudo ip link delete veth0 2>/dev/null || true
sudo ip link add veth0 type veth peer name veth1
sudo ip link set veth0 up
sudo ip link set veth1 up
```

## 📚 Next Steps

After completing the prerequisites:

1. **Verify Installation**: Run the verification scripts
2. **Clone Repository**: Proceed to S02_cloning_the_repo.md
3. **Start Learning**: Begin with Lab 01 exercises
4. **Join Community**: Connect with other OTG users

---

**🎯 Key Points:**
- Ensure all prerequisites are met before starting labs
- Use virtual environments for Python development
- Verify setup with provided test scripts
- Keep Docker and Python packages updated
- Join the OTG community for support and updates

Your environment is now ready for OTG development and testing! 🌟
