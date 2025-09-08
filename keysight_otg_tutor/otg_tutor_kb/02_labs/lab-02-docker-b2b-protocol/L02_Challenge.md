---
title: "Lab 2 Challenge - Advanced Protocol Scenarios"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Practice advanced protocol configurations, route manipulation, and failure scenario testing."
tags: ["challenge", "modification", "protocol", "bgp", "advanced"]
difficulty: "intermediate"
---

# Lab 02: Advanced Protocol Challenge

## 🚀 Step-by-Step Instructions for Advanced Protocol Testing

### Step 1: Modify BGP Configuration

Edit the test script to implement advanced BGP features:

```bash
vim L02_lab_02_test.py
```

**Required changes:**
- **(a)** AS Path Prepending: Add AS path prepending to influence route selection
- **(b)** Route Filtering: Implement prefix-list filtering on advertised routes
- **(c)** Multi-Exit Discriminator (MED): Configure MED values for route preference
- **(d)** BGP Communities: Add community attributes to advertised routes
- **(e)** Route Reflection: Configure one peer as route reflector

### Step 2: Protocol Failure Scenarios

Test protocol resilience:

```bash
# Simulate BGP session failure
# Stop one protocol engine during traffic
docker stop protocol-engine-1

# Monitor traffic behavior during protocol failure
python3 L02_lab_02_test.py --failure-test

# Restart protocol engine and observe reconvergence
docker start protocol-engine-1
```

### Step 3: Advanced Route Advertisement

Implement complex routing scenarios:

- **Route Aggregation**: Advertise summarized routes
- **Route Redistribution**: Simulate route redistribution between protocols
- **Policy-Based Routing**: Implement traffic engineering with BGP policies

**Verify changes:**
```bash
git diff L02_lab_02_test.py
```

**Compare results:**
```bash
# Monitor protocol convergence with advanced features
curl -k https://localhost:8443/api/v1/results/metrics | jq '.protocol_metrics.bgp.advanced_features'

# Verify containers still running after modifications
docker ps -a
```

**Assessment Questions:**
- How did AS path prepending affect route selection?
- What was the impact of route filtering on convergence time?
- How did the network behave during protocol engine failure?
- What's the difference between BGP MED and Local Preference?
