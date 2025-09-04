# L01: Command Reference Card

## 🎯 Quick Command Reference
All commands used in Lab 01 Docker Back-to-Back Testing, organized by section.

---

## 📦 Docker Image Management

### Pull Images
```bash
# Pull KENG Controller (specific version)
docker pull ghcr.io/open-traffic-generator/keng-controller:1.14.0-1

# Pull Ixia-c Traffic Engine (specific version)
docker pull ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99
```

### Verify Images
```bash
# List all images
docker images

# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a
```

---

## 🌐 Network Interface Management

### Create Virtual Interfaces
```bash
# Create veth pair and bring up
sudo ip link add name veth0 type veth peer name veth1 && \
sudo ip link set dev veth0 up && \
sudo ip link set dev veth1 up

# Verify interfaces
ip link
ip addr
```

### Remove Virtual Interfaces
```bash
# Remove veth pair (removes both sides)
sudo ip link delete veth0

# Verify removal
ip link | grep veth  # Should return nothing
```

---

## 🐳 Container Management

### Start KENG Controller
```bash
docker run -d --name controller \
  --network=host \
  ghcr.io/open-traffic-generator/keng-controller:1.14.0-1 \
  --http-port 8443 --accept-eula
```

### Start Traffic Engines
```bash
# Traffic Engine 1 (veth0, port 5551)
docker run -d --name traffic-engine-1 \
  --network=host \
  -e ARG_IFACE_LIST=virtual@af_packet,veth0 \
  -e OPT_NO_HUGEPAGES=Yes \
  --privileged \
  -e OPT_LISTEN_PORT=5551 \
  ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99

# Traffic Engine 2 (veth1, port 5552)
docker run -d --name traffic-engine-2 \
  --network=host \
  -e ARG_IFACE_LIST=virtual@af_packet,veth1 \
  -e OPT_NO_HUGEPAGES=Yes \
  --privileged \
  -e OPT_LISTEN_PORT=5552 \
  ghcr.io/open-traffic-generator/ixia-c-traffic-engine:1.8.0.99
```

### Container Operations
```bash
# Check container status
docker ps -a

# View container logs
docker logs controller
docker logs traffic-engine-1
docker logs traffic-engine-2

# Stop containers
docker stop controller traffic-engine-1 traffic-engine-2

# Remove containers
docker rm controller traffic-engine-1 traffic-engine-2

# Stop and remove in one command
docker stop controller traffic-engine-1 traffic-engine-2 && \
docker rm controller traffic-engine-1 traffic-engine-2
```

---

## 🧪 Test Execution

### Python Script Execution
```bash
# Navigate to lab directory
cd ~/ac2-workshop/lab-01

# View test script
vim lab-01_test.py

# Run test script
python3 lab-01_test.py
```

### Interface Counter Monitoring
```bash
# Save interface counters (before test)
cat /proc/net/dev > counters1.log

# Save interface counters (after test)
cat /proc/net/dev > counters2.log

# Compare counters
diff counters1.log counters2.log
```

---

## 📊 Statistics and Monitoring

### REST API Queries
```bash
# Get flow metrics
curl -k -d '{"choice":"flow"}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get port metrics
curl -k -d '{"choice":"port"}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get specific port metrics
curl -k -d '{"choice":"port","port":{"port_names":["Port-2"]}}' -X POST https://127.0.0.1:8443/monitor/metrics

# Get current configuration
curl -k https://127.0.0.1:8443/config

# Save configuration to file
curl -k https://127.0.0.1:8443/config > ./lab-01-config.json
```

### Configuration Viewing
```bash
# View saved configuration
more lab-01-config.json

# Edit configuration
vi lab-01-config.json
```

---

## 🛠️ OTGEN Tool Usage

### Installation
```bash
# Install otgen tool (version 0.6.2)
bash -c "$(curl -sL https://get.otgcdn.net/otgen)" -- -v 0.6.2
```

### Environment Setup
```bash
# Set environment variables for otgen
export OTG_API="https://localhost:8443"
export OTG_LOCATION_P1="localhost:5551"
export OTG_LOCATION_P2="localhost:5552"
```

### OTGEN Commands
```bash
# Run configuration with flow metrics
otgen run -k -a https://127.0.0.1:8443 -f lab-01-config.json -m flow | \
otgen transform -m flow | \
otgen display --mode table

# Run configuration with port metrics
otgen run -k -a https://127.0.0.1:8443 -f lab-01-config.json -m port | \
otgen transform -m port | \
otgen display --mode table

# Create simple flow and run
otgen create flow -s 1.1.1.1 -d 2.2.2.2 -p 80 --rate 100 --count 2000 | \
otgen run --insecure --metrics flow | \
otgen transform --metrics flow --counters frames | \
otgen display --mode table
```

---

## 🔄 Git Operations

### Version Control
```bash
# Check changes made to files
git diff

# View specific file changes
git diff lab-01_test.py

# Check repository status
git status
```

---

## 🧹 Cleanup Commands

### Complete Cleanup
```bash
# Stop and remove containers
docker stop traffic-engine-1 traffic-engine-2 controller && \
docker rm traffic-engine-1 traffic-engine-2 controller

# Remove virtual interfaces
sudo ip link delete veth0

# Verify cleanup
docker ps -a
ip link && ip addr
```

### Using Cleanup Script
```bash
# Make script executable
chmod +x L01_cleanup_script.sh

# Run cleanup script
./L01_cleanup_script.sh
```

---

## 🚀 Automation Scripts

### Setup Script
```bash
# Make executable and run complete setup
chmod +x L01_setup_script.sh
./L01_setup_script.sh
```

### Test Script
```bash
# Run the lab test script
python3 L01_lab_01_test.py
```

---

## 🔍 Troubleshooting Commands

### Container Diagnostics
```bash
# Check if containers are running
docker ps | grep -E "(controller|traffic-engine)"

# Check container resource usage
docker stats controller traffic-engine-1 traffic-engine-2

# Inspect container configuration
docker inspect controller
```

### Network Diagnostics
```bash
# Check network interfaces
ip link show
ip addr show

# Test API connectivity
curl -k --max-time 5 https://127.0.0.1:8443/config

# Check port availability
netstat -tuln | grep -E "(8443|5551|5552)"
lsof -i :8443
```

### Process Diagnostics
```bash
# Check for conflicting processes
ps aux | grep -E "(controller|traffic-engine)"

# Check system resources
free -h
df -h
```

---

## 📋 Parameter Reference

### Container Parameters
- `--network=host`: Use host networking
- `--privileged`: Required for network interface access
- `-e ARG_IFACE_LIST=virtual@af_packet,vethX`: Specify test interface
- `-e OPT_NO_HUGEPAGES=Yes`: Disable hugepages
- `-e OPT_LISTEN_PORT=XXXX`: Set listening port
- `--http-port 8443`: Controller HTTP port
- `--accept-eula`: Accept license agreement

### Test Parameters
- **Rate**: 100 pps (packets per second)
- **Count**: 2000 packets per direction
- **Frame Size**: 128 bytes (initial)
- **Duration**: ~20 seconds
- **Interfaces**: veth0 ↔ veth1

---

## 🎯 Key Ports
- **8443**: KENG Controller API
- **5551**: Traffic Engine 1
- **5552**: Traffic Engine 2

---

**💡 Pro Tip**: Use `history | grep docker` to quickly find previously used Docker commands!
