---
title: "Port Is Already Allocated"
troubleshooting_id: "T04"
category: "troubleshooting"
objective: "Resolve port allocation conflicts when starting Docker containers or network services."
tags: ["port", "allocation", "docker", "networking", "conflicts"]
difficulty: "beginner"
---

# T04: Port Is Already Allocated

## 🔌 Problem Description
**Error Messages:**
- `bind: address already in use`
- `Port 8080 is already allocated`
- `Cannot start container: port is already allocated`
- `listen tcp :8080: bind: address already in use`

**When This Occurs:**
- Starting OTG controller containers
- Running multiple test sessions simultaneously
- After improper container shutdown
- When other applications use the same ports

## 🔍 Root Cause Analysis

### Common Causes
1. **Previous Container Still Running**: OTG controller from previous session not stopped
2. **Port Conflict**: Another application using the same port (8080, 8443, etc.)
3. **Multiple Test Instances**: Trying to run multiple OTG controllers simultaneously
4. **Zombie Processes**: Container stopped but port not released
5. **System Service Conflict**: System service using the same port

## 🛠️ Solution Steps

### Solution 1: Find and Stop Conflicting Processes

#### Linux/macOS
```bash
# Find what's using the port
lsof -i :8080
netstat -tulpn | grep 8080

# Kill the process using the port
sudo kill -9 <PID>

# Or kill by process name
pkill -f "otg-controller"
```

#### Windows
```powershell
# Find what's using the port
netstat -ano | findstr :8080

# Kill the process
taskkill /PID <PID> /F

# Or kill by process name
taskkill /IM "docker.exe" /F
```

### Solution 2: Stop and Remove Docker Containers
```bash
# List all containers (including stopped ones)
docker ps -a

# Stop specific OTG containers
docker stop otg-controller
docker stop $(docker ps -q --filter "ancestor=keysight/otg-controller")

# Remove containers to free up names and resources
docker rm otg-controller
docker rm $(docker ps -aq --filter "ancestor=keysight/otg-controller")

# Nuclear option: stop and remove ALL containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
```

### Solution 3: Use Different Ports
```bash
# Run OTG controller on different port
docker run -d --name otg-controller-alt \
  --network otg-test-net \
  -p 8081:8080 \
  keysight/otg-controller:latest

# Update your client code to use new port
client = OtgClient("http://localhost:8081")
```

### Solution 4: Clean Docker Networks
```bash
# List Docker networks
docker network ls

# Remove specific network
docker network rm otg-test-net

# Remove all unused networks
docker network prune -f

# Recreate clean network
docker network create otg-test-net
```

## 🧪 Verification Steps

### Test 1: Port Availability Check
```bash
# Check if port is free (should return nothing)
lsof -i :8080
netstat -tulpn | grep 8080

# Test port connectivity
telnet localhost 8080
# Should get "Connection refused" if port is free

# Or use nc (netcat)
nc -zv localhost 8080
```

### Test 2: Docker Container Status
```bash
# Verify no OTG containers running
docker ps | grep otg

# Check for stopped containers
docker ps -a | grep otg

# Verify network is clean
docker network inspect otg-test-net
```

### Test 3: Successful Container Start
```bash
# Start container and verify
docker run -d --name otg-controller \
  --network otg-test-net \
  -p 8080:8080 \
  keysight/otg-controller:latest

# Check container is running
docker ps | grep otg-controller

# Test connectivity
curl http://localhost:8080/health
```

## 🐛 Advanced Troubleshooting

### Issue: Port Shows as Used But No Process Found
**Problem:** Port appears allocated but no visible process using it

**Solutions:**
```bash
# Check for Docker proxy processes
ps aux | grep docker-proxy

# Restart Docker daemon (will free all ports)
sudo systemctl restart docker  # Linux
# Or restart Docker Desktop on macOS/Windows

# Check for TIME_WAIT connections
netstat -an | grep 8080 | grep TIME_WAIT

# Wait for TIME_WAIT to clear (usually 60 seconds)
sleep 60
```

### Issue: Multiple Port Conflicts
**Problem:** Several ports are in use, affecting multiple services

**Systematic Approach:**
```bash
# Create port mapping script
#!/bin/bash
# port_mapper.sh - Find available ports

find_available_port() {
    local start_port=$1
    local port=$start_port
    
    while lsof -i :$port >/dev/null 2>&1; do
        port=$((port + 1))
    done
    
    echo $port
}

# Find available ports starting from 8080
API_PORT=$(find_available_port 8080)
GNMI_PORT=$(find_available_port 9090)

echo "Available API port: $API_PORT"
echo "Available gNMI port: $GNMI_PORT"

# Start container with available ports
docker run -d --name otg-controller \
  --network otg-test-net \
  -p $API_PORT:8080 \
  -p $GNMI_PORT:9090 \
  keysight/otg-controller:latest
```

### Issue: Container Starts But Port Not Accessible
**Problem:** Container runs but port binding fails silently

**Diagnostic Steps:**
```bash
# Check container logs
docker logs otg-controller

# Check port binding inside container
docker exec otg-controller netstat -tulpn

# Check Docker port mapping
docker port otg-controller

# Test from inside container
docker exec otg-controller curl http://localhost:8080/health

# Check firewall rules (Linux)
sudo iptables -L -n | grep 8080
sudo ufw status | grep 8080
```

### Issue: Intermittent Port Conflicts
**Problem:** Port conflicts occur sporadically

**Monitoring Solution:**
```bash
#!/bin/bash
# port_monitor.sh - Monitor port usage over time

LOG_FILE="/tmp/port_monitor.log"
PORT=8080

while true; do
    TIMESTAMP=$(date)
    USAGE=$(lsof -i :$PORT 2>/dev/null || echo "PORT_FREE")
    echo "[$TIMESTAMP] Port $PORT: $USAGE" >> $LOG_FILE
    sleep 10
done
```

## 📋 Prevention Strategies

### Proper Container Lifecycle Management
```bash
#!/bin/bash
# otg_session_manager.sh - Proper container lifecycle

start_otg_session() {
    local session_name=${1:-"otg-session-$(date +%s)"}
    
    # Clean up any existing session
    stop_otg_session
    
    # Start fresh container
    docker run -d --name $session_name \
      --network otg-test-net \
      -p 8080:8080 \
      keysight/otg-controller:latest
    
    echo "Started OTG session: $session_name"
}

stop_otg_session() {
    # Stop and remove all OTG containers
    docker stop $(docker ps -q --filter "ancestor=keysight/otg-controller") 2>/dev/null || true
    docker rm $(docker ps -aq --filter "ancestor=keysight/otg-controller") 2>/dev/null || true
    
    echo "Cleaned up OTG sessions"
}

# Usage
# ./otg_session_manager.sh start
# ./otg_session_manager.sh stop
```

### Port Range Management
```python
#!/usr/bin/env python3
"""Port manager for OTG testing"""

import socket
import subprocess
from contextlib import closing

class PortManager:
    def __init__(self, start_port=8080, end_port=8090):
        self.start_port = start_port
        self.end_port = end_port
    
    def is_port_available(self, port):
        """Check if port is available"""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            return result != 0
    
    def find_available_port(self):
        """Find first available port in range"""
        for port in range(self.start_port, self.end_port + 1):
            if self.is_port_available(port):
                return port
        raise RuntimeError(f"No available ports in range {self.start_port}-{self.end_port}")
    
    def start_otg_controller(self):
        """Start OTG controller on available port"""
        port = self.find_available_port()
        
        cmd = [
            "docker", "run", "-d", 
            "--name", f"otg-controller-{port}",
            "--network", "otg-test-net",
            "-p", f"{port}:8080",
            "keysight/otg-controller:latest"
        ]
        
        subprocess.run(cmd, check=True)
        return port

# Usage
if __name__ == "__main__":
    pm = PortManager()
    try:
        port = pm.start_otg_controller()
        print(f"OTG controller started on port {port}")
    except Exception as e:
        print(f"Failed to start OTG controller: {e}")
```

### Automated Cleanup Scripts
```bash
#!/bin/bash
# cleanup_otg.sh - Comprehensive OTG cleanup

echo "=== OTG Environment Cleanup ==="

# Stop all OTG containers
echo "Stopping OTG containers..."
docker stop $(docker ps -q --filter "ancestor=keysight/otg-controller") 2>/dev/null || true
docker stop $(docker ps -q --filter "ancestor=keysight/otg-gnmi") 2>/dev/null || true

# Remove all OTG containers
echo "Removing OTG containers..."
docker rm $(docker ps -aq --filter "ancestor=keysight/otg-controller") 2>/dev/null || true
docker rm $(docker ps -aq --filter "ancestor=keysight/otg-gnmi") 2>/dev/null || true

# Clean up networks
echo "Cleaning up networks..."
docker network rm otg-test-net 2>/dev/null || true
docker network prune -f

# Clean up volumes
echo "Cleaning up volumes..."
docker volume prune -f

# Verify cleanup
echo "Verifying cleanup..."
echo "Running containers:"
docker ps --filter "ancestor=keysight/otg-controller" --filter "ancestor=keysight/otg-gnmi"

echo "Port usage:"
lsof -i :8080 2>/dev/null || echo "Port 8080 is free"
lsof -i :8443 2>/dev/null || echo "Port 8443 is free"

echo "=== Cleanup Complete ==="
```

## 🔧 Configuration Best Practices

### Dynamic Port Assignment
```python
# In your test scripts, use dynamic port discovery
import socket
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

# Use in container startup
free_port = find_free_port()
client = OtgClient(f"http://localhost:{free_port}")
```

### Container Naming Strategy
```bash
# Use unique container names to avoid conflicts
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="otg-controller-$TIMESTAMP"

docker run -d --name $CONTAINER_NAME \
  --network otg-test-net \
  -p 8080:8080 \
  keysight/otg-controller:latest
```

## 📞 Getting Help

### Information to Collect
When reporting port allocation issues:

```bash
# Port usage information
lsof -i :8080
netstat -tulpn | grep 8080

# Docker container status
docker ps -a
docker network ls

# System information
ps aux | grep docker
systemctl status docker  # Linux

# Log information
docker logs otg-controller 2>&1
journalctl -u docker.service --no-pager  # Linux
```

### Support Resources
1. **Docker Documentation**: Container networking and port management
2. **OTG GitHub Issues**: Port-specific problems
3. **System Administration Forums**: OS-specific networking issues
4. **Stack Overflow**: Programming and scripting solutions

---

**Remember**: Port conflicts are common in development environments. Always clean up containers properly after testing, and consider using dynamic port allocation for more robust testing setups.
