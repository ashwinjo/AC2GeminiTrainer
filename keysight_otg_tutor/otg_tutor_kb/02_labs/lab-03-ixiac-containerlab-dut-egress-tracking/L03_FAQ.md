---
title: "Lab 3 Frequently Asked Questions"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Common questions and troubleshooting for IxiaC-CONTAINERLAB-DUT-EGRESS-TRACKING scenarios."
tags: ["faq", "troubleshooting", "containerlab", "dut", "egress-tracking"]
difficulty: "intermediate"
---

# Lab 03: Frequently Asked Questions

## 🎯 General Questions

### Q1: What makes Lab 03 different from previous labs?
**A:** Lab 03 introduces a **real network device (Nokia SRL DUT)** and **egress tracking** capabilities. Unlike Labs 01-02 which used back-to-back connections, Lab 03 validates how network devices transform packets (VLAN tagging, QoS remarking) using automated tracking.

### Q2: What is egress tracking and why is it important?
**A:** Egress tracking automatically monitors how packets are modified as they traverse network devices. It's crucial for:
- Validating QoS policies (DSCP remarking)
- Verifying VLAN operations (tag insertion/modification)
- Troubleshooting packet transformations
- Automated DUT validation without manual packet capture

### Q3: What's the 12-bit limitation in egress tracking?
**A:** OTG/KENG reserves 12 bits for egress tracking fields. This means:
- VLAN ID alone uses 12 bits (can track solo)
- DSCP uses 6 bits (can combine with other 6-bit fields)
- VLAN (12) + DSCP (6) = 18 bits (exceeds limit - not possible)

## 🔧 Technical Questions

### Q4: Why use ContainerLab instead of Docker Compose?
**A:** ContainerLab is designed for network topology orchestration:
- **Network device support**: Handles Nokia SRL and other network equipment
- **Complex topologies**: Better interface management and connections
- **Network-specific features**: Built for networking scenarios, not just applications

### Q5: How do I interpret hex values in tagged metrics?
**A:** Tagged metrics show values in hexadecimal:
- **0x65** = 101 decimal (VLAN ID 101)
- **0x66** = 102 decimal (VLAN ID 102)
- **0x14** = 20 decimal (DSCP 20)
- Use `int(value, 16)` in Python to convert hex to decimal

### Q6: What happens if egress packet definition doesn't match reality?
**A:** If the egress packet structure doesn't match what the DUT actually sends:
- No tagged metrics will be collected
- Test may show zero egress tracking data
- Need to adjust egress packet definition to match DUT behavior

## 🚨 Troubleshooting

### Q7: "MAC address resolution error" - what does this mean?
**A:** This indicates ARP resolution issues between OTG and DUT:
```bash
# Wait and retry
sleep 10
python3 lab-03-1_test.py

# Check ARP on DUT
ssh admin@clab-lab-03-srl
show arp
```

### Q8: Containers won't start or ContainerLab fails?
**A:** Common solutions:
```bash
# Ensure sudo privileges
sudo -v

# Check for port conflicts
netstat -tulpn | grep 8443

# Clean up previous deployments
sudo containerlab destroy -t lab-03.yml --cleanup

# Redeploy
sudo containerlab deploy -t lab-03.yml
```

### Q9: No tagged metrics appearing in results?
**A:** Check these items:
1. **Egress packet structure**: Must match DUT output format
2. **Metric tags**: Ensure properly configured
3. **DUT configuration**: Verify DUT is actually transforming packets
4. **Bit limits**: Ensure tracked fields don't exceed 12 bits

### Q10: Nokia SRL not responding or configuration not loaded?
**A:** Troubleshooting steps:
```bash
# Check SRL container status
docker logs clab-lab-03-srl

# Verify configuration loaded
ssh admin@clab-lab-03-srl
show configuration

# Restart if needed
sudo containerlab destroy -t lab-03.yml
sudo containerlab deploy -t lab-03.yml
```

## 🔍 Configuration Questions

### Q11: How do I modify QoS policies on Nokia SRL?
**A:** Connect to SRL and use configuration mode:
```bash
ssh admin@clab-lab-03-srl  # Password: NokiaSrl1!
enter candidate
set qos rewrite-rules dscp-policy test-rewrite map FC1 dscp 30
commit now
quit
```

### Q12: Can I track both VLAN and DSCP simultaneously?
**A:** No, due to bit limitations:
- VLAN ID requires 12 bits
- DSCP requires 6 bits  
- Total: 18 bits (exceeds 12-bit limit)
- Must choose one or use smaller custom fields

### Q13: How do I validate traffic distribution across VLANs?
**A:** Use statistical analysis of tagged metrics:
```python
total_packets = sum(t.frames_rx for t in tagged_metrics)
for t in tagged_metrics:
    vlan_id = int(t.tags[0].value.hex, 16)
    percentage = (t.frames_rx / total_packets) * 100
    print(f"VLAN {vlan_id}: {percentage:.1f}%")
```

## 📊 Results Interpretation

### Q14: What does "75% remarked" mean in DSCP tracking?
**A:** In the QoS policy:
- Only DSCP 10 gets remarked to DSCP 20 (25% of traffic)
- Other DSCP values (14, 22, 24) get remarked to DSCP 0 (75% of traffic)
- This validates the QoS policy is working correctly

### Q15: How do I know if the test was successful?
**A:** Success indicators:
- ✅ Zero packet loss (frames_tx = frames_rx)
- ✅ Tagged metrics show expected VLAN IDs (101, 102, 103)
- ✅ DSCP remarking percentages match policy (25% DSCP 20)
- ✅ Even traffic distribution across VLANs (±10%)

### Q16: What if traffic distribution is uneven?
**A:** Uneven distribution could indicate:
- DUT load balancing algorithm behavior
- Hash-based distribution (normal for some scenarios)
- Configuration issues with sub-interfaces
- Need to analyze over longer test duration

## 🔄 Advanced Usage

### Q17: Can I use this with other DUT vendors?
**A:** Yes! The egress tracking concepts apply to any DUT:
- Adjust ContainerLab topology for different vendors
- Modify DUT configuration procedures
- Update egress packet definitions for vendor-specific behaviors

### Q18: How do I create custom packet transformations to test?
**A:** Modify the Nokia SRL configuration:
- Add new QoS classes and policies
- Create additional VLAN sub-interfaces
- Implement custom packet marking rules
- Test with different DSCP values

### Q19: Can I automate the entire test process?
**A:** Absolutely! Create automation scripts that:
- Deploy ContainerLab topology
- Configure DUT policies
- Execute multiple test scenarios
- Collect and analyze results
- Generate reports automatically

---

**💡 Pro Tips:**
- Always verify DUT configuration before testing
- Use packet capture to validate egress tracking results
- Start with single-field tracking before attempting multi-field
- Monitor container resources during long tests
- Save interesting DUT configurations for future analysis

**Need more help?** Check L03_Troubleshooting.md for detailed issue resolution guides!