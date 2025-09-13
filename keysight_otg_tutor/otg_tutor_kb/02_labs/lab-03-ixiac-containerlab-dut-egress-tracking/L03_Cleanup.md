---
title: "Lab 3 Environment Cleanup"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Safely terminate DUT sessions and remove all ContainerLab containers and network topology created during Lab 3."
tags: ["cleanup", "containerlab", "dut", "nokia-srl", "network-topology", "egress-tracking"]
difficulty: "advanced"
---

# L03: Lab Cleanup Guide with ContainerLab and DUT

## 🎯 Overview
This guide walks you through safely removing all resources created during Lab 03, including proper DUT session termination and ContainerLab topology cleanup. DUT-aware cleanup is essential to avoid configuration state issues and ensure clean environment reset for future tests.

## 🧹 Cleanup Checklist
- [ ] Gracefully terminate active test sessions
- [ ] Save DUT configuration (if needed for analysis)
- [ ] Stop running containers (6 total)
- [ ] Destroy ContainerLab topology
- [ ] Remove container images (optional)
- [ ] Clean up ContainerLab networks
- [ ] Verify complete cleanup

## 📋 Step-by-Step Cleanup

### Step 1: Gracefully Terminate Test Sessions

Before destroying the topology, properly terminate any running test sessions:

```bash
# Stop any running test scripts
pkill -f lab-03-1_test.py
pkill -f lab-03-2_test.py

# Wait for graceful termination
sleep 10
```

**Why this matters:**
- Allows OTG to properly close API connections
- Prevents hanging test sessions
- Ensures clean metric collection termination

### Step 2: Save DUT Configuration (Optional)

If you made configuration changes to Nokia SRL during testing, save them for analysis:

```bash
# Connect to Nokia SRL DUT
ssh admin@clab-lab-03-srl

# Save current configuration
show configuration | save /tmp/lab-03-final-config.txt

# Exit DUT
exit
```

**Configuration elements to review:**
- QoS policy changes (DSCP remarking rules)
- Interface statistics
- Any custom configurations applied during testing

### Step 3: Destroy ContainerLab Topology

Use ContainerLab to safely destroy the entire topology:

```bash
# Destroy the complete lab topology
sudo containerlab destroy -t lab-03.yml --cleanup
```

**🧠 What this command does:**
- **Graceful Container Shutdown**: Stops all 6 containers in proper order
- **DUT State Cleanup**: Safely terminates Nokia SRL with proper shutdown sequence
- **Network Cleanup**: Removes all ContainerLab-created networks and links
- **Volume Cleanup**: Removes any temporary volumes created
- **Interface Cleanup**: Removes virtual interfaces and connections
- **Complete Topology Removal**: Destroys the entire lab-03 topology

**Expected Output:**
```
INFO[0000] Parsing & checking topology file: lab-03.yml 
INFO[0001] Destroying lab: lab-03                       
INFO[0001] Removed container: clab-lab-03-pe2          
INFO[0002] Removed container: clab-lab-03-pe1          
INFO[0003] Removed container: clab-lab-03-te2          
INFO[0004] Removed container: clab-lab-03-te1          
INFO[0005] Removed container: clab-lab-03-controller   
INFO[0006] Removed container: clab-lab-03-srl          
INFO[0007] Removing containerlab host entries from /etc/hosts file
INFO[0008] Removing ssh config for containerlab nodes  
```

### Step 4: Verify Complete Cleanup

Verify that all Lab 03 resources have been removed:

```bash
# Check that no lab-03 containers are running
docker ps | grep clab-lab-03
# Should return no results

# Check that no stopped lab-03 containers remain
docker ps -a | grep clab-lab-03
# Should return no results

# Check ContainerLab topologies
sudo containerlab inspect --all | grep lab-03
# Should return no results

# Check Docker networks
docker network ls | grep clab
# Should not show lab-03 networks
```

### Step 5: Clean Up Container Images (Optional)

If you want to free up disk space, remove the container images:

```bash
# List OTG and Nokia SRL images
docker images | grep -E "(keng-controller|ixia-c|srlinux)"

# Remove specific images (optional - only if you want to free disk space)
docker rmi ghcr.io/open-traffic-generator/keng-controller:1.14.0-1
docker rmi ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99
docker rmi ghcr.io/open-traffic-generator/ixia-c-protocol-engine:1.00.0.405
docker rmi ghcr.io/nokia/srlinux:latest

# Alternative: Clean up all unused images
docker image prune -a
```

> ⚠️ **Note**: Removing images will require re-downloading them for future lab runs. Only remove if disk space is a concern.

### Step 6: Advanced Cleanup (If Issues Occur)

If standard cleanup doesn't work completely, use these advanced cleanup commands:

```bash
# Force remove any remaining lab-03 containers
docker rm -f $(docker ps -a -q --filter "name=clab-lab-03")

# Remove any orphaned ContainerLab networks
docker network rm $(docker network ls -q --filter "name=clab-lab-03")

# Clean up any remaining network namespaces
sudo ip netns list | grep clab-lab-03 | xargs -r sudo ip netns del

# Remove ContainerLab host entries (if not cleaned automatically)
sudo sed -i '/clab-lab-03/d' /etc/hosts
```

## 🔍 Troubleshooting Cleanup Issues

### **Container Won't Stop:**
```bash
# Force kill specific container
docker kill clab-lab-03-srl

# Force remove if kill doesn't work
docker rm -f clab-lab-03-srl
```

### **Network Removal Issues:**
```bash
# Check what's using the network
docker network inspect clab-lab-03

# Disconnect containers from network
docker network disconnect clab-lab-03 <container_name>

# Force remove network
docker network rm clab-lab-03
```

### **Permission Issues:**
```bash
# Ensure proper sudo privileges for ContainerLab
sudo -v

# Check ContainerLab process ownership
ps aux | grep containerlab
```

### **Nokia SRL Won't Terminate:**
```bash
# Check SRL container logs
docker logs clab-lab-03-srl

# Force terminate if needed
docker kill clab-lab-03-srl
```

## ✅ Cleanup Verification Checklist

Run these commands to ensure complete cleanup:

```bash
# 1. No lab-03 containers
echo "Checking containers..."
docker ps -a | grep clab-lab-03 && echo "❌ Containers still exist" || echo "✅ No containers found"

# 2. No lab-03 networks  
echo "Checking networks..."
docker network ls | grep clab-lab-03 && echo "❌ Networks still exist" || echo "✅ No networks found"

# 3. No ContainerLab topologies
echo "Checking topologies..."
sudo containerlab inspect --all 2>/dev/null | grep lab-03 && echo "❌ Topology still exists" || echo "✅ No topology found"

# 4. No host file entries
echo "Checking host entries..."
grep clab-lab-03 /etc/hosts && echo "❌ Host entries still exist" || echo "✅ No host entries found"

# 5. No SSH config entries
echo "Checking SSH config..."
grep clab-lab-03 ~/.ssh/config 2>/dev/null && echo "❌ SSH entries still exist" || echo "✅ No SSH entries found"
```

## 📊 Cleanup Success Indicators

**✅ Successful cleanup should show:**
- No containers with `clab-lab-03` prefix
- No networks with `clab-lab-03` prefix  
- No active ContainerLab topologies
- No host file entries for lab containers
- No SSH configuration entries
- Clean `docker ps` and `docker network ls` output

## 🔄 Post-Cleanup Actions

### **Environment Reset:**
```bash
# Verify Docker is clean
docker system df

# Optional: Clean up unused resources
docker system prune

# Verify ContainerLab is ready for next lab
sudo containerlab version
```

### **Preparation for Next Lab:**
- Lab environment is clean and ready
- No resource conflicts for future deployments  
- All network interfaces available
- Container runtime optimized

## 🎯 Cleanup Best Practices

### **1. Always Use Proper Sequence:**
1. Stop test scripts first
2. Save important DUT configurations
3. Use ContainerLab destroy command
4. Verify cleanup completion
5. Clean up images only if needed

### **2. Documentation:**
- Record any custom configurations made
- Note any issues encountered during cleanup
- Document any manual cleanup steps required

### **3. Verification:**
- Always verify complete cleanup
- Check for orphaned resources
- Ensure environment is ready for next lab

---

**🎯 Cleanup Complete!**
Your Lab 03 environment has been safely cleaned up. The system is now ready for:
- Future Lab 03 runs
- Other ContainerLab topologies  
- Different OTG testing scenarios
- Clean development environment

**Next Step**: Review L03_Lab_Metrics.md results or proceed to advanced challenges in L03_Challenge.md.