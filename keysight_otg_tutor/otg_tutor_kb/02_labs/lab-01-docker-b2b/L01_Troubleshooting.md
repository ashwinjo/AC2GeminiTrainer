---
title: "Lab 1 Troubleshooting Guide"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Diagnose and resolve common issues encountered during Lab 1 Docker back-to-back testing setup and execution."
tags: ["troubleshooting", "debugging", "docker", "networking", "solutions"]
difficulty: "intermediate"
---

# Lab 01: Troubleshooting Guide

## Common Issues and Solutions

### 🐳 Docker-Related Issues

#### Issue: Docker daemon not running
**Symptoms:**
- `docker: Cannot connect to the Docker daemon`
- `docker ps` fails with connection error

**Solutions:**
```bash
# On Linux
sudo systemctl start docker
sudo systemctl enable docker

# On macOS
# Start Docker Desktop application

# On Windows
# Start Docker Desktop application

# Verify Docker is running
docker --version
docker info
```

#### Issue: Port 8080 already in use
**Symptoms:**
- `bind: address already in use`
- Container fails to start

**Solutions:**
```bash
# Find what's using the port
lsof -i :8080
netstat -tulpn | grep 8080

# Kill the process or use different port
docker run -d --name otg-controller \
  --network otg-test-net \
  -p 8081:8080 \
  keysight/otg-controller:latest

# Update your client connection
client = OtgClient("http://localhost:8081")
```

#### Issue: Docker network creation fails
**Symptoms:**
- `network with name otg-test-net already exists`
- Network connectivity issues

**Solutions:**
```bash
# Remove existing network
docker network rm otg-test-net

# Or use existing network
docker network ls
docker network inspect otg-test-net

# Create with different name
docker network create otg-test-net-v2
```

### 🐍 Python-Related Issues

#### Issue: Module 'otg_client' not found
**Symptoms:**
- `ModuleNotFoundError: No module named 'otg_client'`
- Import errors in Python script

**Solutions:**
```bash
# Install the OTG client
pip install otg-client

# If using virtual environment
python -m venv otg-env
source otg-env/bin/activate  # Linux/macOS
# or
otg-env\Scripts\activate     # Windows
pip install otg-client

# Verify installation
python -c "import otg_client; print('Success!')"
```

#### Issue: Python version compatibility
**Symptoms:**
- Syntax errors with f-strings
- Import errors with type hints

**Solutions:**
```bash
# Check Python version (need 3.8+)
python --version

# Use appropriate Python version
python3.8 lab-01_test.py
# or
python3.9 lab-01_test.py

# Update Python if needed
# Linux: sudo apt update && sudo apt install python3.9
# macOS: brew install python@3.9
# Windows: Download from python.org
```

### 🌐 Network Connectivity Issues

#### Issue: Connection refused to OTG controller
**Symptoms:**
- `requests.exceptions.ConnectionError`
- `Connection refused` errors

**Solutions:**
```bash
# Check container status
docker ps -a | grep otg-controller

# Check container logs
docker logs otg-controller

# Test connectivity
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/config

# Restart container if needed
docker restart otg-controller

# Wait for startup (can take 30-60 seconds)
sleep 30
```

#### Issue: Virtual interface creation fails
**Symptoms:**
- Port configuration errors
- Interface not found errors

**Solutions:**
```bash
# Create virtual interfaces manually
sudo ip link add veth0 type veth peer name veth1
sudo ip link set veth0 up
sudo ip link set veth1 up

# Verify interfaces exist
ip link show | grep veth

# Alternative: Use Docker's built-in networking
# Modify config to use container networking instead
```

### 📊 Traffic and Statistics Issues

#### Issue: No traffic statistics
**Symptoms:**
- All counters show zero
- Statistics API returns empty data

**Solutions:**
```python
# Add delays for proper timing
import time

# Wait after starting traffic
client.start_traffic()
time.sleep(5)  # Allow traffic to ramp up

# Check flow configuration
print("Flow config:", flow.to_dict())

# Verify endpoints are correct
print("TX device:", flow.tx.device)
print("RX device:", flow.rx.device)
```

#### Issue: High packet loss in B2B setup
**Symptoms:**
- Significant packet loss (>1%)
- Inconsistent statistics

**Solutions:**
```python
# Reduce traffic rate
flow.rate.pps = 100  # Start with lower rate

# Increase packet buffer time
time.sleep(2)  # Between start and statistics collection

# Check system resources
# Monitor CPU/memory usage during test

# Use smaller packet counts for testing
flow.duration.packets = 1000  # Smaller test size
```

#### Issue: Statistics don't update in real-time
**Symptoms:**
- Stale statistics values
- Delayed updates

**Solutions:**
```python
# Increase polling interval
def monitor_traffic(client, duration=30):
    start_time = time.time()
    while time.time() - start_time < duration:
        stats = get_statistics(client)
        display_realtime_stats(stats)
        time.sleep(5)  # Increase from 2 to 5 seconds

# Force statistics refresh
client.clear_statistics()
time.sleep(1)
stats = client.get_metrics()
```

### 🔧 Configuration Issues

#### Issue: Invalid configuration errors
**Symptoms:**
- `400 Bad Request` when setting config
- Configuration validation failures

**Solutions:**
```python
# Validate configuration before applying
try:
    config_dict = config.to_dict()
    print("Config validation:", json.dumps(config_dict, indent=2))
except Exception as e:
    print(f"Config error: {e}")

# Check required fields
assert config.devices, "No devices configured"
assert config.flows, "No flows configured"
assert len(config.devices) >= 2, "Need at least 2 devices"

# Verify port locations exist
for device in config.devices:
    for port in device.ports:
        print(f"Port location: {port.location}")
```

#### Issue: Flow configuration problems
**Symptoms:**
- Traffic doesn't start
- Flow validation errors

**Solutions:**
```python
# Ensure proper flow setup
flow = Flow(name="test_flow")

# Set all required parameters
flow.tx = FlowTx(device="device_a", port="port_a")
flow.rx = FlowRx(device="device_b", port="port_b")

# Set traffic parameters
flow.rate = FlowRate(pps=1000)
flow.size = FlowSize(fixed=64)
flow.duration = FlowDuration(packets=10000)

# Validate flow before adding to config
print("Flow validation:", flow.to_dict())
```

## 🚨 Emergency Troubleshooting

### Complete Reset Procedure
If everything fails, try this complete reset:

```bash
# 1. Stop and remove all containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# 2. Remove networks
docker network prune -f

# 3. Clean up Docker system
docker system prune -f

# 4. Restart Docker service
# Linux: sudo systemctl restart docker
# macOS/Windows: Restart Docker Desktop

# 5. Start fresh
docker network create otg-test-net
docker run -d --name otg-controller \
  --network otg-test-net \
  -p 8080:8080 \
  keysight/otg-controller:latest

# 6. Wait for startup
sleep 60

# 7. Test connectivity
curl http://localhost:8080/health
```

### Debug Mode Script
Use this enhanced version for debugging:

```python
#!/usr/bin/env python3
"""Debug version of lab-01_test.py with extensive logging"""

import logging
import time
import json
from otg_client import OtgClient

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_main():
    """Debug version with extensive logging"""
    
    logger.info("=== DEBUG MODE ENABLED ===")
    
    # Test connectivity first
    logger.info("Testing connectivity...")
    try:
        import requests
        response = requests.get("http://localhost:8080/health", timeout=5)
        logger.info(f"Health check: {response.status_code}")
    except Exception as e:
        logger.error(f"Connectivity test failed: {e}")
        return
    
    # Initialize client with debug
    logger.info("Initializing OTG client...")
    client = OtgClient("http://localhost:8080", debug=True)
    
    # Continue with rest of test...
    # [Include full debug version of your test]

if __name__ == "__main__":
    debug_main()
```

## 📞 Getting Additional Help

### Log Collection
When reporting issues, collect these logs:

```bash
# Docker logs
docker logs otg-controller > otg-controller.log

# System information
docker info > docker-info.log
docker version > docker-version.log

# Network information
docker network ls > networks.log
ip addr show > interfaces.log

# Python environment
pip list > python-packages.log
python --version > python-version.log
```

### Support Channels
1. **Check FAQ first**: Many issues are covered there
2. **GitHub Issues**: For code-related problems
3. **Community Forums**: For general questions
4. **Documentation**: Official OTG documentation
5. **Keysight Support**: For critical issues

---

*Remember: Most issues are environment-related. Start with the basics: Docker running, ports available, Python environment correct.*
