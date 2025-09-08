---
title: "Lab 2 Environment Cleanup"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Safely terminate protocol sessions and remove all Docker containers and virtual network interfaces created during Lab 2."
tags: ["cleanup", "docker", "containers", "protocol-sessions", "network-interfaces"]
difficulty: "intermediate"
---

# L02: Lab Cleanup Guide with Protocol Sessions

## 🎯 Overview
This guide walks you through safely removing all resources created during Lab 02, including proper protocol session termination. Protocol-aware cleanup is essential to avoid session state issues and ensure clean environment reset.

## 🧹 Cleanup Checklist
- [ ] Gracefully terminate protocol sessions
- [ ] Stop running containers (5 total)
- [ ] Remove stopped containers
- [ ] Remove virtual network interfaces
- [ ] Clean up Docker networks
- [ ] Verify complete cleanup

## 📋 Step-by-Step Cleanup

### Step 1: Gracefully Terminate Protocol Sessions

Before stopping containers, properly terminate protocol sessions:

```bash
# Query active BGP sessions
curl -k https://localhost:8443/api/v1/results/metrics | jq '.protocol_metrics.bgp'

# Gracefully stop protocol sessions (if test script is still running)
# This allows BGP sessions to send proper NOTIFICATION messages
pkill -f L02_lab_02_test.py
```

**Wait for graceful shutdown:**
```bash
# Wait 30 seconds for protocol sessions to terminate cleanly
sleep 30
```

### Step 2: Stop and Remove Docker Compose Services

Use Docker Compose to stop and remove all Lab 02 containers:

```bash
#2-20
docker-compose down
```

**What this command does:**
- Stops all running containers defined in compose.yml
- Removes the stopped containers
- Removes the custom bridge network (lab-02_default)
- Preserves volumes (if any were defined)

**Expected Output:**
```
Stopping lab-02_protocol_engine_2_1 ... done
Stopping lab-02_protocol_engine_1_1 ... done
Stopping lab-02_traffic_engine_2_1  ... done
Stopping lab-02_traffic_engine_1_1  ... done
Stopping lab-02_keng-controller_1   ... done
Removing lab-02_protocol_engine_2_1 ... done
Removing lab-02_protocol_engine_1_1 ... done
Removing lab-02_traffic_engine_2_1  ... done
Removing lab-02_traffic_engine_1_1  ... done
Removing lab-02_keng-controller_1   ... done
Removing network lab-02_default
```

**Verification:**
```bash
docker ps -a | grep lab-02
```
Should return no results.

### Step 3: Clean Up IP Network Namespaces

Remove the IP network namespaces created by the connection script:

```bash
#2-21
sudo ip netns del lab-02_traffic_engine_1_1 && sudo ip netns del lab-02_traffic_engine_2_1
```

**What this command does:**
- Deletes the network namespace for Traffic Engine 1
- Deletes the network namespace for Traffic Engine 2
- Removes the veth pair connections automatically
- Cleans up any remaining namespace-specific network configuration

**Expected Output:**
```
(No output on success)
```

**Verification:**
```bash
# Check that namespaces are removed
sudo ip netns list | grep lab-02

# Verify veth interfaces are gone
ip link show | grep veth
```
Both commands should return no results.

### Step 4: Verify Complete Cleanup

Run final verification:

```bash
# Check for any remaining Lab 02 containers
docker ps -a | grep lab-02

# Check for virtual interfaces and namespaces
ip link show | grep veth
sudo ip netns list | grep lab-02

# Check Docker networks
docker network ls | grep lab-02

# Verify no protocol processes running
ps aux | grep -E "(bgp|protocol|snappi)"
```

All commands should return empty results or "not found" errors.

## 🔍 Troubleshooting Cleanup Issues

### Issue: Protocol Sessions Won't Terminate

```bash
# Force terminate any remaining protocol processes
pkill -9 -f "protocol"
pkill -9 -f "bgp"

# Then proceed with Docker Compose cleanup
docker-compose down
```

### Issue: Containers Won't Stop

```bash
# Force stop if graceful Docker Compose down fails
docker-compose kill

# Force remove all containers and networks
docker-compose down --remove-orphans --volumes

# Alternative: Force remove specific Lab 02 containers
docker rm -f $(docker ps -aq --filter "name=lab-02")
```

### Issue: Protocol State Persistence

```bash
# Clear any persistent protocol state files
sudo rm -rf /tmp/bgp_* /tmp/protocol_* 2>/dev/null || true

# Reset network namespaces if needed
sudo ip netns list | grep -E "(otg|test)" | xargs -I {} sudo ip netns delete {}
```

## ✅ Cleanup Verification Checklist

After completing all cleanup steps, verify:

- [ ] `docker ps -a | grep lab-02` shows no Lab 02 containers
- [ ] `sudo ip netns list | grep lab-02` shows no Lab 02 namespaces
- [ ] `ip link show | grep veth` shows no veth interfaces
- [ ] `docker network ls | grep lab-02` shows no lab-02_default network
- [ ] No protocol processes running: `ps aux | grep protocol`
- [ ] System resources are freed up

## 🎓 Why Protocol-Aware Cleanup Matters

### Protocol Session Management
- **Graceful termination**: Allows BGP NOTIFICATION messages
- **State cleanup**: Prevents stale protocol entries
- **Resource management**: Properly releases protocol engine resources

### Best Practices for Protocol Labs
- Always terminate protocol sessions before container cleanup
- Allow time for graceful protocol shutdown
- Monitor protocol session states during cleanup
- Verify complete protocol state cleanup

## 🔄 Preparing for Next Labs

After cleanup, your system is ready for:
- **Lab 03**: Advanced multi-protocol scenarios
- **Lab 04**: Scale testing with thousands of routes
- **Lab 05**: Integration with real network devices

## 📞 Need Help?

If you encounter issues during cleanup:

1. **Check the troubleshooting section** above
2. **Review the FAQ** in L02_FAQ.md
3. **Consult protocol troubleshooting** in L02_Troubleshooting.md
4. **Ask for help** in the community forums

---

**🎯 Key Takeaway**: Protocol-aware cleanup ensures clean session termination and prevents state persistence issues. Always terminate protocol sessions gracefully before container cleanup!
