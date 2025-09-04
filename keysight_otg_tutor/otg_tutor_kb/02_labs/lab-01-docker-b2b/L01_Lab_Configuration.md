---
title: "Lab 1 Configuration Setup"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Set up Docker containers, network interfaces, and download required images for Lab 1 back-to-back testing."
tags: ["configuration", "docker", "setup", "containers", "networking"]
difficulty: "beginner"
---

## 🚀 Step-by-Step Instructions

### Step 1: Download Docker Images

Pull the specific versions of Ixia-c Controller and Traffic Engine from GitHub Container Registry:

```bash
# Pull KENG Controller (specific version)
docker pull ghcr.io/open-traffic-generator/keng-controller:1.14.0-1

# Pull Ixia-c Traffic Engine (specific version)  
docker pull ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99
```

**Verify images and containers:**
```bash
# Check downloaded images
docker images

# Check running containers
docker ps
```

> 💡 **Note**: Always use specific version tags instead of `latest` for reproducible results. The OTG API model is under active development.

### Step 2: Create Virtual Test Interfaces

Create a virtual interface pair for traffic testing:

```bash
# Create veth pair and bring interfaces up
sudo ip link add name veth0 type veth peer name veth1 && \
sudo ip link set dev veth0 up && \
sudo ip link set dev veth1 up

# Verify interfaces created
ip link
```

### Step 3: Start KENG Controller

Deploy the KENG Controller container:

```bash
# Start KENG Controller
docker run -d --name controller \
  --network=host \
  ghcr.io/open-traffic-generator/keng-controller:1.14.0-1 \
  --http-port 8443 --accept-eula
```

**Parameters explained:**
- `--network=host`: Direct connection to Linux host networking
- `--http-port 8443`: Controller listens on TCP port 8443
- `--accept-eula`: Accepts End User License Agreement

### Step 4: Start Traffic Engine Containers

Deploy two Ixia-c Traffic Engine containers:

```bash
# Start Traffic Engine 1 (connected to veth0)
docker run -d --name traffic-engine-1 \
  --network=host \
  -e ARG_IFACE_LIST=virtual@af_packet,veth0 \
  -e OPT_NO_HUGEPAGES=Yes \
  --privileged \
  -e OPT_LISTEN_PORT=5551 \
  ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99

# Start Traffic Engine 2 (connected to veth1)
docker run -d --name traffic-engine-2 \
  --network=host \
  -e ARG_IFACE_LIST=virtual@af_packet,veth1 \
  -e OPT_NO_HUGEPAGES=Yes \
  --privileged \
  -e OPT_LISTEN_PORT=5552 \
  ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99
```

**Parameters explained:**
- `ARG_IFACE_LIST`: Specifies test interface (virtual@af_packet,vethX)
- `OPT_NO_HUGEPAGES`: Disables hugepages for simpler setup
- `--privileged`: Required for network interface access
- `OPT_LISTEN_PORT`: Unique listening port for each engine


**Verify all containers are running:**
```bash
docker ps -a
```


## Frequent Deployment Errors
Frequent errors encountered when starting the containers include:

• Not specifying the correct management network or not having reachability to that network

• Not specifying the correct interfaces (their name / their type / their order) for the test networks

• Not specifying the different listening ports when multiple similar containers are sharing the same namespace

• Not specifying the correct version of the container image from the registry (when multiple versions of the same image exist)

• Not having the test interfaces successfully created before executing the docker run commands