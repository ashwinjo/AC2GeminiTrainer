---
title: "Lab 2 Packet Capture - Protocol Traffic Analysis"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Learn how to capture and analyze network packets during protocol-aware traffic generation using OTG built-in capture functionality."
tags: ["packet-capture", "analysis", "protocol", "bgp", "pcap", "wireshark"]
difficulty: "intermediate"
---

# Lab 02: Packet Capture - Protocol Traffic Analysis

## 🎯 Overview

This section demonstrates how to capture packets on both TX and RX ports during Lab 02 protocol testing. Unlike Lab 01 which only generated raw traffic, Lab 02 includes BGP protocol packets and data traffic, making packet capture essential for understanding protocol behavior and troubleshooting.

## 📦 Packet Capture Configuration in snappi

### **Understanding the Capture Setup**

From the Lab 02 test script (`lab_02_test.py`), the packet capture functionality is configured as follows:

```python
def ebgp_route_prefix_config(api, tc):
    c = api.config()
    ptx = c.ports.add(name="ptx", location="localhost:5551+localhost:50071")
    prx = c.ports.add(name="prx", location="localhost:5552+localhost:50072")
    
    # capture configuration
    rx_capture = c.captures.add(name="prx_capture")
    rx_capture.set(port_names=["prx"], format="pcap", overwrite=True)
    
    tx_capture = c.captures.add(name="ptx_capture") 
    tx_capture.set(port_names=["ptx"], format="pcap", overwrite=True)
```

### **Key Capture Configuration Elements:**

#### **1. Port Configuration with Protocol Engine Integration**
```python
ptx = c.ports.add(name="ptx", location="localhost:5551+localhost:50071")
prx = c.ports.add(name="prx", location="localhost:5552+localhost:50072")
```
**Explanation:**
- **Port Location Format**: `traffic_engine_port+protocol_engine_port`
- **ptx (TX Port)**: Traffic Engine on 5551 + Protocol Engine on 50071
- **prx (RX Port)**: Traffic Engine on 5552 + Protocol Engine on 50072
- **Shared Network**: Both TE and PE share the same network namespace

#### **2. RX Capture Configuration**
```python
rx_capture = c.captures.add(name="prx_capture")
rx_capture.set(port_names=["prx"], format="pcap", overwrite=True)
```
**Parameters:**
- **Name**: `prx_capture` - Identifies the RX port capture
- **Port**: `["prx"]` - Captures packets on the receiving port
- **Format**: `"pcap"` - Standard packet capture format compatible with Wireshark
- **Overwrite**: `True` - Replaces any existing capture file

#### **3. TX Capture Configuration**
```python
tx_capture = c.captures.add(name="ptx_capture")
tx_capture.set(port_names=["ptx"], format="pcap", overwrite=True)
```
**Parameters:**
- **Name**: `ptx_capture` - Identifies the TX port capture  
- **Port**: `["ptx"]` - Captures packets on the transmitting port
- **Format**: `"pcap"` - Standard packet capture format
- **Overwrite**: `True` - Replaces any existing capture file

## 🚀 Implementing Packet Capture in Lab 02

### **Step 1: Modify the Test Script**

Add the packet capture functionality to your `L02_lab_02_test.py` script:

```python
def create_protocol_config_with_capture():
    """Create OTG configuration with BGP protocol engines and packet capture"""
    
    config = snappi.Config()
    
    # Define test ports (connected to traffic engines + protocol engines)
    port1 = config.ports.add(name="ptx", location="localhost:5551+localhost:50071")
    port2 = config.ports.add(name="prx", location="localhost:5552+localhost:50072")
    
    # Configure packet captures for both ports
    rx_capture = config.captures.add(name="prx_capture")
    rx_capture.set(port_names=["prx"], format="pcap", overwrite=True)
    
    tx_capture = config.captures.add(name="ptx_capture") 
    tx_capture.set(port_names=["ptx"], format="pcap", overwrite=True)
    
    # Continue with BGP and traffic configuration...
    # (Rest of the configuration from L02_lab_02_test.py)
    
    return config
```

### **Step 2: Start and Stop Capture Operations**

Add capture control functions to your script:

```python
def start_capture(api):
    """Start packet capture on both ports"""
    logger.info("Starting packet capture on both ports...")
    
    control_state = snappi.ControlState()
    control_state.capture.state = control_state.capture.START
    api.set_control_state(control_state)
    logger.info("Packet capture started")

def stop_capture(api):
    """Stop packet capture and retrieve files"""
    logger.info("Stopping packet capture...")
    
    control_state = snappi.ControlState()
    control_state.capture.state = control_state.capture.STOP
    api.set_control_state(control_state)
    logger.info("Packet capture stopped")

def get_capture_files(api):
    """Retrieve capture files from the controller"""
    logger.info("Retrieving capture files...")
    
    # Get RX capture file
    api.get_capture(api.capture_request().set(port_name="prx"), "prx.pcap")
    logger.info("RX capture saved as prx.pcap")
    
    # Get TX capture file  
    api.get_capture(api.capture_request().set(port_name="ptx"), "ptx.pcap")
    logger.info("TX capture saved as ptx.pcap")
```

### **Step 3: Integrate Capture into Test Flow**

Modify your main test function to include packet capture:

```python
def main():
    """Main test execution function with packet capture"""
    
    logger.info("=== LAB 02: PROTOCOL ENGINE TESTING WITH PACKET CAPTURE ===")
    
    api = snappi.api(location="https://127.0.0.1:8443", verify=False)
    
    try:
        # Create configuration with capture enabled
        config = create_protocol_config_with_capture()
        api.set_config(config)
        
        # Start packet capture before protocol establishment
        start_capture(api)
        
        # Start protocols and wait for convergence
        start_protocols(api)
        wait_for_protocol_convergence(api, timeout=120)
        
        # Generate protocol-aware traffic (capture is running)
        run_traffic_test(api, duration=60)
        
        # Stop capture and retrieve files
        stop_capture(api)
        get_capture_files(api)
        
        # Collect metrics
        collect_comprehensive_metrics(api)
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        raise
    finally:
        graceful_cleanup(api)
```

## 📊 What Gets Captured

### **Protocol Traffic Types in Lab 02:**

#### **1. BGP Protocol Packets**
- **BGP OPEN**: Session establishment messages
- **BGP UPDATE**: Route advertisement messages (10,000 routes per peer)
- **BGP KEEPALIVE**: Session maintenance messages
- **BGP NOTIFICATION**: Error or session termination messages

#### **2. Data Traffic Packets**  
- **TCP Data**: Application traffic using BGP-learned routes
- **Source IPs**: 10.0.0.1 (device1), 20.0.0.1 (device2)
- **Destination IPs**: BGP-advertised route ranges
- **Traffic Rate**: 1000 pps per flow, 1024-byte packets

#### **3. Supporting Protocol Traffic**
- **ARP Requests/Replies**: Address resolution for BGP peering
- **ICMP**: Network diagnostics (if enabled)

## 🔍 Analyzing Captured Packets

### **Step 1: Install Packet Analysis Tools**

```bash
# Install tshark (command-line Wireshark)
sudo apt install tshark -y

# Verify installation
tshark --version
```

### **Step 2: Basic Packet Analysis**

```bash
# View all captured packets from RX port
tshark -r prx.pcap

# View all captured packets from TX port  
tshark -r ptx.pcap

# Count total packets in each capture
tshark -r prx.pcap | wc -l
tshark -r ptx.pcap | wc -l
```

### **Step 3: Protocol-Specific Analysis**

```bash
# Filter BGP protocol packets only
tshark -r prx.pcap -Y bgp

# Filter TCP data traffic (excluding BGP control traffic)
tshark -r prx.pcap -Y tcp -Y "not bgp"

# Filter by BGP message types
tshark -r prx.pcap -Y "bgp.type == 1"  # BGP OPEN messages
tshark -r prx.pcap -Y "bgp.type == 2"  # BGP UPDATE messages  
tshark -r prx.pcap -Y "bgp.type == 4"  # BGP KEEPALIVE messages

# Filter traffic by IP address ranges
tshark -r prx.pcap -Y "ip.src == 10.0.0.1 or ip.dst == 10.0.0.1"
tshark -r prx.pcap -Y "ip.src_host contains 20.0.0"

# Show BGP route advertisements
tshark -r prx.pcap -Y "bgp.update.nlri" -T fields -e bgp.update.nlri
```

### **Step 4: Advanced Traffic Analysis**

```bash
# Analyze traffic timing and rates
tshark -r prx.pcap -T fields -e frame.time_relative -e frame.len

# Check for packet loss indicators
tshark -r prx.pcap -Y "tcp.analysis.retransmission"
tshark -r prx.pcap -Y "tcp.analysis.duplicate_ack"

# Compare TX vs RX packet counts
echo "TX Packets: $(tshark -r ptx.pcap | wc -l)"
echo "RX Packets: $(tshark -r prx.pcap | wc -l)"

# BGP session analysis
tshark -r prx.pcap -Y bgp -T fields -e bgp.type -e frame.time_relative
```

## 🎯 Key Analysis Points

### **BGP Protocol Validation:**
1. **Session Establishment**: Look for BGP OPEN messages at test start
2. **Route Advertisement**: Verify 10,000 UPDATE messages per peer
3. **Session Maintenance**: Confirm periodic KEEPALIVE messages
4. **No Errors**: Absence of BGP NOTIFICATION messages

### **Traffic Flow Validation:**
1. **Route Utilization**: Data traffic using BGP-advertised prefixes
2. **Bidirectional Flow**: Traffic in both directions
3. **Rate Compliance**: 1000 pps rate maintained
4. **Zero Loss**: TX packet count matches RX packet count

### **Protocol-Traffic Integration:**
1. **Timing Correlation**: Data traffic starts after BGP convergence
2. **Route Dependency**: Traffic stops if BGP sessions fail
3. **Path Selection**: Traffic follows BGP best path selection

## 🚨 Troubleshooting with Packet Capture

### **Common Issues and Analysis:**

#### **1. BGP Session Failures**
```bash
# Check for BGP errors
tshark -r prx.pcap -Y "bgp.type == 3"  # NOTIFICATION messages
tshark -r prx.pcap -Y bgp -T fields -e bgp.error_code -e bgp.error_subcode
```

#### **2. Missing Route Advertisements**  
```bash
# Count UPDATE messages
tshark -r prx.pcap -Y "bgp.type == 2" | wc -l
# Should show ~10,000 per peer = ~20,000 total
```

#### **3. Traffic Path Issues**
```bash
# Verify traffic is using BGP routes
tshark -r prx.pcap -Y "ip.dst_host contains 10.0.0 or ip.dst_host contains 20.0.0"
```

## 📋 Lab Exercise: Packet Capture Analysis

### **Exercise Tasks:**

1. **Modify Script**: Add packet capture to your L02_lab_02_test.py
2. **Run Test**: Execute the modified script with capture enabled
3. **Analyze BGP**: Count and examine BGP protocol messages
4. **Analyze Traffic**: Verify data traffic characteristics
5. **Compare Files**: Analyze differences between TX and RX captures

### **Expected Results:**
- **BGP OPEN**: 2 messages (one per peer)
- **BGP UPDATE**: ~20,000 messages (route advertisements)
- **BGP KEEPALIVE**: Periodic throughout test duration
- **Data Traffic**: 120,000 packets (60 seconds × 1000 pps × 2 flows)
- **Zero Loss**: TX count = RX count for data traffic

### **Analysis Questions:**
1. How many BGP UPDATE messages were captured?
2. What was the time difference between BGP OPEN and first UPDATE?
3. How long did complete route advertisement take?
4. Were any BGP NOTIFICATION (error) messages present?
5. Does the data traffic timing correlate with BGP convergence?

---

**💡 Pro Tips:**
- Start capture before BGP session establishment to see complete protocol flow
- Use Wireshark GUI for detailed packet inspection if available
- Compare TX and RX captures to identify any packet loss or modification
- Save capture files for later analysis and troubleshooting reference
- Use packet timing analysis to understand protocol convergence behavior

This packet capture capability provides deep visibility into both BGP protocol behavior and data traffic flow, essential for understanding and troubleshooting protocol-aware network testing scenarios! 🌟
