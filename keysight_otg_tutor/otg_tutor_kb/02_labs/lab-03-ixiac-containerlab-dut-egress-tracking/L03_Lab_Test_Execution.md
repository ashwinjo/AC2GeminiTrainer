---
title: "Lab 3 Test Execution"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Execute egress tracking tests with Nokia SRL DUT validation, VLAN tracking, and QoS policy verification."
tags: ["execution", "test", "snappi", "python", "egress-tracking", "dut", "containerlab"]
difficulty: "advanced"
---

# Lab 03: Test Execution with Egress Tracking

## 🚀 Step-by-Step Instructions to run DUT Egress Tracking Test

### Step 1: Deploy the ContainerLab Environment

First, deploy the complete testing infrastructure with Nokia SRL DUT:

```bash
# Deploy all containers including Nokia SRL DUT
sudo containerlab deploy -t lab-03.yml
```

**What this creates:**
- **Controller**: KENG controller on `clab-lab-03-controller:8443`
- **Traffic Engine 1**: `clab-lab-03-te1:5551`, Protocol Engine port `50071`
- **Traffic Engine 2**: `clab-lab-03-te2:5552`, Protocol Engine port `50071`
- **Protocol Engine 1**: Shares network with Traffic Engine 1
- **Protocol Engine 2**: Shares network with Traffic Engine 2
- **Nokia SRL DUT**: Pre-configured with VLAN sub-interfaces and QoS policies

### Step 2: Verify DUT Configuration

Connect to the Nokia SRL DUT to verify the configuration is loaded correctly:

```bash
# Connect to Nokia SRL (password: NokiaSrl1!)
ssh admin@clab-lab-03-srl

# Enter CLI mode if not already there
sr_cli

# Verify interface configuration
show interface ethernet-1/1
show interface ethernet-1/2

# Check VLAN sub-interfaces
show interface ethernet-1/2.1
show interface ethernet-1/2.2  
show interface ethernet-1/2.3

# Verify QoS policies
show qos
```

**🔍 Key configuration elements to verify:**
- **e1-1**: 192.168.11.1/24 (untagged interface)
- **e1-2.1**: VLAN 101, 192.168.101.1/24
- **e1-2.2**: VLAN 102, 192.168.102.1/24
- **e1-2.3**: VLAN 103, 192.168.103.1/24
- **QoS Policy**: DSCP 10 → FC1 → DSCP 20 remarking

### Step 3: Configure Test Script for ContainerLab

Edit the test script to use ContainerLab container names:

```bash
# Edit the test script
vi lab-03-1_test.py
```

**🔧 Update the script with ContainerLab addresses:**
```python
# Set the KENG Controller address
api = snappi.api(location="https://clab-lab-03-controller:8443", verify=False)

# Set port locations for ContainerLab containers
p1 = c.ports.add(name="p1", location="clab-lab-03-te1:5551+clab-lab-03-te1:50071")
p2 = c.ports.add(name="p2", location="clab-lab-03-te2:5552+clab-lab-03-te2:50071")
```

> 🔧 **ContainerLab Naming Convention**: ContainerLab prefixes all container names with `clab-<topology-name>-`. Use these full names for proper container addressing.

### Step 4: Execute the VLAN Egress Tracking Test

Run the primary test script with VLAN ID tracking:

```bash
python3 lab-03-1_test.py
```

## 📋 Understanding the lab-03-1_test.py Script

### **Script Architecture Overview**
The `lab-03-1_test.py` script demonstrates **egress tracking** capabilities by monitoring how the Nokia SRL DUT transforms packets during transit.

### **Key Script Components:**

#### 🔧 **1. Device and Interface Configuration**
```python
# Key elements the script configures:
- Two OTG devices with sub-interface endpoints
- Device 1: Single interface (192.168.11.2/24)
- Device 2: Multiple sub-interfaces (VLAN 101, 102, 103)
- Nokia SRL DUT between devices performing transformations
```

**What happens:**
- **Port Mapping**: Connects to traffic engines via ContainerLab names
- **Device 1**: Single untagged interface connecting to SRL e1-1
- **Device 2**: Multiple VLAN sub-interfaces connecting to SRL e1-2
- **IP Configuration**: Proper subnet addressing for each VLAN
- **Flow Creation**: Untagged ingress → Tagged egress through DUT

#### 🎯 **2. Egress Tracking Configuration**
```python
# Egress packet structure definition
f.egress_packet.ethernet()                    # Expect Ethernet header
eg_vlan = f.egress_packet.add().vlan         # Expect VLAN header (added by DUT)
eg_ip = f.egress_packet.add().ipv4           # Expect IPv4 header

# Add metric tags for VLAN ID tracking
eg_vlan.id.metric_tags.add(name="vlanIdRx")
```

**What the script tracks:**
- **VLAN ID Insertion**: Monitors which VLAN IDs are added by the DUT
- **Traffic Distribution**: Tracks packet distribution across sub-interfaces
- **Transformation Validation**: Verifies DUT performs expected VLAN tagging

#### 🌐 **3. Traffic Generation and Validation**
```python
# Traffic pattern:
- Source: Device 1 (untagged, 192.168.11.2)
- Destination: Device 2 sub-interfaces (VLAN-tagged)
- DSCP Values: [10, 14, 22, 24] for QoS testing
- Packet Count: 1000 packets at 100 pps
```

**What the script validates:**
- **Packet Reception**: All packets received on tagged interfaces
- **VLAN Distribution**: Traffic spread across VLANs 101, 102, 103
- **Egress Tracking Data**: Tagged metrics showing VLAN ID breakdown

### **Expected Test Results:**

#### **VLAN Tracking Output:**
```
Flow Metrics
Name            State           Frames Tx       Frames Rx       
f1              stopped         1000            1000            

Tagged Metrics (VLAN ID Tracking)
Tracked Value   Frames Rx       FPS Rx          Bytes Rx        
65 (VLAN 101)   333             0               42624           
66 (VLAN 102)   333             0               42624           
67 (VLAN 103)   334             0               42752           
```

**🧠 Understanding the results:**
- **Tracked Value 65**: Hex for VLAN ID 101
- **Tracked Value 66**: Hex for VLAN ID 102  
- **Tracked Value 67**: Hex for VLAN ID 103
- **Distribution**: Roughly equal traffic across all three VLANs

## 🔬 Advanced Testing: DSCP Egress Tracking

### Step 5: Create DSCP Tracking Test

Create a modified version to track DSCP remarking:

```bash
# Create a copy for DSCP tracking
cp lab-03-1_test.py lab-03-2_test.py

# Edit the new script
vi lab-03-2_test.py
```

**🔧 Modify for DSCP tracking:**
```python
# Comment out VLAN tracking
# eg_vlan.id.metric_tags.add(name="vlanIdRx")

# Enable DSCP tracking instead
eg_ip.priority.dscp.metric_tags.add(name="dscpValuesRx")
```

> ⚠️ **Egress Tracking Limitation**: Due to 12-bit limit, you cannot track both VLAN ID (12 bits) and DSCP (6 bits) simultaneously as this would require 18 bits total.

### Step 6: Execute DSCP Tracking Test

Run the DSCP tracking test:

```bash
python3 lab-03-2_test.py
```

**Expected DSCP Tracking Results:**
```
Tagged Metrics (DSCP Tracking)
Tracked Value   Frames Rx       Percentage      Description
14 (0x0E)      250             25%             DSCP 20 (remarked from 10)
00 (0x00)      250             25%             DSCP 0 (remarked from 14)
00 (0x00)      250             25%             DSCP 0 (remarked from 22)
00 (0x00)      250             25%             DSCP 0 (remarked from 24)
```

**🧠 Understanding DSCP remarking:**
- **75% of packets**: Remarked to DSCP 0 (default policy)
- **25% of packets**: DSCP 10 → DSCP 20 (specific QoS policy)
- **QoS Policy**: Only DSCP 10 gets special treatment (FC1 → DSCP 20)

## 🔧 Advanced DUT Configuration Testing

### Step 7: Modify QoS Policy on DUT

Test dynamic configuration changes by modifying the Nokia SRL QoS policy:

```bash
# Connect to Nokia SRL
ssh admin@clab-lab-03-srl

# Enter configuration mode
enter candidate

# Change QoS policy to remark FC1 to DSCP 30 (AF33)
set qos rewrite-rules dscp-policy test-rewrite map FC1 dscp 30

# Commit the change
commit now

# Exit configuration
quit
```

### Step 8: Re-run DSCP Test with Modified Policy

Execute the DSCP test again to see the policy change:

```bash
python3 lab-03-2_test.py
```

**Expected results with modified policy:**
```
Tagged Metrics (DSCP Tracking)
Tracked Value   Frames Rx       Percentage      Description
1E (0x1E)      250             25%             DSCP 30 (remarked from 10)
00 (0x00)      750             75%             DSCP 0 (other values)
```

**🧠 Validation of dynamic policy changes:**
- **Policy Change Verified**: DSCP 10 now remarked to DSCP 30
- **Real-time Testing**: Egress tracking immediately reflects DUT changes
- **Percentage Analysis**: 25% of packets (DSCP 10) get special remarking

## 🔍 Troubleshooting Common Issues

### **Container Connectivity Issues:**
```bash
# Check container status
sudo containerlab inspect -t lab-03.yml

# Verify container logs
docker logs clab-lab-03-te1
docker logs clab-lab-03-te2
```

### **DUT Configuration Issues:**
```bash
# Verify Nokia SRL interfaces
ssh admin@clab-lab-03-srl
show interface
show qos

# Check for interface errors
show log
```

### **Egress Tracking Issues:**
- **No tagged metrics**: Verify egress packet structure matches actual DUT output
- **Incorrect tracking values**: Check DUT configuration and packet transformations
- **Bit limit exceeded**: Reduce tracked fields to stay within 12-bit limit

### **MAC Address Resolution Errors:**
If you encounter MAC address resolution errors:
```bash
# Wait a moment and retry
sleep 10
python3 lab-03-1_test.py

# Or check ARP resolution on DUT
ssh admin@clab-lab-03-srl
show arp
```

## 📊 Test Result Analysis

### **Successful Test Indicators:**
- ✅ All 1000 packets transmitted and received
- ✅ Tagged metrics showing VLAN ID distribution (101, 102, 103)
- ✅ DSCP remarking validation showing policy compliance
- ✅ Traffic distribution across multiple sub-interfaces
- ✅ Zero packet loss through DUT

### **Egress Tracking Validation:**
- **VLAN Tracking**: Confirms DUT adds correct VLAN tags
- **DSCP Tracking**: Validates QoS policies are applied correctly  
- **Distribution Analysis**: Shows load balancing across sub-interfaces
- **Real-time Monitoring**: Live tracking during test execution

### **DUT Functionality Verification:**
- **VLAN Sub-interfaces**: Working correctly with proper tagging
- **QoS Policies**: DSCP remarking applied as configured
- **Routing**: Traffic properly distributed across interfaces
- **Performance**: No packet loss through DUT processing

## 🎯 Key Learning Points

### **Egress Tracking Benefits:**
- **Automated Validation**: No manual packet capture analysis needed
- **Real-time Monitoring**: Live tracking during test execution
- **Statistical Analysis**: Detailed breakdown by tracked field values
- **DUT Verification**: Validates network device transformations automatically

### **DUT Testing Methodology:**
- **Configuration Verification**: Always verify DUT config before testing
- **Dynamic Testing**: Test configuration changes in real-time
- **Multi-field Analysis**: Track different packet fields separately due to bit limitations
- **Correlation**: Use egress tracking with packet captures for comprehensive analysis

---

**Next Step**: Proceed to L03_Lab_Metrics.md to learn advanced egress tracking analysis and correlation techniques.