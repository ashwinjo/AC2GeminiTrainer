---
title: "Lab 4 Test Execution"
lab_id: "lab-04-ixiac-containerlab-dut-convergence"
category: "lab"
objective: "Execute BGP convergence tests with DUT validation, failover testing, and recovery time analysis using Ixia-C-One."
tags: ["execution", "test", "snappi", "python", "bgp", "convergence", "ixia-c-one"]
difficulty: "advanced"
---

# Lab 04: Test Execution with BGP Convergence Testing

## 🚀 Step-by-Step Instructions to run BGP Convergence Test

### Step 1: Deploy the ContainerLab Environment

First, deploy the complete testing infrastructure with Ixia-C-One and Nokia SRL:

```bash
# Deploy Ixia-C-One and Nokia SRL DUT
sudo containerlab deploy -t lab-04.yml
```

**What this creates:**
- **Ixia-C-One**: All-in-one traffic generator on `clab-lab-04-ixia-c-one:8443`
- **Nokia SRL DUT**: Route reflector with pre-configured BGP and interfaces
- **Three connections**: eth1 (traffic), eth2 (BGP peer 1), eth3 (BGP peer 2)

### Step 2: Verify DUT BGP Configuration

Connect to the Nokia SRL DUT to verify the BGP configuration is loaded correctly:

```bash
# Connect to Nokia SRL (password: NokiaSrl1!)
ssh admin@clab-lab-04-srl

# Enter CLI mode if not already there
sr_cli

# Verify BGP configuration
show network-instance default protocols bgp
show network-instance default protocols bgp route-reflector

# Check interface status
show interface ethernet-1/1
show interface ethernet-1/2
show interface ethernet-1/3
```

**🔍 Key configuration elements to verify:**
- **e1-1**: 192.168.11.1/24 (traffic interface)
- **e1-2**: 192.168.22.1/24 (iBGP peer 1)
- **e1-3**: 192.168.33.1/24 (iBGP peer 2)
- **BGP Route Reflector**: Enabled for iBGP peer communication
- **BGP AS**: Configured for internal BGP peering

### Step 3: Configure Test Script for Ixia-C-One

Edit the test script to use the Ixia-C-One all-in-one container:

```bash
# Edit the convergence test script
vi lab-04-1_test.py
```

**🔧 Update the script with Ixia-C-One configuration:**
```python
# Set the Ixia-C-One controller address (all-in-one)
api = snappi.api(location="https://clab-lab-04-ixia-c-one:8443", verify=False)

# Configure ports using direct interface names
p1 = c.ports.add(name="p1", location="eth1")  # Traffic interface
p2 = c.ports.add(name="p2", location="eth2")  # iBGP peer 1
p3 = c.ports.add(name="p3", location="eth3")  # iBGP peer 2
```

> 🔧 **Ixia-C-One Simplification**: Unlike previous labs with separate containers and complex port addressing, Ixia-C-One uses simple interface names (eth1, eth2, eth3).

### Step 4: Understand the BGP Convergence Test Configuration

**📋 Understanding the lab-04-1_test.py Script Architecture:**

The convergence test script demonstrates several advanced concepts:

#### **4.1: iBGP Configuration**
```python
# Configure iBGP on eth2 and eth3
# Both peers advertise the same routes but with different BGP attributes

# BGP Peer 1 (eth2) - Higher Local Preference (preferred path)
bgp_peer_1.local_preference = 200
bgp_peer_1.med = 100

# BGP Peer 2 (eth3) - Lower Local Preference (backup path)
bgp_peer_2.local_preference = 100
bgp_peer_2.med = 200
```

#### **4.2: Route Advertisement**
- Both BGP peers advertise the same IPv4 prefixes
- Different BGP attributes (Local Preference, MED) influence path selection
- Nokia SRL acts as route reflector, enabling iBGP peer communication

#### **4.3: Traffic Generation**
- Bidirectional flows created using BGP-learned routes as destinations
- Traffic initially follows best path (higher Local Preference)
- Convergence events trigger path changes

### Step 5: Execute the BGP Convergence Test

Run the convergence test with different failure scenarios:

```bash
python3 lab-04-1_test.py
```

## 📋 Understanding the Convergence Test Scenarios

### **Scenario 1: Link Down Event (Hard Failure)**

**What happens:**
1. **Baseline Traffic**: Traffic flows via eth2 (best path due to higher Local Preference)
2. **Link Down Event**: Physical link failure simulated on eth2 interface
3. **BGP Detection**: Nokia SRL detects link failure and removes routes
4. **Convergence**: Traffic switches to eth3 (backup path)
5. **Recovery Measurement**: Convergence time calculated based on packet loss

**Expected behavior:**
```
Before Link Down:
Traffic: eth1 → SRL → eth2 (best path)
BGP Best Path: 192.168.22.2 (eth2 peer)

After Link Down:
Traffic: eth1 → SRL → eth3 (backup path)  
BGP Best Path: 192.168.33.2 (eth3 peer)
```

### **Scenario 2: Route Withdrawal Event (Soft Failure)**

**What happens:**
1. **Baseline Traffic**: Traffic flows via eth2 (best path)
2. **Route Withdrawal**: BGP UPDATE message withdraws routes from eth2 peer
3. **BGP Processing**: Nokia SRL processes withdrawal and selects new best path
4. **Traffic Switch**: Traffic switches to eth3 without physical link failure
5. **Faster Recovery**: Typically faster than link down as physical layer remains active

**Key difference from Link Down:**
- Physical link remains operational
- Only routing information changes
- Generally faster convergence time
- No physical failure detection delay

## 🔧 Advanced Test Configuration

### **Enable Link Down Testing:**
```python
# Configure link down event in test script
link_operation = api.control_action()
link_operation.protocol.choice = link_operation.protocol.LINK
link_operation.protocol.link.port_names = ["eth2"]
link_operation.protocol.link.state = link_operation.protocol.link.DOWN

# Execute link down during test
api.set_control_action(link_operation)
```

### **Enable Route Withdrawal Testing:**
```python
# Configure route withdrawal event
route_withdraw = api.control_action()
route_withdraw.protocol.choice = route_withdraw.protocol.ROUTE
route_withdraw.protocol.route.names = ["bgp_routes_eth2"]
route_withdraw.protocol.route.state = route_withdraw.protocol.route.WITHDRAW

# Execute route withdrawal during test
api.set_control_action(route_withdraw)
```

### **BGP Attribute Configuration:**
```python
# Configure BGP Local Preference and MED for path selection
bgp_peer_eth2.local_preference = 200  # Higher preference (primary path)
bgp_peer_eth2.med = 100

bgp_peer_eth3.local_preference = 100  # Lower preference (backup path)  
bgp_peer_eth3.med = 200
```

## 🔍 Real-Time Monitoring During Test Execution

### **Monitor BGP Sessions on DUT:**
```bash
# In separate terminal, connect to Nokia SRL
ssh admin@clab-lab-04-srl

# Watch BGP route changes during convergence
watch show network-instance default protocols bgp routes ipv4 summary

# Monitor BGP neighbor status
watch show network-instance default protocols bgp neighbor
```

**What to observe:**
- **Before Event**: Best route next hop is 192.168.22.2 (eth2 peer)
- **During Event**: Route disappears or becomes unreachable
- **After Event**: Best route next hop becomes 192.168.33.2 (eth3 peer)

### **Monitor Traffic Flow Changes:**
```bash
# Check OTG flow metrics during test
curl -k https://clab-lab-04-ixia-c-one:8443/api/v1/results/metrics

# Monitor port statistics
curl -k -X POST https://clab-lab-04-ixia-c-one:8443/api/v1/results/metrics \
  -H "Content-Type: application/json" \
  -d '{"choice": "port"}'
```

## 📊 Convergence Time Analysis

### **Understanding Convergence Metrics:**

**Convergence Time Calculation:**
```
Convergence Time = (Number of Lost Packets ÷ Transmission Rate) seconds

Example:
- Lost Packets: 50
- Transmission Rate: 100 pps  
- Convergence Time: 50 ÷ 100 = 0.5 seconds
```

**Factors Affecting Convergence Time:**
1. **Failure Detection Time**: How quickly the failure is detected
2. **BGP Processing Time**: Route calculation and best path selection
3. **Forwarding Table Update**: Data plane programming time
4. **Number of Routes**: More routes = longer processing time

### **Comparing Convergence Scenarios:**

**Link Down vs Route Withdrawal:**
```
Link Down (Hard Failure):
- Physical failure detection required
- BGP session timeout
- Longer convergence time
- Complete path failure

Route Withdrawal (Soft Failure):  
- Immediate BGP UPDATE processing
- No physical detection delay
- Faster convergence time
- Graceful path change
```

## 🔧 Advanced Testing Scenarios

### **Variable Route Count Testing:**
```bash
# Test with different route counts
vim lab-04-1_test.py

# Change route advertisement count
route_count = 50  # Test with 50 routes
route_count = 100 # Test with 100 routes
route_count = 500 # Test with 500 routes
```

**Expected behavior:**
- More routes = longer convergence time
- Linear relationship between route count and processing time
- Demonstrates scalability impact on convergence

### **Multiple Failure Scenarios:**
```python
# Sequential failure testing
def test_sequential_failures():
    # 1. Test link down scenario
    execute_link_down_test()
    
    # 2. Wait for recovery
    wait_for_convergence()
    
    # 3. Test route withdrawal scenario
    execute_route_withdrawal_test()
    
    # 4. Analyze comparative results
    analyze_convergence_differences()
```

## 🔍 Troubleshooting Common Issues

### **BGP Session Issues:**
```bash
# Check BGP session status
ssh admin@clab-lab-04-srl
show network-instance default protocols bgp neighbor

# Common issues:
# - BGP sessions not establishing
# - Routes not being advertised
# - Path selection not working as expected
```

### **Ixia-C-One Connectivity Issues:**
```bash
# Test API connectivity
curl -k https://clab-lab-04-ixia-c-one:8443/api/v1/version

# Check container logs
docker logs clab-lab-04-ixia-c-one

# Verify interface status
docker exec -it clab-lab-04-ixia-c-one ip addr
```

### **Convergence Test Issues:**
- **No convergence detected**: Check if failure events are properly triggered
- **Unexpected convergence time**: Verify route count and BGP attributes
- **Traffic not switching paths**: Confirm BGP best path selection working

## 📊 Test Result Analysis

### **Successful Test Indicators:**
- ✅ iBGP sessions established between Ixia-C-One and Nokia SRL
- ✅ Routes advertised and received with correct BGP attributes  
- ✅ Traffic flows via best path (eth2) during steady state
- ✅ Convergence events successfully trigger path changes
- ✅ Traffic recovers via backup path (eth3) after convergence
- ✅ Convergence time measured and within expected ranges

### **Convergence Analysis Results:**
```
Typical Results:
- Link Down Convergence: 1-3 seconds (depends on BGP timers)
- Route Withdrawal Convergence: 0.1-0.5 seconds (faster processing)
- Packet Loss: 50-300 packets (depends on rate and convergence time)
- Route Count Impact: +10-50ms per 100 additional routes
```

## 🎯 Key Learning Points

### **BGP Convergence Concepts:**
- **iBGP vs eBGP**: Internal BGP requires route reflector for peer communication
- **Path Selection**: Local Preference and MED influence best path selection
- **Convergence Types**: Hard failures vs soft failures have different characteristics
- **Scalability**: Route count directly impacts convergence time

### **Ixia-C-One Benefits:**
- **Simplified Architecture**: Single container vs multiple components
- **Integrated Management**: No separate controller container needed
- **Direct Interface Access**: Simple eth1, eth2, eth3 addressing
- **Resource Efficiency**: Lower overhead for convergence testing

### **Production Applications:**
- **Network Resilience Testing**: Validate failover capabilities before deployment
- **SLA Validation**: Ensure convergence times meet service requirements
- **Capacity Planning**: Understand impact of route scale on convergence
- **Operational Readiness**: Test network behavior under failure conditions

---

**Next Step**: Proceed to L04_Lab_Metrics.md to learn advanced convergence analysis techniques and detailed metrics interpretation for BGP convergence testing.