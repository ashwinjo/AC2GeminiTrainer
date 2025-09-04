---
title: "Lab 1 Environment Cleanup"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Safely stop and remove all Docker containers and virtual network interfaces created during Lab 1."
tags: ["cleanup", "docker", "containers", "network-interfaces"]
difficulty: "beginner"
---

# L01: Lab Cleanup Guide

## 🎯 Overview
This guide walks you through safely removing all resources created during Lab 01 (Docker Back-to-Back Testing). Proper cleanup is essential to free up system resources and prevent conflicts with future labs.

## 🧹 Cleanup Checklist
- [ ] Stop running containers
- [ ] Remove stopped containers
- [ ] Remove virtual network interfaces
- [ ] Clean up Docker networks
- [ ] Verify complete cleanup

## 📋 Step-by-Step Cleanup

### Step 1: Stop Running Containers

First, gracefully stop all containers that were started during the lab.

**Command:**
```bash
docker stop controller traffic-engine-1 traffic-engine-2
```

**Expected Output:**
```
controller
traffic-engine-1
traffic-engine-2
```

**Verification:**
```bash
docker ps
```
The output should show no running containers (empty list).

### Step 2: Remove Stopped Containers

Now permanently remove the stopped containers from your system.

**Command:**
```bash
docker rm controller traffic-engine-1 traffic-engine-2
```

**Expected Output:**
```
controller
traffic-engine-1
traffic-engine-2
```

**Verification:**
```bash
docker ps -a
```
The three lab containers should no longer appear in the list.

### Step 3: Remove Virtual Network Interfaces

Remove the virtual network "patch cable" created for the lab.

**Command:**
```bash
sudo ip link delete veth0
```

> 💡 **Note**: You only need to delete one side of the veth pair (veth0). The other side (veth1) will be automatically removed with it.

**Verification:**
```bash
ip link show veth0
```

**Expected Output:**
```
Device "veth0" does not exist.
```
This error message confirms successful deletion.

### Step 4: Clean Up Docker Networks (Optional)

If you created custom Docker networks during the lab, remove them as well.

**Command:**
```bash
# List Docker networks
docker network ls

# Remove lab-specific network (if created)
docker network rm otg-test-net
```

### Step 5: Verify Complete Cleanup

Run a final verification to ensure all resources are cleaned up.

**Verification Commands:**
```bash
# Check for any remaining containers
docker ps -a | grep -E "(controller|traffic-engine)"

# Check for virtual interfaces
ip link show | grep veth

# Check Docker networks
docker network ls | grep otg
```

All commands should return empty results or "not found" errors.

## 🔍 Troubleshooting Cleanup Issues

### Issue: Container Won't Stop
```bash
# Force stop if graceful stop fails
docker kill controller traffic-engine-1 traffic-engine-2

# Then remove
docker rm controller traffic-engine-1 traffic-engine-2
```

### Issue: Permission Denied for Virtual Interface
```bash
# Ensure you're using sudo
sudo ip link delete veth0

# If still failing, check if interface exists
ip link show | grep veth
```

### Issue: Container Removal Fails
```bash
# Force removal
docker rm -f controller traffic-engine-1 traffic-engine-2
```

### Issue: Network Removal Fails
```bash
# Check what's using the network
docker network inspect otg-test-net

# Force remove network
docker network rm -f otg-test-net
```

## ✅ Cleanup Verification Checklist

After completing all cleanup steps, verify:

- [ ] `docker ps` shows no lab-related containers
- [ ] `docker ps -a` shows no lab-related containers
- [ ] `ip link show` shows no veth interfaces
- [ ] `docker network ls` shows no lab-specific networks
- [ ] System resources are freed up

## 🎓 Why Cleanup Matters

### Resource Management
- **Memory**: Containers consume RAM even when stopped
- **Disk Space**: Container layers and logs accumulate over time
- **Network**: Virtual interfaces can conflict with future labs

### Best Practices
- Always clean up after each lab session
- Use descriptive container names for easy identification
- Document custom networks and resources created
- Regular system cleanup prevents resource exhaustion

## 🔄 Preparing for Next Labs

After cleanup, your system is ready for:
- **Lab 02**: Advanced OTG configurations
- **Lab 03**: Multi-container orchestration
- **Lab 04**: Performance testing scenarios

## 📞 Need Help?

If you encounter issues during cleanup:

1. **Check the troubleshooting section** above
2. **Review the FAQ** in L01_FAQ.md
3. **Consult general troubleshooting** in the troubleshooting_general section
4. **Ask for help** in the community forums

---

**🎯 Key Takeaway**: Proper cleanup is just as important as the lab setup. It ensures your system stays healthy and ready for future learning activities!