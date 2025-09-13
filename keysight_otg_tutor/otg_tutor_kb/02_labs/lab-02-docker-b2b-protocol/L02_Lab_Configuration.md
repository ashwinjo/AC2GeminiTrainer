---
title: "Lab 2 Configuration Setup"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Set up Docker Compose orchestration with protocol engines, custom networking, and BGP configuration for Lab 2."
tags: ["configuration", "docker-compose", "setup", "containers", "protocol-engine", "bgp", "networking"]
difficulty: "intermediate"
---

# Lab 02: Configuration Setup with Docker Compose Orchestration

## 🎯 Overview
Unlike Lab 01 which used simple `docker run` commands with host networking, Lab 02 uses **Docker Compose orchestration** with a **shared network architecture**. This approach is necessary because:
- **Protocol engines require specific port configurations** (all PE containers must listen on port 50071)
- **Port conflicts would occur** with multiple PE containers on host networking
- **Shared network namespaces** allow PE and TE containers to work together efficiently
- **Automated deployment** handles complex multi-container dependencies and networking

## 🚀 Step-by-Step Instructions

### Step 1: Deploy with Docker Compose

Deploy all containers using Docker Compose orchestration:

```bash
# Deploy all 5 containers with custom networking
docker-compose -f L02_lab_topo.yaml -d
```

> 🔧 **Alternative Command**: If docker-compose is installed as a Docker plugin:
> ```bash
> docker compose -f compose.yml up -d
> ```
> Notice the missing dash between "docker" and "compose"

**🧠 What's happening behind the scenes:**
- **Automatic Image Download**: Docker Compose automatically downloads any missing Docker images
- **Shared Network Architecture**: PE containers share network namespaces with their paired TE containers
- **Port Management**: Each TE reserves ports for both itself and its paired PE
- **Service Dependencies**: Ensures containers start in the correct order
- **Volume Mounting**: Mounts necessary directories for configuration and logs

### Step 2: Connect Container Test Interfaces

Connect the traffic engine containers using virtual ethernet pairs:

```bash
# Connect TE containers with veth pairs using IP namespaces
sudo bash /home/ubuntu/AC2GeminiTrainer/keysight_otg_tutor/otg_tutor_kb/02_labs/lab-02-docker-b2b-protocol/L02_connect_containers_veth.sh lab-02-docker-b2b-protocol_traffic_engine_1_1 
  lab-02-docker-b2b-protocol_traffic_engine_2_1 veth0 veth1
```

**🧠 What's happening behind the scenes:**
- **IP Namespaces**: The script uses `ip netns` to create network namespaces for each TE container
- **veth0 on TE1**: Creates the first end of the virtual ethernet pair in traffic-engine-1
- **veth1 on TE2**: Creates the second end of the virtual ethernet pair in traffic-engine-2
- **Back-to-Back Connection**: These veth pairs create a direct back-to-back connection between containers
- **Namespace Isolation**: Each container has its own network namespace, preventing interface conflicts

> ⚠️ **Why we need this script**: Unlike host networking in Lab 01, containers in custom bridge networks are isolated. The script creates virtual interfaces that bridge this isolation for traffic testing.

### Step 3: Verify Deployment

Check that all containers are running successfully:

```bash
# Check all container status
docker ps
```

**Expected output:** You should see 5 containers running:
- `lab-02_keng-controller_1` (KENG Controller)
- `lab-02_traffic_engine_1_1` (Traffic Engine 1)
- `lab-02_traffic_engine_2_1` (Traffic Engine 2)  
- `lab-02_protocol_engine_1_1` (Protocol Engine 1)
- `lab-02_protocol_engine_2_1` (Protocol Engine 2)

**🧠 Why different networking approach:**
- **Host Network (Lab 01)**: Simple but limited - containers share host network stack directly
- **Shared Network (Lab 02)**: PE and TE containers share network namespaces using `network_mode: service:`
- **Protocol Engine Constraint**: All PE containers must listen on port 50071 internally
- **Port Conflict Resolution**: Multiple PEs can coexist by sharing TE network namespaces
- **Efficient Communication**: PE and TE communicate via shared memory/IPC, not network calls

### Step 4: Verify Interface Connectivity

Check that the virtual interfaces were created successfully in the traffic engines:

```bash
# Check Traffic Engine 1 logs for veth0 interface
docker logs lab-02_traffic_engine_1_1

# Check Traffic Engine 2 logs for veth1 interface  
docker logs lab-02_traffic_engine_2_1
```

**🔍 What to look for in logs:**
- Interface discovery messages showing `veth0` and `veth1`
- Successful interface binding confirmations
- No error messages about missing interfaces

> ⚠️ **Troubleshooting**: If interfaces are not found in the logs, you may need to redeploy or restart:
> ```bash
> docker-compose restart
> ```

### Step 5: Inspect Custom Bridge Network

Examine the Docker Compose-created networking:

```bash
# List all Docker networks (look for lab-02_default)
docker network ls

# Inspect the custom bridge network details
docker inspect lab-02_default

# Check container IP addresses within the custom network
docker exec -it lab-02_traffic_engine_1_1 ip addr
```

**🧠 Understanding the shared network architecture:**

#### The Elegant Network Solution: `network_mode: service:`
Lab 02 uses a sophisticated networking approach where **two separate containers share the same network namespace**:

```yaml
# Traffic Engine provides the network namespace
traffic_engine_1:
  ports:
    - "5551:5551"    # TE listens here  
    - "50071:50071"  # PE will listen here (same network space)

# Protocol Engine shares TE's network namespace  
protocol_engine_1:
  network_mode: service:traffic_engine_1  # 🔑 Key: shared network!
```

#### Two Network Layers:
1. **Shared Container Networks**:
   - **TE1 + PE1**: Share same network namespace, both access veth0
   - **TE2 + PE2**: Share same network namespace, both access veth1
   - **Communication**: PE ↔ TE via shared memory/IPC (ultra-fast)

2. **Virtual Ethernet Connection (veth0 ↔ veth1)**:
   - **Purpose**: Data plane traffic testing between TE containers
   - **Connection**: Direct back-to-back connection for packet transmission
   - **Access**: Both TE and PE can use the veth interfaces directly

#### Shared Network Space Visualization:
```
┌─────────────────────────────────────────────────────────┐
│ Shared Network Namespace (TE1's network)               │
│                                                         │
│ ┌─────────────────┐         ┌─────────────────────────┐ │
│ │ TE1 Container   │         │ PE1 Container           │ │
│ │ Process         │         │ Process                 │ │
│ │                 │         │                         │ │
│ │ Listens on:     │         │ Listens on:             │ │
│ │ 0.0.0.0:5551    │ ←─────→ │ 0.0.0.0:50071          │ │
│ │                 │  Same   │                         │ │
│ │ veth0 access    │ Network │ veth0 access            │ │
│ │                 │ Stack   │                         │ │
│ └─────────────────┘         └─────────────────────────┘ │
│                                                         │
│ Network Interfaces: veth0, bridge connection           │
│ Port bindings: 5551 (TE), 50071 (PE)                  │
└─────────────────────────────────────────────────────────┘
                              ↕
                    Host Port Mapping
                    5551:5551, 50071:50071
```

**🔧 Why this shared network architecture is brilliant:**
- **No Port Conflicts**: Each TE/PE pair gets its own network namespace
- **Ultra-Fast Communication**: PE and TE communicate via shared memory, not network calls
- **Resource Efficiency**: No network overhead between PE and TE containers
- **Interface Sharing**: Both containers can directly access the same veth interface
- **Elegant Port Management**: TE "reserves" port 50071 for PE to use

## 🎯 Configuration Summary

After successful deployment, you will have:
- **5 containers** running with shared network architecture:
  - **TE1 + PE1**: Sharing network namespace with ports 5551 and 50071
  - **TE2 + PE2**: Sharing network namespace with ports 5552 and 50072
  - **Controller**: Running independently
- **Virtual ethernet pairs** (veth0 ↔ veth1) connecting TE containers for data plane testing
- **Shared interface access** allowing both TE and PE to use the same veth interfaces
- **Ultra-efficient PE ↔ TE communication** via shared memory instead of network calls
- **BGP protocol engines** ready for configuration and peering

## ⚠️ Common Deployment Issues

### Network-Related Issues:
- **Interface not found**: Run `docker-compose restart` to recreate interfaces
- **Port conflicts**: Check that external ports in compose.yml are not in use
- **Bridge network issues**: Restart Docker daemon if custom bridge creation fails

### Container Issues:
- **PE startup failures**: Check logs for port binding errors on 50071
- **TE interface binding**: Verify veth interfaces exist in container namespaces
- **Service dependencies**: Ensure all containers start in correct order

---

**Next Step**: Proceed to L02_Lab_Test_Execution.md to configure BGP sessions and start protocol testing.
