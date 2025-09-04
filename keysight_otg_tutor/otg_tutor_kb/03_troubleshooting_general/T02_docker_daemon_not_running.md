# T02: Docker Daemon Not Running

## 🐳 Problem Description
**Error Messages:**
- `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`
- `docker: Cannot connect to the Docker daemon. Is the docker daemon running?`
- `Got permission denied while trying to connect to the Docker daemon socket`
- `docker: command not found`

**When This Occurs:**
- Starting OTG containers for testing
- Running docker commands from command line
- First-time Docker setup or after system restart
- After Docker installation or updates

## 🔍 Root Cause Analysis

### Common Causes
1. **Docker Service Not Started**: Docker daemon is not running
2. **Permission Issues**: User not in docker group
3. **Docker Not Installed**: Docker engine not installed on system
4. **Socket Permission Problems**: Docker socket has incorrect permissions
5. **System Resource Issues**: Insufficient resources to start Docker
6. **Configuration Problems**: Docker daemon configuration errors

## 🛠️ Solution Steps by Operating System

### 🐧 Linux Solutions

#### Solution 1: Start Docker Service
```bash
# Check Docker service status
sudo systemctl status docker

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Verify Docker is running
docker --version
docker info
```

#### Solution 2: Fix User Permissions
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes (logout/login or use newgrp)
newgrp docker

# Verify group membership
groups $USER

# Test Docker without sudo
docker run hello-world
```

#### Solution 3: Install Docker (if missing)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# CentOS/RHEL/Fedora
sudo yum install docker docker-compose
# or
sudo dnf install docker docker-compose

# Start and enable service
sudo systemctl start docker
sudo systemctl enable docker
```

#### Solution 4: Fix Socket Permissions
```bash
# Check socket permissions
ls -la /var/run/docker.sock

# Fix socket permissions (temporary)
sudo chmod 666 /var/run/docker.sock

# Better solution: ensure user is in docker group (see Solution 2)
```

### 🍎 macOS Solutions

#### Solution 1: Start Docker Desktop
```bash
# Check if Docker Desktop is running
docker --version

# Start Docker Desktop application
open -a Docker

# Or start from Applications folder
# Applications > Docker > Docker Desktop

# Wait for Docker to start (check system tray)
# Verify with:
docker info
```

#### Solution 2: Install Docker Desktop (if missing)
```bash
# Download from official website
# https://www.docker.com/products/docker-desktop

# Or install using Homebrew
brew install --cask docker

# Start Docker Desktop after installation
open -a Docker
```

#### Solution 3: Restart Docker Desktop
```bash
# Quit Docker Desktop
osascript -e 'quit app "Docker"'

# Wait a few seconds, then restart
sleep 5
open -a Docker

# Or restart from Docker Desktop menu
# Docker Desktop > Restart
```

### 🪟 Windows Solutions

#### Solution 1: Start Docker Desktop
```powershell
# Check Docker status
docker --version

# Start Docker Desktop from Start Menu
# Or run from PowerShell
Start-Process "Docker Desktop"

# Wait for Docker to start and verify
docker info
```

#### Solution 2: Install Docker Desktop (if missing)
```powershell
# Download from official website
# https://www.docker.com/products/docker-desktop

# Or install using Chocolatey
choco install docker-desktop

# Or using winget
winget install Docker.DockerDesktop
```

#### Solution 3: Enable Windows Features
```powershell
# Enable Hyper-V and Containers (run as Administrator)
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
Enable-WindowsOptionalFeature -Online -FeatureName Containers -All

# Restart computer after enabling features
Restart-Computer
```

## 🧪 Verification Steps

### Test 1: Basic Docker Functionality
```bash
# Check Docker version
docker --version

# Check Docker system information
docker info

# Test with hello-world container
docker run hello-world

# List running containers
docker ps

# List all containers
docker ps -a
```

### Test 2: OTG-Specific Docker Test
```bash
# Test Docker networking (required for OTG)
docker network create test-network
docker network ls | grep test-network
docker network rm test-network

# Test port binding (required for OTG controller)
docker run -d --name test-nginx -p 8080:80 nginx:alpine
curl http://localhost:8080
docker stop test-nginx
docker rm test-nginx
```

### Test 3: Resource Availability
```bash
# Check Docker system resource usage
docker system df

# Check available disk space
df -h

# Check memory usage
free -h  # Linux
top -l 1 | head -10  # macOS
```

## 🐛 Advanced Troubleshooting

### Issue: Docker Service Fails to Start (Linux)
**Problem:** Docker daemon fails to start with errors

**Diagnostic Steps:**
```bash
# Check detailed service status
sudo systemctl status docker -l

# Check Docker daemon logs
sudo journalctl -u docker.service -f

# Check for configuration errors
sudo dockerd --debug

# Check for conflicting processes
sudo lsof -i :2375
sudo lsof -i :2376
```

**Common Solutions:**
```bash
# Reset Docker daemon configuration
sudo systemctl stop docker
sudo rm -rf /var/lib/docker/tmp
sudo systemctl start docker

# Reconfigure Docker daemon
sudo nano /etc/docker/daemon.json
# Add: {"storage-driver": "overlay2"}
sudo systemctl restart docker
```

### Issue: Permission Denied After Adding to Docker Group
**Problem:** Still getting permission errors after adding user to docker group

**Solutions:**
```bash
# Verify group membership
id $USER
groups $USER

# Force group refresh (without logout)
newgrp docker

# Or logout and login again
# Or restart terminal session

# Verify Docker socket ownership
ls -la /var/run/docker.sock
# Should show: srw-rw---- 1 root docker
```

### Issue: Docker Desktop Won't Start (macOS/Windows)
**Problem:** Docker Desktop application fails to launch

**macOS Solutions:**
```bash
# Check system requirements
sw_vers  # macOS version
sysctl -n hw.ncpu  # CPU cores
sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}'  # RAM

# Reset Docker Desktop
rm -rf ~/Library/Group\ Containers/group.com.docker
rm -rf ~/Library/Containers/com.docker.docker
open -a Docker

# Check Console app for error messages
open -a Console
```

**Windows Solutions:**
```powershell
# Check Windows version and features
Get-ComputerInfo | Select WindowsProductName, WindowsVersion

# Check Hyper-V status
Get-WindowsOptionalFeature -FeatureName Microsoft-Hyper-V-All -Online

# Reset Docker Desktop
Get-Process "*docker*" | Stop-Process -Force
Remove-Item -Path "$env:APPDATA\Docker" -Recurse -Force
Start-Process "Docker Desktop"
```

### Issue: Resource Exhaustion
**Problem:** System runs out of resources for Docker

**Solutions:**
```bash
# Clean up Docker resources
docker system prune -a -f
docker volume prune -f
docker network prune -f

# Check disk usage
docker system df

# Configure Docker resource limits
# Edit Docker Desktop settings or daemon.json
```

## 📋 Prevention Strategies

### Automated Startup Scripts

#### Linux Systemd Service Check
```bash
#!/bin/bash
# check_docker.sh - Ensure Docker is running

if ! systemctl is-active --quiet docker; then
    echo "Starting Docker service..."
    sudo systemctl start docker
    sleep 5
fi

if ! docker info >/dev/null 2>&1; then
    echo "Docker is not responding. Check configuration."
    exit 1
fi

echo "Docker is running and ready."
```

#### macOS/Windows Startup Check
```bash
#!/bin/bash
# check_docker_desktop.sh - Ensure Docker Desktop is running

max_wait=60
count=0

while ! docker info >/dev/null 2>&1; do
    if [ $count -eq 0 ]; then
        echo "Starting Docker Desktop..."
        open -a Docker  # macOS
        # Start-Process "Docker Desktop"  # Windows PowerShell
    fi
    
    echo "Waiting for Docker to start... ($count/$max_wait)"
    sleep 5
    count=$((count + 5))
    
    if [ $count -ge $max_wait ]; then
        echo "Docker failed to start within $max_wait seconds"
        exit 1
    fi
done

echo "Docker is running and ready."
```

### Health Check Script
```bash
#!/bin/bash
# docker_health_check.sh - Comprehensive Docker health check

echo "=== Docker Health Check ==="

# Check if Docker command exists
if ! command -v docker &> /dev/null; then
    echo "❌ Docker command not found. Install Docker first."
    exit 1
fi

# Check Docker daemon
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon not running or not accessible."
    echo "Try: sudo systemctl start docker (Linux)"
    echo "Or start Docker Desktop (macOS/Windows)"
    exit 1
fi

# Check Docker version
echo "✅ Docker version: $(docker --version)"

# Check system resources
echo "📊 Docker system info:"
docker system df

# Test basic functionality
echo "🧪 Testing Docker functionality..."
if docker run --rm hello-world >/dev/null 2>&1; then
    echo "✅ Docker is working correctly"
else
    echo "❌ Docker test failed"
    exit 1
fi

echo "=== All checks passed! ==="
```

## 🔧 Configuration Optimization

### Docker Daemon Configuration
Create `/etc/docker/daemon.json` (Linux) or configure via Docker Desktop:

```json
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

### Resource Limits (Docker Desktop)
- **Memory**: Allocate sufficient RAM (4GB minimum for OTG)
- **CPU**: Allocate multiple cores for better performance
- **Disk**: Ensure adequate disk space for images and containers

## 📞 Getting Help

### Information to Collect
When seeking help, provide:

```bash
# System information
uname -a  # Linux/macOS
Get-ComputerInfo  # Windows

# Docker information
docker --version
docker info
docker system df

# Service status (Linux)
sudo systemctl status docker
sudo journalctl -u docker.service --no-pager

# Process information
ps aux | grep docker
netstat -tulpn | grep docker
```

### Support Resources
1. **Docker Documentation**: Official installation and troubleshooting guides
2. **Docker Community Forums**: Community support and discussions
3. **GitHub Issues**: Docker and OTG-specific issues
4. **System-specific Forums**: OS-specific Docker problems

---

**Remember**: Docker daemon issues are usually related to service management, permissions, or system resources. Most problems can be resolved by ensuring the Docker service is running and the user has proper permissions.
