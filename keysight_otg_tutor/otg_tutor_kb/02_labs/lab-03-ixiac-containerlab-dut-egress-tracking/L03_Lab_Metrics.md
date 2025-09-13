---
title: "Lab 3 Metrics Collection and Analysis"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Comprehensive metrics collection, egress tracking analysis, and DUT performance validation for Lab 3."
tags: ["metrics", "analysis", "egress-tracking", "tagged-metrics", "dut-validation", "performance"]
difficulty: "advanced"
---

# Lab 03: Metrics Collection and Egress Tracking Analysis

## 🎯 Overview
Lab 03 introduces **advanced metrics collection** with a focus on **egress tracking** and **DUT validation**. Unlike previous labs that focused on basic flow metrics, Lab 03 provides:
- **Tagged metrics** for field-specific analysis (VLAN ID, DSCP values)
- **DUT transformation validation** through automated tracking
- **Statistical analysis** of traffic distribution patterns
- **Real-time monitoring** of packet modifications
- **Correlation techniques** between different metric types

## 📊 Metrics Collection Methods

### Method 1: Real-time Egress Tracking During Test Execution

Monitor egress tracking metrics while the test is running:

```bash
# Run test with verbose egress tracking output
python3 lab-03-1_test.py

# The script automatically displays:
# - Standard flow metrics (TX/RX counters)
# - Tagged metrics (per VLAN ID breakdown)
# - Real-time statistics during execution
```

**🧠 Understanding the output:**
```
Flow Metrics
Name            State           Frames Tx       Frames Rx       FPS Tx          FPS Rx
f1              stopped         1000            1000            0               0

Tagged Metrics (VLAN ID Tracking)
Tracked Value   Frames Rx       FPS Rx          Bytes Rx        
65              333             0               42624           
66              333             0               42624           
67              334             0               42752           
```

**Key insights:**
- **Tracked Value 65**: Hex representation of VLAN ID 101
- **Tracked Value 66**: Hex representation of VLAN ID 102
- **Tracked Value 67**: Hex representation of VLAN ID 103
- **Distribution**: Traffic evenly distributed across all three VLANs

### Method 2: OTG API Metrics Query

Query detailed metrics using the OTG API:

```python
# Example API query for comprehensive metrics
import snappi

api = snappi.api(location="https://clab-lab-03-controller:8443", verify=False)

# Request flow metrics
req = api.metrics_request()
req.flow.flow_names = []  # Empty list gets all flows

# Get comprehensive metrics
metrics = api.get_metrics(req).flow_metrics

for m in metrics:
    print(f"Flow: {m.name}")
    print(f"TX Frames: {m.frames_tx}, RX Frames: {m.frames_rx}")
    print(f"TX Bytes: {m.bytes_tx}, RX Bytes: {m.bytes_rx}")
    
    # Egress tracking specific metrics
    if len(m.tagged_metrics) > 0:
        print("\nTagged Metrics:")
        for t in m.tagged_metrics:
            tracked_value = t.tags[0].value.hex
            print(f"Value {tracked_value}: {t.frames_rx} frames, {t.bytes_rx} bytes")
```

### Method 3: Container-level Network Statistics

Monitor network statistics at the container level:

```bash
# Check Traffic Engine 1 interface statistics
docker exec -it clab-lab-03-te1 cat /proc/net/dev

# Check Traffic Engine 2 interface statistics  
docker exec -it clab-lab-03-te2 cat /proc/net/dev

# Monitor real-time interface counters
docker exec -it clab-lab-03-te1 watch -n 1 cat /proc/net/dev
```

### Method 4: Nokia SRL DUT Metrics

Collect metrics directly from the Nokia SRL DUT:

```bash
# Connect to Nokia SRL
ssh admin@clab-lab-03-srl

# Check interface statistics
show interface ethernet-1/1 statistics
show interface ethernet-1/2 statistics

# Check VLAN sub-interface statistics
show interface ethernet-1/2.1 statistics
show interface ethernet-1/2.2 statistics
show interface ethernet-1/2.3 statistics

# Check QoS statistics
show qos interface ethernet-1/1 output
show qos interface ethernet-1/2 output
```

## 🔍 Egress Tracking Analysis Techniques

### **1. VLAN ID Distribution Analysis**

Analyze how traffic is distributed across VLAN sub-interfaces:

```python
def analyze_vlan_distribution(tagged_metrics):
    """Analyze VLAN ID distribution from tagged metrics"""
    total_packets = sum(t.frames_rx for t in tagged_metrics)
    
    print("VLAN Distribution Analysis:")
    print("-" * 50)
    
    for t in tagged_metrics:
        vlan_id = int(t.tags[0].value.hex, 16)  # Convert hex to decimal
        percentage = (t.frames_rx / total_packets) * 100
        
        print(f"VLAN {vlan_id:3d}: {t.frames_rx:4d} packets ({percentage:5.1f}%)")
    
    # Check for even distribution (should be ~33.3% each)
    expected_per_vlan = total_packets / 3
    for t in tagged_metrics:
        vlan_id = int(t.tags[0].value.hex, 16)
        deviation = abs(t.frames_rx - expected_per_vlan)
        if deviation > expected_per_vlan * 0.1:  # More than 10% deviation
            print(f"⚠️  VLAN {vlan_id} has uneven distribution!")
```

### **2. DSCP Remarking Validation**

Validate QoS DSCP remarking policies:

```python
def analyze_dscp_remarking(tagged_metrics, original_dscp_values):
    """Analyze DSCP remarking results"""
    total_packets = sum(t.frames_rx for t in tagged_metrics)
    
    print("DSCP Remarking Analysis:")
    print("-" * 50)
    
    dscp_mapping = {
        0: "Best Effort (0)",
        10: "AF11 (10)", 
        14: "AF12 (14)",
        20: "AF22 (20)",
        22: "AF23 (22)",
        24: "AF24 (24)",
        30: "AF33 (30)"
    }
    
    for t in tagged_metrics:
        dscp_value = int(t.tags[0].value.hex, 16) >> 2  # DSCP is upper 6 bits
        percentage = (t.frames_rx / total_packets) * 100
        dscp_name = dscp_mapping.get(dscp_value, f"Unknown ({dscp_value})")
        
        print(f"DSCP {dscp_value:2d} ({dscp_name}): {t.frames_rx:4d} packets ({percentage:5.1f}%)")
    
    # Validate expected remarking (25% DSCP 10→20, 75% others→0)
    if any(int(t.tags[0].value.hex, 16) >> 2 == 20 for t in tagged_metrics):
        dscp_20_count = next(t.frames_rx for t in tagged_metrics if int(t.tags[0].value.hex, 16) >> 2 == 20)
        expected_dscp_20 = total_packets * 0.25  # 25% should be remarked
        if abs(dscp_20_count - expected_dscp_20) < expected_dscp_20 * 0.1:
            print("✅ DSCP remarking policy working correctly")
        else:
            print("⚠️  DSCP remarking policy may have issues")
```

### **3. Traffic Pattern Analysis**

Analyze traffic patterns and identify anomalies:

```python
def analyze_traffic_patterns(flow_metrics, tagged_metrics):
    """Comprehensive traffic pattern analysis"""
    
    print("Traffic Pattern Analysis:")
    print("=" * 60)
    
    # Basic flow analysis
    for m in flow_metrics:
        packet_loss = m.frames_tx - m.frames_rx
        loss_percentage = (packet_loss / m.frames_tx) * 100 if m.frames_tx > 0 else 0
        
        print(f"Flow: {m.name}")
        print(f"  TX: {m.frames_tx} packets, {m.bytes_tx} bytes")
        print(f"  RX: {m.frames_rx} packets, {m.bytes_rx} bytes")
        print(f"  Loss: {packet_loss} packets ({loss_percentage:.2f}%)")
        
        # Egress tracking analysis
        if len(m.tagged_metrics) > 0:
            print(f"  Tagged Fields: {len(m.tagged_metrics)} unique values")
            
            # Check for missing or unexpected values
            expected_values = {101, 102, 103}  # Expected VLAN IDs
            actual_values = {int(t.tags[0].value.hex, 16) for t in m.tagged_metrics}
            
            missing = expected_values - actual_values
            unexpected = actual_values - expected_values
            
            if missing:
                print(f"  ⚠️  Missing expected values: {missing}")
            if unexpected:
                print(f"  ⚠️  Unexpected values found: {unexpected}")
            if not missing and not unexpected:
                print(f"  ✅ All expected values present")
```

## 📈 Performance Metrics and Benchmarking

### **DUT Performance Impact Analysis**

Measure the performance impact of DUT processing:

```python
def analyze_dut_performance(flow_metrics):
    """Analyze DUT performance impact"""
    
    print("DUT Performance Analysis:")
    print("-" * 40)
    
    for m in flow_metrics:
        # Calculate throughput
        if m.frames_tx > 0:
            avg_packet_size = m.bytes_tx / m.frames_tx
            throughput_mbps = (m.bytes_rx * 8) / (1000000 * test_duration_seconds)
            
            print(f"Average Packet Size: {avg_packet_size:.1f} bytes")
            print(f"Throughput: {throughput_mbps:.2f} Mbps")
            
            # Check for performance degradation
            if m.frames_rx < m.frames_tx:
                loss_rate = (m.frames_tx - m.frames_rx) / m.frames_tx
                if loss_rate > 0.001:  # More than 0.1% loss
                    print(f"⚠️  Significant packet loss: {loss_rate:.3f}%")
                else:
                    print(f"✅ Minimal packet loss: {loss_rate:.6f}%")
```

### **Egress Tracking Overhead Analysis**

Measure the impact of egress tracking on performance:

```bash
# Compare test execution time with and without egress tracking

# Test with egress tracking
time python3 lab-03-1_test.py

# Test without egress tracking (comment out metric tags)
time python3 lab-03-1_test_no_tracking.py
```

## 🔄 Real-time Monitoring Techniques

### **Continuous Metrics Collection**

Set up continuous monitoring during long-running tests:

```python
import time
import threading

def continuous_metrics_monitor(api, interval_seconds=5):
    """Monitor metrics continuously during test execution"""
    
    def monitor_loop():
        while monitoring_active:
            req = api.metrics_request()
            req.flow.flow_names = []
            metrics = api.get_metrics(req).flow_metrics
            
            timestamp = time.strftime("%H:%M:%S")
            print(f"\n[{timestamp}] Current Metrics:")
            
            for m in metrics:
                print(f"  {m.name}: TX={m.frames_tx}, RX={m.frames_rx}")
                
                if len(m.tagged_metrics) > 0:
                    for t in m.tagged_metrics:
                        value = t.tags[0].value.hex
                        print(f"    Tag {value}: {t.frames_rx} packets")
            
            time.sleep(interval_seconds)
    
    monitoring_active = True
    monitor_thread = threading.Thread(target=monitor_loop)
    monitor_thread.start()
    
    return monitor_thread
```

## 🎯 Metrics Validation and Success Criteria

### **Automated Validation Functions**

Create automated validation for test success:

```python
def validate_test_results(flow_metrics, expected_criteria):
    """Automated validation of test results"""
    
    validation_results = {
        "packet_loss": False,
        "vlan_distribution": False,
        "dscp_remarking": False,
        "overall_success": False
    }
    
    for m in flow_metrics:
        # Check packet loss
        loss_rate = (m.frames_tx - m.frames_rx) / m.frames_tx if m.frames_tx > 0 else 0
        validation_results["packet_loss"] = loss_rate < 0.001  # Less than 0.1%
        
        # Check VLAN distribution
        if len(m.tagged_metrics) >= 3:  # Should have 3 VLANs
            vlan_counts = [t.frames_rx for t in m.tagged_metrics]
            avg_count = sum(vlan_counts) / len(vlan_counts)
            max_deviation = max(abs(count - avg_count) for count in vlan_counts)
            validation_results["vlan_distribution"] = max_deviation < avg_count * 0.1
        
        # Check DSCP remarking (if tracking DSCP)
        if "dscp" in expected_criteria:
            dscp_20_found = any(int(t.tags[0].value.hex, 16) >> 2 == 20 for t in m.tagged_metrics)
            validation_results["dscp_remarking"] = dscp_20_found
    
    # Overall success
    validation_results["overall_success"] = all([
        validation_results["packet_loss"],
        validation_results["vlan_distribution"]
    ])
    
    return validation_results
```

## 📋 Metrics Collection Best Practices

### **1. Collection Timing**
- Collect baseline metrics before test execution
- Monitor metrics during test execution for real-time validation
- Collect final metrics after test completion for comprehensive analysis

### **2. Data Correlation**
- Correlate OTG metrics with DUT interface statistics
- Compare egress tracking results with packet captures
- Validate tagged metrics against expected DUT behavior

### **3. Performance Monitoring**
- Monitor container resource usage during tests
- Track egress tracking overhead impact
- Measure DUT processing latency and throughput

### **4. Error Detection**
- Set thresholds for acceptable packet loss rates
- Monitor for unexpected egress tracking values
- Detect traffic distribution anomalies automatically

---

**🎯 Success Criteria for Lab 03:**
- ✅ Zero packet loss through DUT (< 0.1% acceptable)
- ✅ Even traffic distribution across all 3 VLAN sub-interfaces (±10%)
- ✅ Correct DSCP remarking: 25% of packets DSCP 10→20, 75% others→0
- ✅ All expected VLAN IDs present in egress tracking (101, 102, 103)
- ✅ Tagged metrics correlate with packet capture analysis
- ✅ DUT performance within acceptable limits (no significant latency)

**Next Step**: Proceed to L03_Challenge.md to explore advanced egress tracking scenarios and custom analysis techniques.