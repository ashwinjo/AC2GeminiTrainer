---
title: "Lab 2 Troubleshooting Guide"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Diagnose and resolve issues with protocol engines, BGP sessions, and advanced OTG testing scenarios."
tags: ["troubleshooting", "debugging", "protocol", "bgp", "sessions"]
difficulty: "intermediate"
---

# Lab 02: Troubleshooting Guide - Protocol Engine Issues

## Common Issues and Solutions

### 🔧 Protocol Engine Issues

#### Issue: Protocol engine containers won't start
**Symptoms:**
- Container exits immediately after start
- "Protocol engine failed to initialize" errors
- Port binding conflicts

**Solutions:**
```bash
# Check for port conflicts
lsof -i :5555
lsof -i :5556

# Use different ports if needed
docker run -d --name protocol-engine-1 --network=host \
  -e OPT_LISTEN_PORT=5557 \
  ghcr.io/open-traffic-generator/ixia-c-protocol-engine:1.8.0.99

# Check container logs for detailed errors
docker logs protocol-engine-1
```

#### Issue: Protocol engines running but not responding
**Symptoms:**
- Containers show as running but API calls fail
- Connection timeout errors
- Protocol configuration fails

**Solutions:**
```bash
# Test protocol engine connectivity
curl -v http://localhost:5555/health
curl -v http://localhost:5556/health

# Check resource usage
docker stats protocol-engine-1 protocol-engine-2

# Restart protocol engines if unresponsive
docker restart protocol-engine-1 protocol-engine-2
```

### 🌐 BGP Session Issues

#### Issue: BGP sessions stuck in "Active" state
**Symptoms:**
- Sessions never reach "Established" state
- Continuous connection attempts
- No route exchange

**Diagnostic Steps:**
```bash
# Check BGP session states
curl -k https://localhost:8443/api/v1/results/metrics | jq '.protocol_metrics.bgp'

# Verify BGP configuration
curl -k https://localhost:8443/api/v1/config | jq '.devices[].protocols.bgp'

# Check protocol engine logs
docker logs protocol-engine-1 | grep -i bgp
docker logs protocol-engine-2 | grep -i bgp
```

**Common Solutions:**
```python
# Fix AS number mismatch
device1_bgp.as_number = 65001  # Must match peer configuration
device2_bgp.as_number = 65002  # Must be different from device1

# Fix router ID conflicts
device1_bgp.router_id = "192.168.1.1"  # Must be unique
device2_bgp.router_id = "192.168.1.2"  # Must be unique

# Adjust BGP timers for faster convergence
bgp_peer.hold_time = 90
bgp_peer.keepalive_interval = 30
```

#### Issue: BGP sessions establish but no routes learned
**Symptoms:**
- BGP state shows "Established"
- Route counters show 0 advertised/received
- Traffic fails due to no routes

**Solutions:**
```python
# Verify route advertisement configuration
bgp_routes = device1_bgp.ipv4_routes.add()
bgp_routes.name = "routes_v4"
bgp_routes.addresses.add(address="10.0.0.1", prefix=24, count=1000, step=256)

# Check route policies
# Ensure no route filtering is blocking advertisements
bgp_peer.route_range_name = "routes_v4"

# Monitor route learning
curl -k https://localhost:8443/api/v1/results/metrics | \
  jq '.protocol_metrics.bgp[] | {name: .name, routes_advertised: .routes_advertised, routes_received: .routes_received}'
```

### 📊 Protocol Convergence Issues

#### Issue: Slow BGP convergence
**Symptoms:**
- BGP sessions take >2 minutes to establish
- Route learning is very slow
- Traffic startup delayed

**Optimization Solutions:**
```python
# Reduce BGP timers
bgp_peer.hold_time = 60          # Default: 180
bgp_peer.keepalive_interval = 20  # Default: 60

# Limit initial route advertisements
bgp_routes.addresses[0].count = 100  # Start small, increase gradually

# Increase container resources
# Add to docker run command:
# --memory=2g --cpus=2
```

#### Issue: Protocol sessions flapping
**Symptoms:**
- BGP sessions repeatedly go up/down
- Inconsistent route learning
- High CPU usage in protocol engines

**Solutions:**
```bash
# Check system resources
docker stats --no-stream

# Monitor protocol engine stability
watch -n 5 'curl -s -k https://localhost:8443/api/v1/results/metrics | jq ".protocol_metrics.bgp[].session_state"'

# Increase hold time to prevent flapping
bgp_peer.hold_time = 300  # More conservative timer
```

### 🚦 Traffic Flow Issues with Protocols

#### Issue: Traffic not flowing through established routes
**Symptoms:**
- BGP sessions established and routes learned
- Traffic counters show 0 packets
- No errors in logs

**Diagnostic Steps:**
```bash
# Verify route installation
curl -k https://localhost:8443/api/v1/results/metrics | \
  jq '.protocol_metrics.bgp[].routes_received'

# Check traffic configuration
curl -k https://localhost:8443/api/v1/config | jq '.flows'

# Verify traffic engine connectivity
docker logs traffic-engine-1 | grep -i error
docker logs traffic-engine-2 | grep -i error
```

**Solutions:**
```python
# Ensure traffic uses protocol-learned routes
flow.packet.ethernet().ipv4().src = "10.0.0.1"    # Must match advertised routes
flow.packet.ethernet().ipv4().dst = "20.0.0.1"    # Must match learned routes

# Verify traffic engines are associated with protocol engines
device1.container_name = "traffic-engine-1"
device1.protocol_container_name = "protocol-engine-1"  # Important!
```

### 🔄 Integration Issues

#### Issue: Protocol engines and traffic engines not communicating
**Symptoms:**
- Protocols establish but traffic doesn't use learned routes
- API shows disconnected engines
- Configuration applies but no traffic flows

**Solutions:**
```bash
# Check container networking
docker network inspect bridge

# Verify all containers are on same network
docker inspect controller traffic-engine-1 traffic-engine-2 protocol-engine-1 protocol-engine-2 | \
  grep -A 5 "NetworkMode"

# Restart containers in proper order
docker restart controller
sleep 10
docker restart traffic-engine-1 traffic-engine-2
sleep 10  
docker restart protocol-engine-1 protocol-engine-2
```

## 🚨 Emergency Troubleshooting

### Complete Protocol Reset Procedure
If all else fails, try this complete reset:

```bash
# 1. Gracefully terminate protocol sessions
curl -k -X POST https://localhost:8443/api/v1/control/protocols/stop

# 2. Stop all containers
docker stop protocol-engine-1 protocol-engine-2 traffic-engine-1 traffic-engine-2 controller

# 3. Remove containers
docker rm protocol-engine-1 protocol-engine-2 traffic-engine-1 traffic-engine-2 controller

# 4. Clean protocol state
sudo rm -rf /tmp/bgp_* /tmp/protocol_* 2>/dev/null || true

# 5. Recreate virtual interfaces
sudo ip link delete veth0 2>/dev/null || true
sudo ip link add name veth0 type veth peer name veth1
sudo ip link set dev veth0 up
sudo ip link set dev veth1 up

# 6. Restart all containers
# Follow L02_Lab_Configuration.md steps 3-5
```

### Debug Mode Protocol Testing
```python
#!/usr/bin/env python3
"""Debug version of L02_lab_02_test.py with extensive protocol logging"""

import logging
import time
from snappi import snappi

# Enable debug logging for protocols
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_protocol_test():
    """Debug version with extensive protocol monitoring"""
    
    logger.info("=== PROTOCOL DEBUG MODE ENABLED ===")
    
    # Test connectivity to all engines
    logger.info("Testing connectivity to protocol engines...")
    try:
        import requests
        for port in [5555, 5556]:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            logger.info(f"Protocol engine {port}: {response.status_code}")
    except Exception as e:
        logger.error(f"Protocol engine connectivity failed: {e}")
        return
    
    # Initialize with protocol support
    api = snappi.api(location="https://127.0.0.1:8443", verify=False)
    
    # Configure with detailed logging
    config = api.config()
    
    # Add detailed BGP configuration with logging
    logger.info("Configuring BGP peers...")
    # ... detailed protocol configuration with logging at each step
    
    # Monitor protocol session establishment
    logger.info("Monitoring BGP session establishment...")
    for attempt in range(60):  # 5 minutes max
        try:
            metrics = api.get_metrics()
            bgp_metrics = metrics.protocol_metrics.bgp
            for bgp in bgp_metrics:
                logger.info(f"BGP {bgp.name}: State={bgp.session_state}, "
                           f"Routes_Adv={bgp.routes_advertised}, "
                           f"Routes_Rcv={bgp.routes_received}")
            
            if all(bgp.session_state == "established" for bgp in bgp_metrics):
                logger.info("All BGP sessions established!")
                break
                
        except Exception as e:
            logger.error(f"Metrics collection error: {e}")
        
        time.sleep(5)
    
    # Continue with traffic testing...

if __name__ == "__main__":
    debug_protocol_test()
```

## 📞 Getting Additional Help

### Log Collection for Protocol Issues
When reporting protocol issues, collect these logs:

```bash
# Protocol engine logs
docker logs protocol-engine-1 > protocol-engine-1.log
docker logs protocol-engine-2 > protocol-engine-2.log

# Traffic engine logs  
docker logs traffic-engine-1 > traffic-engine-1.log
docker logs traffic-engine-2 > traffic-engine-2.log

# Controller logs
docker logs controller > controller.log

# System information
docker info > docker-info.log
docker network ls > networks.log

# Protocol metrics snapshot
curl -k https://localhost:8443/api/v1/results/metrics > protocol-metrics.json
```

### Support Channels
1. **Check FAQ first**: L02_FAQ.md covers common protocol issues
2. **Protocol documentation**: Official BGP/OSPF protocol guides
3. **Community forums**: Protocol-specific discussions
4. **GitHub issues**: For protocol engine bugs
5. **Keysight support**: For critical protocol issues

---

*Remember: Protocol issues are often timing-related. Allow sufficient time for convergence and use debug logging to trace protocol state changes.*
