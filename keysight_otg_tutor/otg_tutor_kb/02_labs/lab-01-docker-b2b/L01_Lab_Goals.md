---
title: "Lab 1 Goals and Objectives"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Learn the learning objectives, architecture, and expected outcomes for Lab 1 Docker back-to-back testing."
tags: ["goals", "objectives", "b2b-testing", "docker", "snappi"]
difficulty: "beginner"
---

# Lab 01: Docker Back-to-Back Testing - Main Guide

## 🎯 Overview
This lab uses **snappi** to control the free **Ixia-c Community Edition** (OTG Test Tool) deployed via Docker Engine commands to send raw traffic in a back-to-back topology. This lab consists of:
- **1x KENG Controller** container
- **2x Ixia-c Traffic Engine** containers

## 🎓 Learning Objectives
By the end of this lab, you will be able to:
- Deploy Ixia-c containers using Docker
- Create virtual network interfaces for testing
- Configure and execute traffic flows using snappi
- Validate traffic statistics and metrics
- Use otgen CLI tool for configuration management
- Perform proper cleanup of test environment

## 📋 Prerequisites
- Docker installed and running
- Python 3.8+ with pip and snappi package
- sudo privileges for network interface creation
- Basic understanding of networking concepts
- Familiarity with command line interface

## 🏗️ Lab Architecture
```
[KENG Controller:8443] ←→ [Traffic Engine 1:5551] ←→ veth0 ←→ veth1 ←→ [Traffic Engine 2:5552]
```

## 📊 Test Specifications
- **Traffic Pattern**: Bidirectional raw traffic (no protocol emulation)
- **Packet Count**: 2000 packets per direction
- **Rate**: 100 packets per second
- **Duration**: 20 seconds
- **Frame Size**: 128 bytes (initially)
- **Validation**: Port metrics for sent/received packets


**Questions to analyze:**
- Q#01: How much time did the entire test take?
- Q#02: Expected vs actual test duration and overhead?
- Q#03: How often does the script fetch statistics?



### Step 10: Modify Test Configuration

Edit the test script to change parameters:

```bash
vim lab-01_test.py
```

**Required changes:**
- **(a)** Rate: 200 fps instead of 100 fps
- **(b)** Duration: 5 seconds instead of 20 seconds
- **(c)** Frame size: 512 bytes instead of 128 bytes
- **(d)** Remove UDP header from one flow (ETH + IP only)
- **(e)** Change to unidirectional traffic (same direction)

**Verify changes:**
```bash
git diff
```

### Step 11: Execute Modified Test

Run the updated script:

```bash
python3 lab-01_test.py
```

**Compare results:**
```bash
# Save new interface counters
cat /proc/net/dev > counters2.log

# Compare before and after
diff counters1.log counters2.log

# Verify containers still running
docker ps -a
```


## ⚠️ Common Errors to Avoid

1. **Incorrect management network** or no reachability
2. **Wrong interface names/types/order** for test networks
3. **Same listening ports** for multiple containers in same namespace
4. **Incorrect container image versions** from registry
5. **Test interfaces not created** before docker run commands

---

## 📊 Expected Results

- **Container Status**: All 3 containers running successfully
- **Traffic Flow**: 2000 packets sent/received per direction
- **Duration**: ~20 seconds for initial test
- **Packet Loss**: 0% in ideal conditions
- **Interface Counters**: Match configured packet/byte counts

---

## 🎓 Key Learning Points

- **Version Specificity**: Always use specific image tags
- **Network Interfaces**: Virtual interfaces enable contained testing
- **Port Management**: Unique ports required for multiple containers
- **API Integration**: Both snappi (Python) and otgen (CLI) control same backend
- **Statistics Validation**: Multiple methods to verify traffic flow

---

## 📚 Additional Resources

- [Ixia-c Community Edition](https://ixia-c.dev/#community-edition)
- [OTG Model Rendering](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/open-traffic-generator/models/master/artifacts/openapi.yaml)
- [Ixia-c Releases](https://github.com/open-traffic-generator/ixia-c/releases)
- [OTGEN Documentation](https://github.com/open-traffic-generator/otgen)
