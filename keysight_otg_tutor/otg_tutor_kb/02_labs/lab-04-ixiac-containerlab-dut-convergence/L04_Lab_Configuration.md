---
title: "Lab 4 Configuration Setup"
lab_id: "lab-04-ixiac-containerlab-dut-convergence"
category: "lab"
objective: "Set up ContainerLab orchestration with Ixia-C-One all-in-one container and Nokia SRL DUT for BGP convergence testing."
tags: ["configuration", "containerlab", "setup", "ixia-c-one", "bgp", "convergence"]
difficulty: "advanced"
---

# Lab 04: Configuration Setup with ContainerLab and Ixia-C-One

## 🎯 Overview
Lab 04 introduces the **Ixia-C-One all-in-one container** for streamlined network testing with **BGP convergence analysis**. Unlike previous labs that used separate controller and traffic engine containers, Lab 04 demonstrates:
- **All-in-one traffic generation** with integrated controller, traffic engines, and protocol engines
- **iBGP convergence testing** through a Nokia SRL DUT acting as route reflector
- **Advanced failure scenarios** including link down and route withdrawal events
- **Convergence time measurement** for network resilience validation
- **Simplified deployment** with reduced container complexity

## 🚀 Step-by-Step Instructions

### Step 1: Install ContainerLab (if not already installed)

Install ContainerLab for advanced network topology orchestration:

```bash
# Install ContainerLab with specific version
bash -c "$(curl -sL https://get.containerlab.dev)" -- -v 0.59.0

# Verify installation
containerlab version
```

> 🔧 **Why ContainerLab for Lab 04?** ContainerLab provides excellent support for complex network topologies and is ideal for BGP convergence testing scenarios with real network devices.

### Step 2: Analyze the ContainerLab Topology

Examine the `lab-04.yml` ContainerLab deployment file to understand the simplified architecture:

```bash
# View the topology definition
cat lab-04.yml
```

**🧠 Understanding the lab-04.yml structure:**

```yaml
name: lab-04
topology:
  nodes:
    # Ixia-C-One: All-in-one traffic generator
    ixia-c-one:
      kind: linux
      image: ghcr.io/open-traffic-generator/ixia-c-one:1.8.0.99
      ports:
        - "8443:8443"   # Integrated controller port
      env:
        # Configure multiple interfaces for BGP testing
        OTG_LISTEN_PORT: 8443
        
    # Nokia SRL DUT: Route reflector and convergence testing
    srl:
      kind: nokia_srlinux
      image: ghcr.io/nokia/srlinux:latest
      startup-config: lab-04-srl.cfg
  
  links:
    # Direct connections for BGP convergence testing
    - endpoints: ["ixia-c-one:eth1","srl:e1-1"]  # Traffic interface
    - endpoints: ["ixia-c-one:eth2","srl:e1-2"]  # iBGP peer 1
    - endpoints: ["ixia-c-one:eth3","srl:e1-3"]  # iBGP peer 2
```

**Key architectural differences:**
- **Simplified Container Architecture**: Only 2 containers instead of 5-6 from previous labs
- **Ixia-C-One Integration**: All OTG components in a single container
- **Multiple Interface Connectivity**: Three interfaces for traffic and dual BGP peering
- **iBGP Configuration**: Internal BGP for convergence testing scenarios

### Step 3: Deploy the ContainerLab Topology

Deploy the complete topology with Ixia-C-One and Nokia SRL:

```bash
# Deploy the convergence testing topology
sudo containerlab deploy -t lab-04.yml
```

> ⚠️ **Automatic Image Download**: ContainerLab will automatically download any missing Docker images. The Ixia-C-One image may take a few minutes to download on first run.

**🧠 What happens during deployment:**
1. **Image Download**: Downloads Ixia-C-One and Nokia SRL images (first run only)
2. **Container Startup**: Starts both containers with proper networking
3. **DUT Configuration**: Nokia SRL loads the pre-configured BGP and interface setup
4. **Interface Linking**: Establishes three direct connections between containers
5. **Management Network**: All containers get management IPs for orchestration

### Step 4: Verify Deployment Success

Check that both containers are running and properly connected:

```bash
# Check ContainerLab deployment status
sudo containerlab inspect -t lab-04.yml

# Alternative: Check container status
docker ps
```

**Expected output:** You should see 2 containers running:
- `clab-lab-04-ixia-c-one` (Ixia-C-One All-in-One)
- `clab-lab-04-srl` (Nokia SRL DUT)

### Step 5: Verify Ixia-C-One Integration

Test the all-in-one container functionality:

```bash
# Check Ixia-C-One controller accessibility
curl -k https://clab-lab-04-ixia-c-one:8443/api/v1/version

# Check container logs for startup status
docker logs clab-lab-04-ixia-c-one
```

**🧠 Understanding Ixia-C-One Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│ Ixia-C-One Container                                    │
│                                                         │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│ │ Controller  │  │ Traffic     │  │ Protocol        │  │
│ │ :8443       │  │ Engines     │  │ Engines         │  │
│ │             │  │             │  │                 │  │
│ │ API Server  │  │ eth1, eth2, │  │ BGP, OSPF,      │  │
│ │ Config Mgmt │  │ eth3        │  │ ISIS, etc.      │  │
│ └─────────────┘  └─────────────┘  └─────────────────┘  │
│                                                         │
│ Interfaces: eth1 (traffic), eth2 (BGP), eth3 (BGP)    │
└─────────────────────────────────────────────────────────┘
```

**🔧 Advantages of Ixia-C-One:**
- **Simplified Deployment**: Single container instead of multiple components
- **Integrated Management**: No need for separate controller container
- **Reduced Complexity**: Fewer networking configurations required
- **Resource Efficiency**: Lower overhead compared to separate containers

### Step 6: Verify Nokia SRL DUT Configuration

Connect to the Nokia SRL DUT to verify BGP and interface configuration:

```bash
# Connect to Nokia SRL DUT
ssh admin@clab-lab-04-srl

# Default password: NokiaSrl1!
# If not in CLI mode, type: sr_cli
```

**Verify key configuration elements:**
```bash
# Check interface configuration
show interface ethernet-1/1
show interface ethernet-1/2
show interface ethernet-1/3

# Check BGP configuration
show network-instance default protocols bgp

# Check route reflector configuration
show network-instance default protocols bgp route-reflector
```

**🧠 Understanding the Nokia SRL Configuration:**
The `lab-04-srl.cfg` file pre-configures the DUT with:
- **Interface e1-1**: 192.168.11.1/24 (traffic interface)
- **Interface e1-2**: 192.168.22.1/24 (iBGP peer 1)
- **Interface e1-3**: 192.168.33.1/24 (iBGP peer 2)
- **BGP Route Reflector**: Enables iBGP between eth2 and eth3 peers
- **BGP Attributes**: Configured for Local Preference and MED testing

## 🎯 Configuration Summary

After successful deployment, you will have:

### **Container Architecture:**
- **2 containers** running with ContainerLab orchestration:
  - **Ixia-C-One**: `clab-lab-04-ixia-c-one:8443` (all-in-one traffic generator)
  - **Nokia SRL DUT**: `clab-lab-04-srl` with pre-configured BGP and interfaces

### **Network Topology:**
- **Three interface connections**: eth1 (traffic), eth2 (BGP peer 1), eth3 (BGP peer 2)
- **ContainerLab management network** for orchestration
- **iBGP peering** through Nokia SRL route reflector
- **Traffic and control plane separation** for realistic testing

### **BGP Configuration:**
- **iBGP sessions** between Ixia-C-One eth2/eth3 and Nokia SRL
- **Route reflection** enabling communication between iBGP peers
- **BGP attributes** configured for path selection testing (Local Preference, MED)
- **Route advertisement** ready for convergence testing scenarios

### **Convergence Testing Setup:**
- **Dual-path architecture** for failover testing
- **Link failure simulation** capabilities
- **Route withdrawal** testing through BGP updates
- **Traffic monitoring** during convergence events

## ⚠️ Common Deployment Issues

### ContainerLab-Specific Issues:
- **Permission errors**: Ensure `sudo` is used for ContainerLab commands
- **Ixia-C-One image**: First download may take time, be patient
- **Port conflicts**: Check that 8443 is not in use by other applications
- **Network conflicts**: Verify ContainerLab network doesn't conflict with existing networks

### Ixia-C-One Issues:
- **Controller not responding**: Check if all-in-one container started properly
- **Interface binding**: Verify eth1, eth2, eth3 interfaces exist in container
- **API connectivity**: Ensure port 8443 is accessible for API communication
- **Resource constraints**: Ixia-C-One requires adequate CPU and memory

### BGP Configuration Issues:
- **SRL not responding**: Check if startup-config loaded properly
- **BGP sessions not establishing**: Verify IP addressing and routing
- **Route reflection not working**: Confirm route reflector configuration
- **Interface down**: Verify physical interface connections in topology

## 🔧 Advanced Configuration Notes

### **ContainerLab Container Naming:**
ContainerLab prefixes all container names with `clab-<topology-name>-`:
- Use `clab-lab-04-ixia-c-one:8443` in test scripts for controller
- Use interface names directly: eth1, eth2, eth3 for port locations

### **Ixia-C-One API Access:**
```bash
# Test API connectivity
curl -k https://clab-lab-04-ixia-c-one:8443/api/v1/version

# Check controller status
curl -k https://clab-lab-04-ixia-c-one:8443/api/v1/control/state
```

### **Nokia SRL BGP Monitoring:**
```bash
# Monitor BGP sessions
ssh admin@clab-lab-04-srl
show network-instance default protocols bgp neighbor

# Watch route changes during convergence
watch show network-instance default protocols bgp routes ipv4 summary
```

### **Convergence Testing Preparation:**
- **Baseline establishment**: Verify stable BGP sessions before testing
- **Route advertisement**: Confirm both peers advertise routes successfully
- **Traffic validation**: Ensure bidirectional flows work correctly
- **Monitoring setup**: Prepare real-time monitoring during convergence events

---

**Next Step**: Proceed to L04_Lab_Test_Execution.md to configure BGP convergence testing and start validation with the Ixia-C-One all-in-one container.