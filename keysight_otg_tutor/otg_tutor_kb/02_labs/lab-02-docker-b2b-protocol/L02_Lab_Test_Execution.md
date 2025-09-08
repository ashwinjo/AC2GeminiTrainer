---
title: "Lab 2 Test Execution"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Execute BGP protocol configuration, session establishment, and traffic generation with comprehensive monitoring."
tags: ["execution", "test", "snappi", "python", "protocol", "bgp", "docker-compose"]
difficulty: "intermediate"
---

# Lab 02: Test Execution with Protocol Engines

## 🚀 Step-by-Step Instructions to run Protocol-Aware OTG Test

### Step 1: Start the Docker Compose Environment

First, start the OTG infrastructure using the provided docker compose file:

```bash
# Start the OTG containers (controller, traffic engines, protocol engines)
docker compose -f L02_lab_topo.yaml up -d
```

**What this creates:**
- **Controller**: KENG controller on `localhost:8443`
- **Traffic Engine 1**: Port `5551`, Protocol Engine port `50071`
- **Traffic Engine 2**: Port `5552`, Protocol Engine port `50072`
- **Protocol Engine 1**: Shares network with Traffic Engine 1
- **Protocol Engine 2**: Shares network with Traffic Engine 2

### Step 2: Connect Container Networks

Run the container connection script to create veth pairs between the traffic engines:

```bash
# Make the script executable and run it
chmod +x L02_connect_containers_veth.sh
./L02_connect_containers_veth.sh
```

**What this script does:**
- Creates veth pair connections between traffic engines
- Sets up the network topology for BGP protocol testing
- Configures the virtual interfaces needed for traffic flow

### Step 3: Verify Container Status

Check that all containers are running properly:

```bash
# Check container status
docker compose -f L02_lab_topo.yaml ps

# Expected output should show all 5 containers as "Up"
```

### Step 4: Execute the Protocol Test Script

Run the snappi test script with BGP protocol configuration:

```bash
python3 L02_lab_02_test.py
```

## 📋 Understanding the L02_lab_02_test.py Script

### **Script Architecture Overview**
The `L02_lab_02_test.py` script is a comprehensive BGP protocol testing framework that demonstrates the full integration between Protocol Engines and Traffic Engines in Lab 02's shared network architecture.

### **Key Script Components:**

#### 🔧 **1. Configuration Creation (`create_protocol_config()`)**
```python
# Key elements the script configures:
- Two devices with shared TE+PE network architecture
- BGP AS 65001 (device1) ↔ AS 65002 (device2) peering
- 10,000 IPv4 routes advertised per device
- Bidirectional traffic flows using BGP-learned routes
```

**What happens:**
- **Port Mapping**: Connects to traffic engines on `localhost:5551` and `localhost:5552`
- **Device Association**: Links devices with their TE/PE container pairs
- **IP Configuration**: Sets up 192.168.1.1/24 and 192.168.1.2/24 addressing
- **BGP Peering**: Configures EBGP sessions between the two devices
- **Route Advertisement**: Each device advertises 10,000 routes (10.0.0.0/24 range and 20.0.0.0/24 range)

#### 🌐 **2. Protocol Session Management**
```python
# BGP session establishment process:
start_protocols(api)                    # Start BGP sessions
wait_for_protocol_convergence(api, 120) # Wait up to 2 minutes for convergence
```

**What the script monitors:**
- **Session States**: Tracks BGP sessions from "Active" → "Established"
- **Route Learning**: Monitors route advertisement and reception counts
- **Convergence Timing**: Measures how long BGP takes to fully converge
- **Success Criteria**: Requires 20,000+ total routes learned (10K per peer)

#### 🚦 **3. Protocol-Aware Traffic Generation (`run_traffic_test()`)**
```python
# Traffic configuration highlights:
- Bidirectional flows: device1 ↔ device2
- Source IPs: 10.0.0.1 (device1), 20.0.0.1 (device2)  
- Destination IPs: Uses BGP-learned route ranges
- Traffic Rate: 1000 packets per second per flow
- Duration: 60 seconds (60,000 packets total per flow)
- Protocol: TCP with source/destination port mapping
```

**Key Traffic Features:**
- **Protocol-Aware Routing**: Traffic uses routes learned through BGP, not static routes
- **Dynamic Addressing**: Destination IPs increment through advertised route ranges
- **Bidirectional Testing**: Simultaneous traffic in both directions
- **Real-time Monitoring**: Progress updates every 10 seconds during traffic generation

#### 📊 **4. Comprehensive Metrics Collection (`collect_comprehensive_metrics()`)**
```python
# The script collects and analyzes:
- BGP session states and route counts
- Traffic statistics (TX/RX frames, loss rates)
- Protocol convergence timing
- Overall test success/failure criteria
```

**Success Criteria Validation:**
- **Protocol Success**: All BGP sessions "established" + 20,000+ routes learned
- **Traffic Success**: Frame loss < 1.0%
- **Performance Metrics**: Convergence time, throughput rates

## 🔄 **Script Execution Flow**

### Step 2: Observe Script Output

The script provides detailed logging throughout execution:

```
=== LAB 02: PROTOCOL ENGINE TESTING STARTED ===
Connected to KENG Controller at https://127.0.0.1:8443
Protocol configuration created
Applying configuration to protocol engines...
Configuration applied successfully
Starting BGP protocol sessions...
BGP protocol start command sent
Monitoring BGP session establishment...
BGP bgp_peer1: State=active, Routes_Adv=0, Routes_Rcv=0
BGP bgp_peer2: State=active, Routes_Adv=0, Routes_Rcv=0
BGP bgp_peer1: State=established, Routes_Adv=10000, Routes_Rcv=10000
BGP bgp_peer2: State=established, Routes_Adv=10000, Routes_Rcv=10000
✅ BGP convergence completed in 45.2s
📊 Routes advertised: 20000, Routes received: 20000
```

### Step 3: Traffic Generation and Results

Once BGP converges, protocol-aware traffic begins:

```
Starting 60s traffic test through BGP routes...
Traffic generation started
Flow flow_device1_to_device2: TX=10000, RX=10000, Loss=0
Flow flow_device2_to_device1: TX=10000, RX=10000, Loss=0
Traffic progress: 60s / 60s
Traffic generation stopped

📊 PROTOCOL METRICS:
BGP Peer: bgp_peer1
  Session State: established
  Routes Advertised: 10000
  Routes Received: 10000

🚦 TRAFFIC METRICS:
Flow: flow_device1_to_device2
  Frames TX: 60,000
  Frames RX: 60,000
  Frame Loss: 0 (0.00%)

✅ TRAFFIC TEST: PASSED (Loss < 1%)
✅ PROTOCOL TEST: PASSED (All sessions established, routes learned)
```

## 🎯 **Key Learning Points from the Script**

### **1. Shared Network Architecture Integration**
```python
# Script demonstrates TE+PE shared networking:
device1.container_name = "traffic-engine-1"
device1.protocol_container_name = "protocol-engine-1"
# PE1 shares TE1's network namespace (port 50071 via TE1's port mapping)
```

### **2. BGP Protocol Fundamentals**
- **AS Numbers**: Autonomous System identification (65001, 65002)
- **Router IDs**: Unique BGP router identification (192.168.1.1, 192.168.1.2)
- **Route Advertisement**: How networks are advertised between BGP peers
- **Convergence**: Time required for BGP sessions to establish and exchange routes

### **3. Protocol-Traffic Integration**
- **Route Learning**: PE learns routes, shares with TE via shared network
- **Traffic Generation**: TE uses PE-learned routes for intelligent packet forwarding
- **End-to-End Validation**: Both protocol establishment AND traffic flow must succeed

### **4. Production-Ready Features**
- **Comprehensive Logging**: Detailed execution tracking and debugging
- **Error Handling**: Graceful cleanup and timeout management
- **Success Criteria**: Automated pass/fail determination
- **Performance Monitoring**: Real-time metrics collection and analysis

**Expected Results:**
- **BGP Convergence**: 30-60 seconds for full route learning
- **Route Scale**: 20,000 total routes (10K advertised per peer)
- **Traffic Performance**: >99% success rate with zero packet loss
- **Protocol Stability**: Established BGP sessions throughout test duration
