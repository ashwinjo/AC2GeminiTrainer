---
title: "Lab 3 Challenge - Advanced Egress Tracking Scenarios"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Practice advanced egress tracking configurations, multi-field analysis, and complex DUT validation scenarios."
tags: ["challenge", "modification", "egress-tracking", "dut", "advanced", "multi-field"]
difficulty: "advanced"
---

# Lab 03: Advanced Egress Tracking Challenge

## 🚀 Challenge Overview

Test your mastery of egress tracking with these advanced scenarios that push the boundaries of DUT validation and packet analysis.

## Challenge 1: Multi-Field Egress Tracking

Create a test that tracks multiple packet fields while respecting the 12-bit limitation:

```bash
# Create challenge script
cp lab-03-1_test.py lab-03-challenge-1.py
vim lab-03-challenge-1.py
```

**Requirements:**
- Track DSCP values (6 bits) + Custom field (6 bits) = 12 bits total
- Implement statistical analysis of multi-field correlations
- Validate bit usage doesn't exceed limits

**Implementation:**
```python
# Track IP priority (DSCP + ECN) - 8 bits
eg_ip.priority.raw.metric_tags.add(name="ipPriorityRx", length=8)

# Add custom 4-bit field
eg_custom = f.egress_packet.add().custom
eg_custom.bytes = "0xF0"
eg_custom.metric_tags.add(name="customFieldRx", length=4)
```

## Challenge 2: Dynamic DUT Configuration Testing

Test egress tracking with real-time DUT configuration changes:

**Test Scenario:**
1. Run baseline egress tracking
2. Modify Nokia SRL QoS policies during test
3. Observe real-time egress tracking changes
4. Validate policy changes are reflected immediately

**DUT Changes:**
```bash
ssh admin@clab-lab-03-srl
enter candidate
set qos rewrite-rules dscp-policy test-rewrite map FC1 dscp 30
commit now
```

## Challenge 3: Advanced Statistical Analysis

Implement comprehensive statistical analysis:

**Required Functions:**
- Distribution uniformity testing (Chi-square)
- Temporal pattern analysis
- Anomaly detection (outlier identification)
- Performance correlation analysis

## Challenge 4: Custom Validation Scenarios

**Scenario A: Load Balancing Validation**
```python
def validate_load_balancing(tagged_metrics, tolerance=0.1):
    """Validate even traffic distribution across VLANs"""
    total_packets = sum(t.frames_rx for t in tagged_metrics)
    expected_per_vlan = total_packets / len(tagged_metrics)
    
    for t in tagged_metrics:
        deviation = abs(t.frames_rx - expected_per_vlan) / expected_per_vlan
        if deviation > tolerance:
            return False
    return True
```

**Scenario B: QoS Compliance Testing**
- Validate DSCP remarking rates
- Check policy compliance percentages
- Identify policy violations

## Challenge 5: Performance Impact Analysis

Measure egress tracking overhead:

**Metrics to Compare:**
- CPU usage impact
- Memory consumption increase
- Test execution time difference
- Network performance impact

## 🎯 Assessment Questions

1. **Multi-field Tracking**: How does the 12-bit limitation affect complex packet analysis?

2. **Dynamic Testing**: What challenges arise when modifying DUT configuration during active tests?

3. **Statistical Insights**: What patterns emerged that basic metrics couldn't reveal?

4. **Performance Trade-offs**: How significant is egress tracking overhead versus benefits?

5. **Real-world Application**: How would you apply these techniques in production testing?

## ✅ Success Criteria

- ✅ All 5 challenges completed successfully
- ✅ Multi-field tracking within bit limits
- ✅ Dynamic configuration testing working
- ✅ Statistical analysis providing insights
- ✅ Performance impact documented

**Advanced Achievement:**
- 🌟 Innovative egress tracking applications
- 🌟 Automated analysis frameworks
- 🌟 Production-ready validation techniques

---

**🎯 Challenge Complete!**
Master these advanced egress tracking techniques to become an expert in sophisticated network device validation and automated testing frameworks.