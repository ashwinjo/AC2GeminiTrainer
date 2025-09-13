# L03: Egress Tracking in OTG/KENG

## 🎯 What is Egress Tracking?

**Egress Tracking** is a powerful feature in OTG/KENG that allows you to monitor and analyze how packets are modified as they traverse through network devices (DUTs - Devices Under Test). It enables you to track specific packet fields on the receiving side and compare them with what was originally transmitted.

### Core Concept
Think of egress tracking as a "packet detective" that follows your traffic through the network and reports back on any changes that occurred during transit. This is crucial for:
- **QoS Validation**: Verifying DSCP markings are correctly applied
- **VLAN Operations**: Tracking VLAN tag additions, modifications, or removals  
- **Network Function Testing**: Ensuring DUTs perform expected packet transformations
- **Troubleshooting**: Identifying where and how packets are being modified

## 🏗️ How Egress Tracking Works in OTG/KENG

### Traditional Flow Metrics vs. Egress Tracking

**Traditional Flow Metrics:**
```
[TX Port] → [DUT] → [RX Port]
     ↓                  ↓
  Tx Stats          Rx Stats
  (frames_tx)      (frames_rx)
```

**With Egress Tracking:**
```
[TX Port] → [DUT] → [RX Port]
     ↓         ↓         ↓
  Tx Stats   Packet    Rx Stats + 
             Changes   Tagged Metrics
                      (per tracked field)
```

### Key Components

1. **Egress Packet Definition**: Defines the expected packet structure on the receive side
2. **Metric Tags**: Specific fields you want to track (VLAN ID, DSCP, etc.)
3. **Tagged Metrics**: Statistics broken down by tracked field values
4. **Comparison Logic**: Automatic analysis of transmitted vs. received packet fields

## 🔧 OTG API Implementation

### Basic Egress Tracking Configuration

```python
import snappi

# Create flow configuration
f = c.flows.add()
f.name = "egress_tracking_flow"
f.metrics.enable = True

# Define the transmitted packet structure
f_eth = f.packet.add().ethernet
f_ip = f.packet.add().ipv4
f_ip.priority.dscp.phb.values = [10, 14, 22, 24]  # Original DSCP values

# Configure egress tracking - define expected receive packet structure
f.egress_packet.ethernet()  # Expect Ethernet header
eg_vlan = f.egress_packet.add().vlan  # Expect VLAN header (added by DUT)
eg_ip = f.egress_packet.add().ipv4    # Expect IPv4 header

# Add metric tags to track specific fields
eg_vlan.id.metric_tags.add(name="vlanIdRx")  # Track VLAN ID changes
eg_ip.priority.dscp.metric_tags.add(name="dscpValuesRx")  # Track DSCP changes
```

### Lab 03 Implementation Example

From the Lab 03 test script (`lab-03-1_test.py`):

```python
def otg_config(api, tc):
    # ... port and device configuration ...
    
    f = c.flows.add()
    f.name = "f1"
    f.metrics.enable = True
    
    # Original packet with DSCP values
    f_ip = f.packet.add().ipv4
    f_ip.priority.dscp.phb.values = [10, 14, 22, 24]
    
    # Egress tracking configuration
    f.egress_packet.ethernet()
    eg_vlan = f.egress_packet.add().vlan
    eg_ip = f.egress_packet.add().ipv4
    
    # Track VLAN ID on received packets
    eg_vlan.id.metric_tags.add(name="vlanIdRx")
    
    return c
```

## 📊 Analyzing Egress Tracking Results

### Tagged Metrics Structure

When egress tracking is enabled, you receive additional metrics beyond standard flow statistics:

```python
def get_flow_metrics(api):
    metrics = api.get_metrics(req).flow_metrics
    
    for m in metrics:
        # Standard flow metrics
        print(f"Frames TX: {m.frames_tx}")
        print(f"Frames RX: {m.frames_rx}")
        
        # Tagged metrics from egress tracking
        if len(m.tagged_metrics) > 0:
            for t in m.tagged_metrics:
                tracked_value = t.tags[0].value.hex
                print(f"Tracked Value: {tracked_value}")
                print(f"Frames RX for this value: {t.frames_rx}")
                print(f"Bytes RX for this value: {t.bytes_rx}")
```

### Sample Output

```
Flow Metrics
Name            State           Frames Tx       Frames Rx       
f1              stopped         1000            1000            

Tagged Metrics  
Tracked Value   Frames Rx       FPS Rx          Bytes Rx        
65              250             0               32000           
66              250             0               32000           
67              250             0               32000           
68              250             0               32000           
```

## 🌟 Practical Use Cases

### 1. QoS DSCP Remarking Validation

**Scenario**: Verify that a router correctly remarks DSCP values based on QoS policies.

```python
# Send traffic with DSCP 10, expect DUT to remark to DSCP 20
f_ip.priority.dscp.phb.values = [10]

# Track received DSCP values
eg_ip.priority.dscp.metric_tags.add(name="dscpRemarked")

# Analysis: Verify all packets received have DSCP 20
```

### 2. VLAN Tag Insertion/Modification

**Scenario**: Test that an access port correctly adds VLAN tags.

```python
# Send untagged traffic
f_eth = f.packet.add().ethernet

# Expect VLAN tag to be added by DUT
eg_vlan = f.egress_packet.add().vlan
eg_vlan.id.metric_tags.add(name="insertedVlan")

# Analysis: Verify correct VLAN ID was inserted
```

### 3. Load Balancing Verification

**Scenario**: Ensure traffic is distributed across multiple paths/VLANs.

```python
# Send single flow
f.tx_rx.device.set(tx_names=[d1_ip.name], rx_names=rx_endpoints)

# Track which VLAN each packet egresses on
eg_vlan.id.metric_tags.add(name="loadBalanceVlan")

# Analysis: Verify traffic distribution across VLANs
```

## 🔍 Lab 03 Specific Implementation

### Test Topology
```
[OTG Port 1] → [Nokia SRL DUT] → [OTG Port 2 - Multiple Sub-interfaces]
     ↓              ↓                        ↓
  Untagged      QoS Policy +             Tagged Traffic
  Traffic       VLAN Tagging             (VLAN 101-103)
```

### DUT Configuration Impact
The Nokia SRL configuration in `lab-03-srl.cfg` shows:
- **QoS Classifier**: DSCP 10 → Forwarding Class FC1
- **QoS Rewrite**: FC1 → DSCP 20 (remarking)
- **VLAN Subinterfaces**: 101, 102, 103 with different IP subnets

### Expected Egress Tracking Results
1. **VLAN Tracking**: Packets should be received with VLAN IDs 101, 102, or 103
2. **DSCP Tracking**: Original DSCP 10 should be remarked to DSCP 20
3. **Distribution**: Traffic should be distributed across the three sub-interfaces

## 🚀 Advanced Features

### 1. Multiple Field Tracking
```python
# Track both VLAN and DSCP simultaneously
eg_vlan.id.metric_tags.add(name="vlanId")
eg_ip.priority.dscp.metric_tags.add(name="dscpValue")
```

### 2. Custom Packet Structures
```python
# Track custom headers or protocols
eg_custom = f.egress_packet.add().custom
eg_custom.bytes = "0x1234"
eg_custom.metric_tags.add(name="customField")
```

### 3. Statistical Analysis
```python
# Analyze distribution and detect anomalies
def analyze_distribution(tagged_metrics):
    total_packets = sum(t.frames_rx for t in tagged_metrics)
    for t in tagged_metrics:
        percentage = (t.frames_rx / total_packets) * 100
        print(f"Value {t.tags[0].value.hex}: {percentage:.2f}%")
```

## 🎯 Benefits in Network Testing

### 1. **Comprehensive Validation**
- Verify not just connectivity, but correct packet processing
- Ensure DUTs perform expected transformations
- Validate complex QoS and VLAN policies

### 2. **Automated Testing**
- No need for manual packet captures
- Real-time statistics during test execution
- Programmatic analysis of results

### 3. **Troubleshooting Power**
- Identify exactly which packets are affected
- Pinpoint specific field modifications
- Correlate issues with traffic patterns

### 4. **Scale and Performance**
- Track millions of packets in real-time
- Minimal performance impact on traffic generation
- Detailed statistics without packet capture overhead

## 🔧 Best Practices

### 1. **Design Considerations**
- Define egress packet structure to match expected DUT behavior
- Use meaningful metric tag names for clarity
- Consider the number of unique values to avoid metric explosion

### 2. **Performance Optimization**
- Limit the number of tracked fields to essential ones
- Use appropriate packet rates to ensure accurate tracking
- Monitor memory usage with large numbers of unique values

### 3. **Test Design**
- Start with simple single-field tracking
- Gradually add complexity as understanding increases
- Validate tracking configuration with known packet modifications

## 📚 Integration with OTG Ecosystem

Egress tracking seamlessly integrates with other OTG/KENG features:
- **Protocol Emulation**: Track packets through BGP, OSPF route changes
- **Traffic Shaping**: Verify QoS queue assignments and priority handling  
- **Multi-Port Testing**: Compare egress behavior across different DUT ports
- **Statistics Collection**: Combine with standard flow metrics for comprehensive analysis

This powerful capability makes OTG/KENG an ideal platform for modern network testing, providing visibility into packet-level transformations that traditional tools simply cannot match.
