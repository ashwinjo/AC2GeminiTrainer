---
title: "Lab 2 Metrics Collection"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Learn how to collect and analyze both protocol and traffic metrics from OTG test execution with protocol engines."
tags: ["metrics", "monitoring", "statistics", "analysis", "protocol", "bgp"]
difficulty: "intermediate"
---

# Lab 02: Metrics Collection with Protocol Statistics

## 🚀 Step-by-Step Instructions to get Protocol and Traffic Metrics

### Step 1: BGP Protocol Metrics Collection

Check BGP session establishment and route statistics:

```bash
# Query BGP protocol metrics
curl -k -d '{"choice":"bgpv4"}' -X POST https://127.0.0.1:8443/monitor/metrics
```

**What this shows:**
- BGP session states (Idle, Active, Established)
- Routes advertised and received counts
- BGP neighbor information
- Session establishment timing
- Protocol convergence status

### Step 2: Traffic Engine Metrics (Following L01 Pattern)

Following the same approach as Lab 01, collect traffic engine statistics:

```bash
# Get flow metrics (traffic statistics)
curl -k -d '{"choice":"flow"}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get port metrics (interface statistics)
curl -k -d '{"choice":"port"}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get specific port metrics
curl -k -d '{"choice":"port","port":{"port_names":["port1"]}}' -X POST https://127.0.0.1:8443/monitor/metrics
curl -k -d '{"choice":"port","port":{"port_names":["port2"]}}' -X POST https://127.0.0.1:8443/monitor/metrics
```

### Step 3: System-Level Interface Verification

Check network interface statistics at the system level:

```bash
# Save interface counters before test
cat /proc/net/dev > counters_before.log

# After test execution
cat /proc/net/dev > counters_after.log

# Compare interface statistics
diff counters_before.log counters_after.log

# Check specific veth interfaces
cat /proc/net/dev | grep veth
```

### Step 4: Protocol State Information

Query detailed protocol states and neighbor information:

```bash
# BGP neighbor states
curl -k -d '{"choice":"ipv4_neighbors"}' -X POST https://127.0.0.1:8443/monitor/states

# BGP prefix information
curl -k -d '{"choice":"bgp_prefixes"}' -X POST https://127.0.0.1:8443/monitor/states
```

## 📊 **Comprehensive Metrics Analysis**

### **BGP Protocol Metrics:**
- **Session State**: Established/Idle/Active/Connect
- **Routes Advertised**: Number of prefixes sent to peer
- **Routes Received**: Number of prefixes learned from peer
- **Session Flaps**: Connection stability indicators
- **Convergence Time**: Time to establish and exchange routes

### **Traffic Engine Metrics:**
- **Frames TX/RX**: Packet counts transmitted and received
- **Frame Loss**: Difference between TX and RX counts
- **Frame Rate**: Packets per second transmission rates
- **Byte Counts**: Total data transferred
- **Protocol-Aware Flows**: Traffic using BGP-learned routes

### **Analysis Questions:**
- **Q#04**: Which veth interfaces carried the protocol traffic?
- **Q#05**: Do BGP route counts match the configured 10,000 per peer?
- **Q#06**: Does traffic flow through BGP-learned routes show zero loss?
- **Q#07**: How long did BGP convergence take?
- **Q#08**: Are both BGP sessions in "Established" state?

## 🔍 **Advanced Monitoring Options**

### **Explore All Available Metrics**
For a complete list of available monitoring choices, refer to the official OTG OpenAPI documentation:

**📖 OpenAPI Reference**: [OTG Monitor API Documentation](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/open-traffic-generator/models/master/artifacts/openapi.yaml%23tag/Monitor/operation/get_states#tag/Monitor/operation/get_states)

This documentation shows all available `"choice"` options for the monitor endpoints, including:
- `"bgpv4"` - BGP version 4 metrics
- `"flow"` - Traffic flow statistics  
- `"port"` - Interface/port metrics
- `"ipv4_neighbors"` - IPv4 neighbor states
- `"bgp_prefixes"` - BGP route prefix information
- And many other protocol and traffic monitoring options

### **Real-Time Monitoring**
```bash
# Continuous BGP monitoring (updates every 5 seconds)
watch -n 5 'curl -s -k -d "{\"choice\":\"bgpv4\"}" -X POST https://127.0.0.1:8443/monitor/metrics'

# Combined protocol and traffic monitoring
watch -n 3 'echo "=== BGP STATUS ===" && curl -s -k -d "{\"choice\":\"bgpv4\"}" -X POST https://127.0.0.1:8443/monitor/metrics && echo -e "\n=== TRAFFIC STATUS ===" && curl -s -k -d "{\"choice\":\"flow\"}" -X POST https://127.0.0.1:8443/monitor/metrics'
```

## ✅ **Success Criteria Validation**

### **Protocol Success Indicators:**
- All BGP sessions show `"session_state": "established"`
- Routes advertised = 10,000 per peer (20,000 total)
- Routes received = 10,000 per peer (20,000 total)
- No session flaps during test execution

### **Traffic Success Indicators:**
- Frame loss = 0 (or < 1% acceptable threshold)
- TX frame count matches expected test duration × rate
- RX frame count equals TX frame count
- Traffic flows successfully through protocol-learned routes

This comprehensive metrics collection approach validates both the protocol engine functionality (BGP session establishment and route learning) and the traffic engine performance (packet forwarding through protocol-aware routes).
