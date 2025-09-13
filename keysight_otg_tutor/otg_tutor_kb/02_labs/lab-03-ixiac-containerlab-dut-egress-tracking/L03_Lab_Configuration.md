---
title: "Lab 3 Configuration Setup"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Set up ContainerLab orchestration with Nokia SRL DUT, egress tracking configuration, and advanced network topology for Lab 3."
tags: ["configuration", "containerlab", "setup", "dut", "nokia-srl", "egress-tracking", "vlan", "qos"]
difficulty: "advanced"
---

# Lab 03: Configuration Setup with ContainerLab Orchestration

## 🎯 Overview
Lab 03 introduces a **real network device (DUT)** into the testing environment using **ContainerLab orchestration**. Unlike previous labs that used simple back-to-back connections, Lab 03 demonstrates:
- **Device Under Test (DUT) integration** with Nokia SRL network device
- **ContainerLab networking** for complex topologies with real network equipment
- **Egress tracking configuration** to monitor packet transformations
- **VLAN sub-interface setup** with QoS policies for comprehensive testing
- **Automated DUT configuration** with pre-loaded network policies

## 🚀 Step-by-Step Instructions

### Step 1: Install ContainerLab (if not already installed)

Install ContainerLab for advanced network topology orchestration:

```bash
# Install ContainerLab with specific version
bash -c "$(curl -sL https://get.containerlab.dev)" -- -v 0.59.0

# Verify installation
containerlab version
```

> 🔧 **Why ContainerLab?** Unlike Docker Compose which is designed for application containers, ContainerLab is specifically built for network topology orchestration with support for real network devices, complex interconnections, and network-specific configurations.

**🧠 ContainerLab vs Docker Compose:**
- **Docker Compose**: Application-focused, simple networking, limited topology control
- **ContainerLab**: Network-focused, complex topologies, real device integration, advanced networking features

### Step 2: Analyze the ContainerLab Topology

Examine the `lab-03.yml` ContainerLab deployment file:

```bash
# View the topology definition
cat lab-03.yml
```

**🧠 Understanding the lab-03.yml structure:**

```yaml
name: lab-03
topology:
  nodes:
    # KENG Controller - orchestrates all testing
    controller:
      kind: linux
      image: ghcr.io/open-traffic-generator/keng-controller:1.14.0-1
      cmd: --accept-eula --http-port 8443
      ports:
        - 8443:8443
    
    # Traffic Engine 1 - generates traffic
    te1:
      kind: linux
      image: ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99
      env:
        OPT_LISTEN_PORT: 5551
        ARG_IFACE_LIST: virtual@af_packet,eth1
        OPT_NO_HUGEPAGES: Yes
        OPT_NO_PINNING: Yes
        WAIT_FOR_IFACE: Yes
    
    # Nokia SRL DUT - the device we're testing
    srl:
      kind: nokia_srlinux
      image: ghcr.io/nokia/srlinux:latest
      startup-config: lab-03-srl.cfg
  
  links:
    # Direct connections between components
    - endpoints: ["te1:eth1","srl:e1-1"]
    - endpoints: ["te2:eth2","srl:e1-2"]
```

**Key differences from Docker Compose:**
- **Real Device Integration**: Nokia SRL is a real network device, not just another container
- **Startup Configuration**: DUT automatically loads `lab-03-srl.cfg` configuration
- **Advanced Networking**: ContainerLab handles complex network device interconnections
- **Interface Mapping**: Direct interface-to-interface connections (eth1 ↔ e1-1)

### Step 3: Deploy the ContainerLab Topology

Deploy all containers and the Nokia SRL DUT:

```bash
# Deploy the complete topology with DUT
sudo containerlab deploy -t lab-03.yml
```

> ⚠️ **Sudo Required**: ContainerLab needs elevated privileges to create network namespaces and configure real network devices.

**🧠 What happens during deployment:**
1. **Image Download**: Downloads Nokia SRL and OTG images (first run only)
2. **Network Creation**: Creates ContainerLab management network
3. **Container Startup**: Starts all 6 containers in dependency order
4. **DUT Configuration**: Nokia SRL loads the pre-configured startup config
5. **Interface Linking**: Establishes direct connections between containers
6. **Management Network**: All containers get management IPs for orchestration

### Step 4: Verify Deployment Success

Check that all containers are running and properly connected:

```bash
# Check ContainerLab deployment status
sudo containerlab inspect -t lab-03.yml

# Alternative: Check container status
docker ps
```

**Expected output:** You should see 6 containers running:
- `clab-lab-03-controller` (KENG Controller)
- `clab-lab-03-te1` (Traffic Engine 1)
- `clab-lab-03-te2` (Traffic Engine 2)  
- `clab-lab-03-pe1` (Protocol Engine 1)
- `clab-lab-03-pe2` (Protocol Engine 2)
- `clab-lab-03-srl` (Nokia SRL DUT)

### Step 5: Verify Nokia SRL DUT Configuration

Connect to the Nokia SRL DUT to verify the configuration loaded correctly:

```bash
# Connect to Nokia SRL DUT
ssh admin@clab-lab-03-srl

# Default password: NokiaSrl1!
# If not in CLI mode, type: sr_cli
```

**Verify key configuration elements:**
```bash
# Check interface configuration
show interface ethernet-1/1
show interface ethernet-1/2

# Check VLAN sub-interfaces
show interface ethernet-1/2.1
show interface ethernet-1/2.2
show interface ethernet-1/2.3

# Check QoS policies
show qos
```

**🧠 Understanding the Nokia SRL Configuration:**
The `lab-03-srl.cfg` file pre-configures the DUT with:
- **Interface e1-1**: 192.168.11.1/24 (untagged, connects to TE1)
- **Sub-interfaces on e1-2**:
  - e1-2.1: VLAN 101, 192.168.101.1/24
  - e1-2.2: VLAN 102, 192.168.102.1/24  
  - e1-2.3: VLAN 103, 192.168.103.1/24
- **QoS Policies**: DSCP 10 → FC1 → DSCP 20 remarking

### Step 6: Understand the Network Architecture

Unlike previous labs, Lab 03 uses **ContainerLab networking** instead of manual veth pairs:

```bash
# Inspect the ContainerLab network
docker network ls | grep clab

# Check container network assignments
docker inspect clab-lab-03-te1 | grep NetworkMode
```

**🧠 ContainerLab Network Architecture:**

#### **Management Network:**
All containers connect to a ContainerLab-managed network for orchestration:
```
clab-lab-03 network: 172.20.20.0/24
├── controller: 172.20.20.2
├── te1: 172.20.20.3
├── te2: 172.20.20.4
├── pe1: shares te1's network
├── pe2: shares te2's network
└── srl: 172.20.20.7
```

#### **Data Plane Connections:**
Direct interface connections for traffic testing:
```
te1:eth1 ←→ srl:e1-1 (192.168.11.0/24)
te2:eth2 ←→ srl:e1-2 (VLAN sub-interfaces)
```

#### **Shared Network Spaces (PE + TE):**
Protocol Engines share network namespaces with Traffic Engines:
```yaml
pe1:
  network-mode: container:te1  # PE1 shares TE1's network
pe2:
  network-mode: container:te2  # PE2 shares TE2's network
```

### Step 7: Verify Interface Connectivity

Check that the traffic engines can see their interfaces:

```bash
# Check TE1 interfaces
docker exec -it clab-lab-03-te1 ip addr

# Check TE2 interfaces  
docker exec -it clab-lab-03-te2 ip addr

# Look for eth1 and eth2 interfaces respectively
```

**🔍 What to look for:**
- **eth1 on TE1**: Connected to Nokia SRL e1-1
- **eth2 on TE2**: Connected to Nokia SRL e1-2
- **Management interfaces**: For ContainerLab orchestration
- **No veth pairs needed**: ContainerLab handles direct connections

### Step 8: Prepare for Egress Tracking

Understanding the egress tracking setup for this lab:

**🧠 Egress Tracking Configuration:**
```python
# What we'll track in the test script:
f.egress_packet.ethernet()              # Expect Ethernet header
eg_vlan = f.egress_packet.add().vlan    # Expect VLAN header (added by DUT)
eg_ip = f.egress_packet.add().ipv4      # Expect IPv4 header

# Track VLAN ID values
eg_vlan.id.metric_tags.add(name="vlanIdRx")

# Track DSCP values (optional)
eg_ip.priority.dscp.metric_tags.add(name="dscpValuesRx")
```

**Expected transformations by Nokia SRL:**
1. **Ingress (TE1 → SRL e1-1)**: Untagged packets with various DSCP values
2. **DUT Processing**: 
   - Add VLAN tags (101, 102, or 103)
   - Remark DSCP 10 → DSCP 20
   - Route to appropriate sub-interface
3. **Egress (SRL e1-2 → TE2)**: Tagged packets with modified DSCP values

## 🎯 Configuration Summary

After successful deployment, you will have:

### **Container Architecture:**
- **6 containers** running with ContainerLab orchestration:
  - **Controller**: `clab-lab-03-controller:8443`
  - **TE1 + PE1**: `clab-lab-03-te1:5551` + `clab-lab-03-te1:50071`
  - **TE2 + PE2**: `clab-lab-03-te2:5552` + `clab-lab-03-te2:50071`
  - **Nokia SRL DUT**: `clab-lab-03-srl` with pre-configured policies

### **Network Topology:**
- **Direct interface connections** (eth1 ↔ e1-1, eth2 ↔ e1-2)
- **ContainerLab management network** for orchestration
- **Shared PE+TE network namespaces** for efficient communication
- **VLAN sub-interfaces** on Nokia SRL for traffic distribution

### **DUT Configuration:**
- **VLAN sub-interfaces**: 101, 102, 103 on e1-2
- **QoS policies**: DSCP remarking (10 → 20)
- **IP addressing**: Proper subnet configuration for each VLAN
- **Ready for egress tracking**: Configured to perform packet transformations

## ⚠️ Common Deployment Issues

### ContainerLab-Specific Issues:
- **Permission errors**: Ensure `sudo` is used for ContainerLab commands
- **Nokia SRL image**: First download may take time, be patient
- **Port conflicts**: Check that 8443 is not in use by other applications
- **Network conflicts**: Verify ContainerLab network doesn't conflict with existing networks

### DUT Configuration Issues:
- **SRL not responding**: Check if startup-config loaded properly
- **Interface down**: Verify physical interface connections in topology
- **QoS not working**: Confirm policies loaded correctly with `show qos`
- **VLAN issues**: Check sub-interface configuration with `show interface`

### Container Networking Issues:
- **PE startup failures**: Check that TE containers started successfully first
- **Interface binding**: Verify eth1/eth2 interfaces exist in TE containers
- **Management connectivity**: Ensure all containers can reach controller

## 🔧 Advanced Configuration Notes

### **ContainerLab Container Naming:**
ContainerLab prefixes all container names with `clab-<topology-name>-`:
- Use `clab-lab-03-controller:8443` in test scripts
- Use `clab-lab-03-te1:5551+clab-lab-03-te1:50071` for port locations
- Use `clab-lab-03-te2:5552+clab-lab-03-te2:50071` for port locations

### **Nokia SRL Access:**
```bash
# SSH access
ssh admin@clab-lab-03-srl
# Password: NokiaSrl1!

# Enter CLI mode if needed
sr_cli

# Configuration commands
enter candidate
set <configuration>
commit now
quit
```

### **Egress Tracking Limitations:**
- **Bit limitation**: Maximum 12 bits for egress tracking fields
- **VLAN ID**: Uses 12 bits (can track alone)
- **DSCP**: Uses 6 bits (can combine with other fields)
- **Combined tracking**: VLAN (12) + DSCP (6) = 18 bits (exceeds limit)

---

**Next Step**: Proceed to L03_Lab_Test_Execution.md to configure egress tracking and start DUT validation testing.