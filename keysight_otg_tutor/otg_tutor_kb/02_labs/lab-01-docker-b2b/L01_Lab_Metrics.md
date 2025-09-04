---
title: "Lab 1 Metrics Collection"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Learn how to collect and analyze traffic metrics from OTG test execution using various monitoring techniques."
tags: ["metrics", "monitoring", "statistics", "analysis", "verification"]
difficulty: "beginner"
---

## 🚀 Step-by-Step Instructions to get metrics from OTG Test Execution

### Step 1: Verify Interface Counters

Check network interface statistics:

```bash
# Save interface counters before test
cat /proc/net/dev > counters1.log
```

**Analysis questions:**
- Q#04: Which interfaces were used for traffic?
- Q#05: Do packet counts match script configuration?
- Q#06: Do byte counts correspond to frame size?

### Step 2: Get Controller Statistics via REST API

Query statistics using curl commands:

```bash
# Get flow metrics
curl -k -d '{"choice":"flow"}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get port metrics
curl -k -d '{"choice":"port"}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get specific port metrics
curl -k -d '{"choice":"port","port":{"port_names":["Port-2"]}}' -X POST https://127.0.0.1:8443/monitor/metrics
```