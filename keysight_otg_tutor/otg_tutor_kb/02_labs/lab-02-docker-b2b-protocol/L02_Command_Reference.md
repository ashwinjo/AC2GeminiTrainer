---
title: "Lab 2 Command Reference Card"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Quick reference for all Docker, networking, protocol, and OTG commands used in Lab 2 protocol engine testing."
tags: ["reference", "commands", "docker", "networking", "protocol", "bgp", "cheat-sheet"]
difficulty: "intermediate"
---

# Lab 02: Command Reference Card - Protocol Engine Testing

## 📋 Lab 02 Step-by-Step Commands

### #2-01: Examine Docker Compose Configuration
```bash
cd ~/ac2-workshop/lab-02
cat compose.yml
```
**Purpose:** Review the Docker Compose file with shared network architecture (TE+PE pairs)

### #2-02: Deploy Lab Environment  
```bash
docker-compose -f compose.yml up -d
sudo bash connect_containers_veth.sh lab-02_traffic_engine_1_1 lab-02_traffic_engine_2_1 veth0 veth1
```
**Purpose:** Deploy all 5 containers and connect TE containers with veth pairs using IP namespaces

### #2-03: Verify Container Deployment
```bash
docker ps
```
**Purpose:** Confirm all containers are running (controller, 2 TEs, 2 PEs)

### #2-04: Check Traffic Engine 1 Logs
```bash
docker logs lab-02_traffic_engine_1_1
```
**Purpose:** Verify TE1 found veth0 interface and bound successfully

### #2-05: Check Traffic Engine 2 Logs  
```bash
docker logs lab-02_traffic_engine_2_1
```
**Purpose:** Verify TE2 found veth1 interface and bound successfully

### #2-06: Inspect Docker Network
```bash
docker network ls
docker inspect lab-02_default
```
**Purpose:** Examine the custom bridge network created by Docker Compose

### #2-07: Network Architecture Analysis
```bash
docker network ls
docker inspect lab-02_default
```
**Purpose:** Understand container IP assignments and network configuration

### #2-08: Edit Test Script
```bash
vi lab-02_test.py
```
**Purpose:** Review/modify the BGP protocol test script

### #2-09: Execute Protocol Test
```bash
python3 lab-02_test.py
```
**Purpose:** Run BGP session establishment and traffic generation test

### #2-10: Monitor BGP Metrics
```bash
curl -k -d '{"choice":"bgpv4"}' -X POST https://127.0.0.1:8443/monitor/metrics
```
**Purpose:** Query BGP session statistics and route counts

### #2-11: Check IPv4 Neighbors
```bash
curl -k -d '{"choice":"ipv4_neighbors"}' -X POST https://127.0.0.1:8443/monitor/states
```
**Purpose:** Verify BGP neighbor relationships and session states

### #2-12: Examine BGP Prefixes
```bash
curl -k -d '{"choice":"bgp_prefixes"}' -X POST https://127.0.0.1:8443/monitor/states
```
**Purpose:** View advertised and received BGP route prefixes

### #2-13: Modify Test for Packet Capture
```bash
vi lab-02_test.py
```
**Purpose:** Add packet capture functionality to the test script

### #2-14: Install Packet Analysis Tools
```bash
sudo apt install tshark -y
ll
```
**Purpose:** Install Wireshark/tshark for packet capture analysis

### #2-15: Analyze Captured Packets
```bash
tshark -r prx.pcap
```
**Purpose:** View all captured packets from the test

### #2-16: Further Script Modifications
```bash
nano lab-02_test.py
```
**Purpose:** Make additional changes to test parameters

### #2-17: Re-run Protocol Test
```bash
python3 lab-02_test.py
```
**Purpose:** Execute modified test with new configurations

### #2-18: Additional Script Edits
```bash
nano lab-02_test.py
```
**Purpose:** Fine-tune test parameters or add features

### #2-19: Filter TCP Traffic
```bash
tshark -r prx.pcap -Y tcp
```
**Purpose:** Analyze only TCP packets (including BGP traffic)

### #2-20: Clean Up Environment
```bash
docker-compose down
```
**Purpose:** Stop and remove all containers deployed by Docker Compose

### #2-21: Remove Network Namespaces
```bash
sudo ip netns del lab-02_traffic_engine_1_1 && sudo ip netns del lab-02_traffic_engine_2_1
```
**Purpose:** Clean up IP namespaces created by the connection script

## 🐳 Docker Compose Architecture Commands

### Container Operations
```bash
# List all containers with Docker Compose naming
docker ps -a

# Check specific Lab 02 containers
docker ps | grep -E "lab-02"

# View container logs (Docker Compose naming)
docker logs lab-02_keng-controller_1
docker logs lab-02_protocol_engine_1_1
docker logs lab-02_protocol_engine_2_1
docker logs lab-02_traffic_engine_1_1
docker logs lab-02_traffic_engine_2_1

# Container resource usage
docker stats --no-stream

# Docker Compose operations
docker-compose -f compose.yml up -d     # Start all services
docker-compose -f compose.yml down      # Stop and remove all services
docker-compose -f compose.yml restart   # Restart all services
docker-compose -f compose.yml logs      # View all logs

# Individual container control
docker stop lab-02_protocol_engine_1_1
docker start lab-02_protocol_engine_1_1
docker restart lab-02_traffic_engine_1_1
```

## 🌐 Network Interface and Namespace Commands

### Container Network Inspection
```bash
# Check Docker networks created by Compose
docker network ls
docker inspect lab-02_default

# Examine container network settings
docker exec -it lab-02_traffic_engine_1_1 ip addr
docker exec -it lab-02_traffic_engine_2_1 ip addr

# Check container connectivity
docker exec -it lab-02_traffic_engine_1_1 ping lab-02_traffic_engine_2_1
```

### IP Namespace Management
```bash
# List network namespaces (created by connection script)
sudo ip netns list

# Execute commands in container namespaces
sudo ip netns exec lab-02_traffic_engine_1_1 ip link show
sudo ip netns exec lab-02_traffic_engine_2_1 ip link show

# Check veth interfaces in namespaces
sudo ip netns exec lab-02_traffic_engine_1_1 ip link show veth0
sudo ip netns exec lab-02_traffic_engine_2_1 ip link show veth1

# Remove namespaces (cleanup)
sudo ip netns del lab-02_traffic_engine_1_1
sudo ip netns del lab-02_traffic_engine_2_1
```

### Connection Script Analysis
```bash
# View the connection script
cat connect_containers_veth.sh

# Run connection script manually
sudo bash connect_containers_veth.sh lab-02_traffic_engine_1_1 lab-02_traffic_engine_2_1 veth0 veth1

# Verify veth connection
sudo ip netns exec lab-02_traffic_engine_1_1 ping -I veth0 -c 3 192.168.1.2
```

## 🔧 Protocol Engine Health Checks

### Connectivity Testing (Lab 02 Ports)
```bash
# Test protocol engine health endpoints (shared network ports)
curl -v http://localhost:50071/health   # PE1 via TE1's network
curl -v http://localhost:50072/health   # PE2 via TE2's network

# Test traffic engine endpoints
curl -v http://localhost:5551/health    # TE1
curl -v http://localhost:5552/health    # TE2

# Test controller endpoint
curl -k https://localhost:8443/health   # Controller

# Check port availability for Lab 02
lsof -i :50071  # PE1 (via TE1 network)
lsof -i :50072  # PE2 (via TE2 network) 
lsof -i :5551   # TE1
lsof -i :5552   # TE2
lsof -i :8443   # Controller

# Network connectivity test
netstat -tulpn | grep -E ":(50071|50072|5551|5552|8443)"
```

## 📊 Protocol Monitoring Commands (Lab 02 API)

### BGP Session Monitoring
```bash
# Lab 02 specific BGP monitoring commands
curl -k -d '{"choice":"bgpv4"}' -X POST https://127.0.0.1:8443/monitor/metrics
curl -k -d '{"choice":"ipv4_neighbors"}' -X POST https://127.0.0.1:8443/monitor/states  
curl -k -d '{"choice":"bgp_prefixes"}' -X POST https://127.0.0.1:8443/monitor/states

# Alternative monitoring methods
curl -k https://localhost:8443/api/v1/results/metrics | jq '.protocol_metrics'
curl -k https://localhost:8443/api/v1/results/metrics | jq '.protocol_metrics.bgp'

# BGP session states
curl -k https://localhost:8443/api/v1/results/metrics | \
  jq '.protocol_metrics.bgp[] | {name: .name, state: .session_state}'

# BGP route counts
curl -k https://localhost:8443/api/v1/results/metrics | \
  jq '.protocol_metrics.bgp[] | {name: .name, adv: .routes_advertised, rcv: .routes_received}'

# Continuous monitoring
watch -n 5 'curl -s -k -d "{\"choice\":\"bgpv4\"}" -X POST https://127.0.0.1:8443/monitor/metrics'
```

### Configuration Verification
```bash
# Get current configuration
curl -k https://localhost:8443/api/v1/config

# BGP configuration
curl -k https://localhost:8443/api/v1/config | jq '.devices[].protocols.bgp'

# Device configuration
curl -k https://localhost:8443/api/v1/config | jq '.devices[]'

# Flow configuration
curl -k https://localhost:8443/api/v1/config | jq '.flows'
```

## 🚦 Traffic Commands with Protocol Awareness

### Traffic Generation (Lab 02)
```bash
# Execute Lab 02 protocol test script
python3 lab-02_test.py

# Background execution with logging
nohup python3 lab-02_test.py > test_output.log 2>&1 &

# Monitor test progress
tail -f test_output.log

# Kill running test
pkill -f lab-02_test.py

# Edit test script during lab
vi lab-02_test.py      # Using vi editor
nano lab-02_test.py    # Using nano editor
```

### Packet Capture Analysis
```bash
# Install packet analysis tools
sudo apt install tshark -y

# View captured packets
tshark -r prx.pcap

# Filter specific traffic types
tshark -r prx.pcap -Y tcp          # TCP traffic (includes BGP)
tshark -r prx.pcap -Y bgp          # BGP protocol messages
tshark -r prx.pcap -Y icmp         # ICMP traffic
tshark -r prx.pcap -Y "tcp.port == 179"  # BGP port traffic

# List files in directory
ll    # List captured files and scripts
```

### Traffic Metrics
```bash
# Get traffic statistics
curl -k https://localhost:8443/api/v1/results/metrics | jq '.flow_metrics'

# Traffic through protocol routes
curl -k https://localhost:8443/api/v1/results/metrics | \
  jq '.flow_metrics[] | {name: .name, tx_rate: .frames_tx_rate, rx_rate: .frames_rx_rate}'

# Combined protocol and traffic metrics
curl -k https://localhost:8443/api/v1/results/metrics | \
  jq '{protocols: .protocol_metrics.bgp, traffic: .flow_metrics}'
```

## 🔍 Troubleshooting Commands

### System Diagnostics
```bash
# System resource usage
free -h
df -h
top -n 1

# Docker system info
docker system info
docker system df

# Network connectivity
ping -c 3 localhost
telnet localhost 8443
telnet localhost 5555
telnet localhost 5556
```

### Protocol Debugging
```bash
# Protocol engine process check
ps aux | grep -E "(protocol|bgp)"

# Network namespace check
sudo ip netns list

# Container network inspection
docker inspect protocol-engine-1 | jq '.[0].NetworkSettings'
docker inspect protocol-engine-2 | jq '.[0].NetworkSettings'

# Log analysis
docker logs protocol-engine-1 | grep -i error
docker logs protocol-engine-2 | grep -i bgp
docker logs controller | grep -i protocol
```

### Emergency Recovery
```bash
# Complete protocol reset
curl -k -X POST https://localhost:8443/api/v1/control/protocols/stop
docker stop protocol-engine-1 protocol-engine-2 traffic-engine-1 traffic-engine-2 controller
docker rm protocol-engine-1 protocol-engine-2 traffic-engine-1 traffic-engine-2 controller

# Clean protocol state
sudo rm -rf /tmp/bgp_* /tmp/protocol_* 2>/dev/null || true

# Recreate network interfaces
sudo ip link delete veth0 2>/dev/null || true
sudo ip link add name veth0 type veth peer name veth1
sudo ip link set dev veth0 up && sudo ip link set dev veth1 up
```

## 📋 One-Liners for Quick Operations

### Quick Status Checks
```bash
# All containers status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Protocol engine health
curl -s http://localhost:5555/health && curl -s http://localhost:5556/health && echo "All protocol engines healthy"

# BGP session summary
curl -s -k https://localhost:8443/api/v1/results/metrics | jq -r '.protocol_metrics.bgp[] | "\(.name): \(.session_state)"'

# Quick traffic check
curl -s -k https://localhost:8443/api/v1/results/metrics | jq -r '.flow_metrics[] | "\(.name): TX=\(.frames_tx) RX=\(.frames_rx)"'
```

### Quick Setup
```bash
# Complete environment setup in one command
sudo ip link add name veth0 type veth peer name veth1 && sudo ip link set dev veth0 up && sudo ip link set dev veth1 up && \
docker run -d --name controller --network=host ghcr.io/open-traffic-generator/keng-controller:1.14.0-1 --http-port 8443 --accept-eula && \
sleep 5 && \
docker run -d --name traffic-engine-1 --network=host -e ARG_IFACE_LIST=virtual@af_packet,veth0 -e OPT_NO_HUGEPAGES=Yes --privileged -e OPT_LISTEN_PORT=5551 ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99 && \
docker run -d --name traffic-engine-2 --network=host -e ARG_IFACE_LIST=virtual@af_packet,veth1 -e OPT_NO_HUGEPAGES=Yes --privileged -e OPT_LISTEN_PORT=5552 ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99 && \
docker run -d --name protocol-engine-1 --network=host -e OPT_LISTEN_PORT=5555 ghcr.io/open-traffic-generator/ixia-c-protocol-engine:1.8.0.99 && \
docker run -d --name protocol-engine-2 --network=host -e OPT_LISTEN_PORT=5556 ghcr.io/open-traffic-generator/ixia-c-protocol-engine:1.8.0.99
```

### Quick Cleanup
```bash
# Complete cleanup in one command
docker stop protocol-engine-1 protocol-engine-2 traffic-engine-1 traffic-engine-2 controller 2>/dev/null || true && \
docker rm protocol-engine-1 protocol-engine-2 traffic-engine-1 traffic-engine-2 controller 2>/dev/null || true && \
sudo ip link delete veth0 2>/dev/null || true
```

## 🎯 Environment Variables Reference

### Protocol Engine Variables
```bash
# Protocol engine configuration
OPT_LISTEN_PORT=5555          # Protocol engine listening port
OPT_LOG_LEVEL=info            # Logging level (debug, info, warn, error)
OPT_PROTOCOL_LIST=bgp,ospf    # Supported protocols
OPT_SESSION_TIMEOUT=300       # Protocol session timeout

# Traffic engine integration
ARG_IFACE_LIST=virtual@af_packet,veth0  # Interface binding
OPT_NO_HUGEPAGES=Yes                     # Disable hugepages
OPT_LISTEN_PORT=5551                     # Traffic engine port
```

---

**💡 Pro Tips:**
- Always start containers in order: Controller → Traffic Engines → Protocol Engines
- Use `docker logs` for detailed troubleshooting
- Monitor BGP convergence before starting traffic
- Allow 60+ seconds for initial protocol convergence
- Use `jq` for JSON parsing of API responses
