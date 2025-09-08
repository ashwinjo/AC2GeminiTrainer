---
title: "Lab 1 Test Execution"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Execute the OTG test script and monitor traffic generation in the Docker back-to-back setup."
tags: ["execution", "test", "snappi", "python", "traffic-generation"]
difficulty: "beginner"
---

## 🚀 Step-by-Step Instructions to run OTG Test

### Step 1: Execute the Test Script

Run the snappi test script:

```bash
python3 L01_lab_01_test.py
```

## 📋 Understanding the L01_lab_01_test.py Script

### **Script Architecture Overview**
The `L01_lab_01_test.py` script demonstrates basic OTG traffic generation in a back-to-back Docker setup. It sends bidirectional traffic between two ports and validates the results using port metrics.

### **Key Script Components:**

#### 🔧 **1. Imports and Setup**
```python
from time     import time
from datetime import datetime
from snappi   import snappi
```
- **snappi**: The Python API library for OTG (Open Traffic Generator)
- **datetime**: For timestamping and execution timing
- **time**: For wait functions and timing operations

#### 🌐 **2. API Connection (`api.config()`)**
```python
api = snappi.api(location="https://127.0.0.1:8443", verify=False)
configuration = api.config()
```
**What happens:**
- **Controller Connection**: Connects to KENG Controller at `https://127.0.0.1:8443`
- **SSL Verification**: Disabled (`verify=False`) for local testing
- **Configuration Object**: Creates empty configuration to be populated

#### 🔌 **3. Port Configuration**
```python
port1, port2 = (
    configuration.ports
    .port(name="Port-1", location="127.0.0.1:5551")
    .port(name="Port-2", location="127.0.0.1:5552")
)
```
**Key Details:**
- **Port Names**: "Port-1" and "Port-2" for identification
- **Locations**: Maps to Traffic Engine containers (5551, 5552)
- **Host Network**: Uses `127.0.0.1` because containers run in `--network=host` mode

#### 🚦 **4. Traffic Flow Configuration**
```python
flow1, flow2 = (
    configuration.flows
    .flow(name="Flow #1 - Port 1 > Port 2")
    .flow(name="Flow #2 - Port 2 > Port 1")
)

# Enable metrics and configure direction
flow1.metrics.enable = True
flow2.metrics.enable = True
flow1.tx_rx.port.tx_name = port1.name
flow1.tx_rx.port.rx_names = [port2.name]
flow2.tx_rx.port.tx_name = port2.name
flow2.tx_rx.port.rx_names = [port1.name]
```
**Traffic Flow Design:**
- **Bidirectional**: Two flows for back-to-back testing
- **Flow 1**: Port-1 → Port-2 (TX from port1, RX on port2)
- **Flow 2**: Port-2 → Port-1 (TX from port2, RX on port1)
- **Metrics Enabled**: Allows collection of flow statistics

#### ⚙️ **5. Traffic Parameters**
```python
flow1.size.fixed = 128
flow2.size.fixed = 128
for f in configuration.flows:
    f.duration.fixed_packets.packets = 2000  # Send 2000 packets per flow
    f.rate.pps = 100                         # Send 100 packets per second
```
**Test Specifications:**
- **Packet Size**: 128 bytes (fixed size)
- **Packet Count**: 2000 packets per flow (4000 total)
- **Transmission Rate**: 100 packets per second
- **Test Duration**: 20 seconds (2000 packets ÷ 100 pps)

#### 📦 **6. Packet Header Configuration**
```python
# Flow 1 packet structure
eth1 = flow1.packet.add().ethernet
ip1 = flow1.packet.add().ipv4
udp1 = flow1.packet.add().udp

# Flow 2 packet structure (alternative syntax)
flow2.packet.ethernet().ipv4().udp()
eth2, ip2, udp2 = flow2.packet[0], flow2.packet[1], flow2.packet[2]

# MAC addresses
eth1.src.value, eth1.dst.value = "00:AA:00:00:01:00", "00:AA:00:00:02:00"
eth2.src.value, eth2.dst.value = "00:AA:00:00:02:00", "00:AA:00:00:01:00"

# IP addresses
ip1.src.value, ip1.dst.value = "10.0.0.1", "10.0.0.2"
ip2.src.value, ip2.dst.value = "10.0.0.2", "10.0.0.1"
```
**Packet Structure:**
- **Layer 2**: Ethernet headers with unique MAC addresses
- **Layer 3**: IPv4 headers with 10.0.0.x addressing
- **Layer 4**: UDP headers (configured next)
- **Bidirectional**: Source/destination reversed for each flow

#### 🔢 **7. Advanced UDP Port Configuration**
```python
# Flow 1: Incrementing source ports
udp1.src_port.increment.start = 5100
udp1.src_port.increment.step  = 2
udp1.src_port.increment.count = 10
# Results in: 5100, 5102, 5104, 5106, 5108, 5110, 5112, 5114, 5116, 5118

# Flow 1: Destination port list
udp1.dst_port.values = [6100, 6125, 6150, 6170, 6190]

# Flow 2: Different increment pattern
udp2.src_port.increment.start = 5200
udp2.src_port.increment.step  = 4
udp2.src_port.increment.count = 10
# Results in: 5200, 5204, 5208, 5212, 5216, 5220, 5224, 5228, 5232, 5236

udp2.dst_port.values = [6200, 6222, 6244, 6266, 6288]
```
**Advanced Features Demonstrated:**
- **Port Increment**: Dynamic source port generation
- **Value Lists**: Specific destination port selections
- **Traffic Variation**: Creates diverse packet patterns for realistic testing

#### ▶️ **8. Test Execution**
```python
api.set_config(configuration)  # Apply configuration

# Start traffic transmission
cs = api.control_state()
cs.choice = cs.TRAFFIC
cs.traffic.choice = cs.traffic.FLOW_TRANSMIT
cs.traffic.flow_transmit.state = cs.traffic.flow_transmit.START
api.set_control_state(cs)
```
**Execution Flow:**
- **Configuration Apply**: Pushes config to traffic engines
- **Control State**: Uses OTG control state API
- **Traffic Start**: Begins packet transmission on both flows

#### 📊 **9. Statistics Verification (`verify_statistics()`)**
```python
def verify_statistics(api, configuration):
    statistics = api.metrics_request()
    statistics.port.port_names = [p.name for p in configuration.ports]
    statistics.port.column_names = [statistics.port.FRAMES_TX, statistics.port.FRAMES_RX]
    
    results = api.get_metrics(statistics)
    
    total_frames_tx = sum([m.frames_tx for m in results.port_metrics])
    total_frames_rx = sum([m.frames_rx for m in results.port_metrics])
    total_expected  = sum([f.duration.fixed_packets.packets for f in configuration.flows])
    
    return total_expected == total_frames_tx and total_frames_rx >= total_expected
```
**Validation Logic:**
- **Expected**: 4000 packets total (2000 per flow)
- **TX Validation**: Confirms all packets were transmitted
- **RX Validation**: Confirms all packets were received (≥ expected)
- **Success Criteria**: TX matches expected AND RX ≥ expected

#### ⏱️ **10. Wait Function (`wait_for()`)**
```python
def wait_for(func, timeout=30, interval=1):
    start = time.time()
    while time.time() - start <= timeout:
        if func():
            return True
        time.sleep(interval)
    return False
```
**Polling Mechanism:**
- **Timeout**: 30 seconds maximum wait
- **Interval**: Check every 1 second
- **Function**: Repeatedly calls `verify_statistics()`
- **Success**: Returns `True` when validation passes

## 🔄 **Script Execution Flow**

### **Expected Output:**
```
Starting connection to controller                     ... 
Starting configuration apply                          ... 
Starting transmit on all flows                        ... 
Starting statistics verification on all ports         ... 
====================================================================================
			Expected	Tx		Rx
TOTAL  		4000		4000		4000
====================================================================================
Test is PASSED in 0:00:20.123456                                      
```

### **Key Learning Points:**

#### **1. OTG API Fundamentals**
- **snappi Library**: Python wrapper for OTG API
- **Configuration Model**: Declarative approach to traffic setup
- **Control State**: Imperative commands for start/stop operations

#### **2. Back-to-Back Testing**
- **Bidirectional Flows**: Simultaneous traffic in both directions
- **Port Mapping**: Direct connection between traffic engines
- **Metrics Validation**: Automated pass/fail determination

#### **3. Traffic Engineering**
- **Packet Construction**: Layer-by-layer header building
- **Field Variation**: Increment and list-based field modification
- **Rate Control**: Precise packet-per-second timing

#### **4. Production Practices**
- **Error Handling**: Assertion-based validation
- **Timing Measurement**: Execution duration tracking
- **Automated Verification**: Polling-based statistics checking

**Expected Results:**
- **Test Duration**: ~20 seconds (plus setup/teardown time)
- **Packet Success**: 4000 packets transmitted and received
- **Zero Loss**: All transmitted packets should be received
- **Validation**: Automated PASS/FAIL determination
