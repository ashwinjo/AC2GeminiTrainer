# Lab 01 Step-by-Step Guide for First-Time Users

This guide walks through the refactored Lab 01 test, explaining each step in detail for users new to the Open Traffic Generator (OTG) API.

## Prerequisites

Before running this test, ensure you have:
- Docker containers running for the traffic generator
- Snappi Python library installed (`pip install snappi`)
- Basic understanding of network protocols (Ethernet, IP, UDP)

## Test Overview

This test demonstrates bidirectional traffic generation between two ports:
- **Goal**: Send 2000 packets in each direction at 100 packets per second
- **Validation**: Verify all packets are transmitted and received correctly
- **Duration**: Approximately 20 seconds per direction

## Step-by-Step Walkthrough

### Step 1: Create API Connection
```python
api = create_api_connection()
```

**What happens here:**
- Establishes connection to the traffic generator controller
- Uses HTTPS connection to localhost on port 8443
- This is the entry point for all OTG operations

**First-time user notes:**
- The controller manages the traffic generation hardware/software
- Different traffic generators use different connection formats
- Connection must succeed before any configuration can be applied

### Step 2: Create Base Configuration
```python
configuration = create_base_configuration(api)
```

**What happens here:**
- Creates an empty configuration object
- This object will hold all test settings (ports, flows, packets)
- Think of it as a blueprint for your test

**First-time user notes:**
- Configuration is hierarchical - ports contain flows, flows contain packets
- Nothing is applied to hardware until `set_config()` is called
- You can build the entire configuration before applying it

### Step 3: Configure Test Ports
```python
port1, port2 = configure_ports(configuration)
```

**What happens here:**
- Defines two logical ports for the test
- Maps logical names to physical/virtual port locations
- Port locations specify where packets will be sent/received

**First-time user notes:**
- Port names are used to reference ports in flows
- Port locations are platform-specific (Docker uses IP:port format)
- You must have access to the specified port locations

### Step 4: Configure Traffic Flows
```python
flow1, flow2 = configure_traffic_flows(configuration, port1, port2)
```

**What happens here:**
- Creates two traffic flows for bidirectional testing
- Flow 1: Port 1 → Port 2
- Flow 2: Port 2 → Port 1
- Enables statistics collection for both flows

**First-time user notes:**
- Flows define the direction of traffic
- Each flow can have different packet formats and rates
- Statistics must be enabled to collect performance data

### Step 5: Configure Flow Properties
```python
configure_flow_properties(configuration, flow1, flow2)
```

**What happens here:**
- Sets packet size to 128 bytes
- Sets transmission rate to 100 packets per second
- Sets duration to 2000 packets total per flow

**First-time user notes:**
- Packet size affects bandwidth utilization
- Rate determines how fast packets are sent
- Duration controls when transmission stops

### Step 6: Configure Packet Headers
```python
eth1, ip1, udp1, eth2, ip2, udp2 = configure_packet_headers(flow1, flow2)
```

**What happens here:**
- Adds Ethernet, IPv4, and UDP headers to each flow
- Creates the protocol stack for each packet
- Sets up the foundation for addressing

**First-time user notes:**
- Headers are processed in order (Ethernet → IPv4 → UDP)
- Each header adds specific protocol information
- This creates the basic packet structure

### Step 7: Configure UDP Port Patterns
```python
configure_udp_port_patterns(udp1, udp2)
```

**What happens here:**
- Sets up varying UDP port numbers for traffic diversity
- Uses increment patterns for source ports
- Uses value lists for destination ports

**First-time user notes:**
- Port patterns create traffic variation
- Increment patterns automatically vary values
- Value lists specify exact values to use
- This helps test different network paths

### Step 8: Apply Configuration
```python
apply_configuration(api, configuration)
```

**What happens here:**
- Validates the complete configuration
- Pushes configuration to the traffic generator
- Prepares hardware/software for traffic generation

**First-time user notes:**
- This is where errors are caught (invalid settings, unreachable ports)
- Configuration is now "live" on the traffic generator
- Changes require creating and applying a new configuration

### Step 9: Start Traffic
```python
start_traffic(api)
```

**What happens here:**
- Sends control command to begin packet transmission
- Traffic generator starts sending packets according to configuration
- Both flows begin transmitting simultaneously

**First-time user notes:**
- Traffic starts immediately when this command is sent
- Packets are generated according to the configured rate
- Traffic continues until the configured duration is reached

### Step 10: Verify Statistics
```python
verify_traffic_statistics(api, configuration)
```

**What happens here:**
- Continuously polls the traffic generator for statistics
- Compares actual results with expected values
- Determines if the test passed or failed

**First-time user notes:**
- Statistics are updated in real-time during traffic generation
- The function waits for traffic to complete before final verification
- Pass/fail is based on packet counts matching expectations

## Understanding the Output

When you run the test, you'll see output like this:

```
Creating API connection to controller...
API connection established successfully
Creating base configuration object...
Base configuration object created
Configuring test ports...
Ports configured: Port-1, Port-2
...
====================================================================================
                                        Expected    Tx      Rx
2024-01-15 10:30:45 TOTAL               4000        4000    4000
====================================================================================
Test PASSED in 0:00:22.153456
```

**What this means:**
- **Expected**: Total packets that should be sent (2000 × 2 flows = 4000)
- **Tx**: Total packets transmitted by all ports
- **Rx**: Total packets received by all ports
- **Test result**: PASSED if Tx = Expected and Rx ≥ Expected

## Common Issues for First-Time Users

### 1. Connection Failures
**Symptom**: "Connection refused" or timeout errors
**Solution**: Verify Docker containers are running and ports are accessible

### 2. Configuration Errors
**Symptom**: Schema validation failures
**Solution**: Check that all required fields are set and values are valid

### 3. Port Access Issues
**Symptom**: "Port not found" or "Permission denied"
**Solution**: Verify port locations and ensure no other processes are using them

### 4. Statistics Mismatches
**Symptom**: Rx count less than Tx count
**Solution**: Check network connectivity between ports, look for packet drops

## Key Concepts to Remember

1. **Configuration First**: Always configure before starting traffic
2. **Bidirectional Testing**: Use multiple flows to test both directions
3. **Statistics Validation**: Always verify results match expectations
4. **Error Handling**: Check return values and handle exceptions
5. **Resource Cleanup**: Stop traffic and clean up resources when done

## Next Steps

After understanding this basic test:
1. Try modifying packet sizes and rates
2. Add more protocol headers (VLAN, TCP, etc.)
3. Experiment with different traffic patterns
4. Learn about advanced statistics collection
5. Explore performance optimization techniques

## Files Created

1. **L01_lab_01_test_refactored.py**: Refactored test code with smaller functions
2. **L01_OTG_API_Schema_Mapping.md**: Detailed OTG API schema documentation
3. **L01_Step_by_Step_Guide.md**: This step-by-step guide for beginners
