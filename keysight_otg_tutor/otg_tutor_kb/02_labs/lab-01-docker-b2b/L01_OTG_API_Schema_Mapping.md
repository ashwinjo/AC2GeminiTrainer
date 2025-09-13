# OTG API Schema Mapping for Lab 01

This document explains how each function in the refactored Lab 01 test maps to the Open Traffic Generator (OTG) API schema components.

## Overview

The OTG API follows a hierarchical schema structure where configuration objects contain nested components. Understanding this mapping helps developers work effectively with traffic generation tools.

## Schema Hierarchy

```
API Root
├── Configuration
│   ├── Ports[]
│   └── Flows[]
│       ├── TxRx
│       ├── Size  
│       ├── Rate
│       ├── Duration
│       ├── Metrics
│       └── Packet[]
│           ├── Ethernet
│           ├── IPv4
│           └── UDP
├── ControlState
│   └── Traffic
│       └── FlowTransmit
└── MetricsRequest
    └── Port
```

## Function-to-Schema Mapping

### 1. `create_api_connection()`

**OTG Schema Components:**
- **Root API Object**: Entry point to all OTG operations
- **Connection**: Establishes communication with traffic generator

**Code Example:**
```python
api = snappi.api(location="https://127.0.0.1:8443", verify=False)
```

**Schema Mapping:**
- `snappi.api()` → Creates the root API client instance
- `location` → Specifies the traffic generator endpoint
- Different generators use different location formats:
  - Ixia-C: `https://<ip>:<port>`
  - IxNetwork: `https://<ip>:<port>` with `ext="ixnetwork"`
  - TRex: `<ip>:<port>` with `ext="trex"`

### 2. `create_base_configuration()`

**OTG Schema Components:**
- **Config**: Root configuration container

**Code Example:**
```python
configuration = api.config()
```

**Schema Mapping:**
- `api.config()` → Creates empty `Config` object
- This object will contain all test configuration (ports, flows, etc.)

### 3. `configure_ports()`

**OTG Schema Components:**
- **Config.ports[]**: Array of Port objects
- **Port.name**: Logical name for the port
- **Port.location**: Physical/virtual port identifier

**Code Example:**
```python
port1, port2 = (
    configuration.ports
    .port(name="Port-1", location="127.0.0.1:5551")
    .port(name="Port-2", location="127.0.0.1:5552")
)
```

**Schema Mapping:**
- `configuration.ports` → Access to `Config.ports[]` array
- `.port(name, location)` → Creates new `Port` object
- `Port.name` → String identifier used in flows
- `Port.location` → Platform-specific port address

### 4. `configure_traffic_flows()`

**OTG Schema Components:**
- **Config.flows[]**: Array of Flow objects
- **Flow.name**: Descriptive name for the flow
- **Flow.metrics.enable**: Boolean to enable statistics collection
- **Flow.tx_rx.port**: Defines transmit and receive ports

**Code Example:**
```python
flow1, flow2 = (
    configuration.flows
    .flow(name="Flow #1 - Port 1 > Port 2")
    .flow(name="Flow #2 - Port 2 > Port 1")
)

flow1.metrics.enable = True
flow1.tx_rx.port.tx_name = port1.name
flow1.tx_rx.port.rx_names = [port2.name]
```

**Schema Mapping:**
- `configuration.flows` → Access to `Config.flows[]` array
- `.flow(name)` → Creates new `Flow` object
- `Flow.metrics.enable` → Boolean for statistics collection
- `Flow.tx_rx.port.tx_name` → Source port name
- `Flow.tx_rx.port.rx_names[]` → Array of destination port names

### 5. `configure_flow_properties()`

**OTG Schema Components:**
- **Flow.size.fixed**: Fixed packet size in bytes
- **Flow.rate.pps**: Transmission rate in packets per second
- **Flow.duration.fixed_packets.packets**: Number of packets to send

**Code Example:**
```python
flow1.size.fixed = 128
f.duration.fixed_packets.packets = 2000
f.rate.pps = 100
```

**Schema Mapping:**
- `Flow.size.fixed` → `FlowSize.fixed` (integer, bytes)
- `Flow.rate.pps` → `FlowRate.pps` (integer, packets/second)
- `Flow.duration.fixed_packets.packets` → `FlowDurationFixedPackets.packets` (integer)

### 6. `configure_packet_headers()`

**OTG Schema Components:**
- **Flow.packet[]**: Array of protocol headers
- **FlowEthernet**: Ethernet header configuration
- **FlowIpv4**: IPv4 header configuration  
- **FlowUdp**: UDP header configuration

**Code Example:**
```python
eth1 = flow1.packet.add().ethernet
ip1 = flow1.packet.add().ipv4
udp1 = flow1.packet.add().udp

eth1.src.value = "00:AA:00:00:01:00"
ip1.src.value = "10.0.0.1"
```

**Schema Mapping:**
- `flow.packet.add().ethernet` → Creates `FlowEthernet` header
- `flow.packet.add().ipv4` → Creates `FlowIpv4` header
- `flow.packet.add().udp` → Creates `FlowUdp` header
- `ethernet.src.value` → `FlowEthernet.src.value` (MAC address string)
- `ipv4.src.value` → `FlowIpv4.src.value` (IP address string)

### 7. `configure_udp_port_patterns()`

**OTG Schema Components:**
- **FlowUdp.src_port.increment**: Incrementing pattern for source ports
- **FlowUdp.dst_port.values**: List of destination port values
- **FlowUdpSrcPortIncrement**: Configuration for increment pattern

**Code Example:**
```python
udp1.src_port.increment.start = 5100
udp1.src_port.increment.step = 2
udp1.src_port.increment.count = 10
udp1.dst_port.values = [6100, 6125, 6150, 6170, 6190]
```

**Schema Mapping:**
- `udp.src_port.increment` → `FlowUdpSrcPort.increment`
- `increment.start` → `FlowUdpSrcPortIncrement.start` (integer)
- `increment.step` → `FlowUdpSrcPortIncrement.step` (integer)  
- `increment.count` → `FlowUdpSrcPortIncrement.count` (integer)
- `udp.dst_port.values` → `FlowUdpDstPort.values[]` (integer array)

### 8. `apply_configuration()`

**OTG Schema Components:**
- **Config**: Complete configuration object validation and deployment

**Code Example:**
```python
api.set_config(configuration)
```

**Schema Mapping:**
- `api.set_config()` → Validates entire `Config` object against OTG schema
- Pushes configuration to traffic generator for validation and setup

### 9. `start_traffic()`

**OTG Schema Components:**
- **ControlState**: Traffic control operations
- **ControlState.traffic.flow_transmit**: Flow transmission control
- **FlowTransmitState**: START/STOP/PAUSE states

**Code Example:**
```python
cs = api.control_state()
cs.choice = cs.TRAFFIC
cs.traffic.choice = cs.traffic.FLOW_TRANSMIT
cs.traffic.flow_transmit.state = cs.traffic.flow_transmit.START
api.set_control_state(cs)
```

**Schema Mapping:**
- `api.control_state()` → Creates `ControlState` object
- `cs.choice = cs.TRAFFIC` → Sets control type to traffic operations
- `cs.traffic.choice = cs.traffic.FLOW_TRANSMIT` → Sets traffic control to flow transmission
- `cs.traffic.flow_transmit.state = START` → Sets transmission state to START
- `api.set_control_state()` → Applies the control state

### 10. `verify_traffic_statistics()`

**OTG Schema Components:**
- **MetricsRequest**: Request object for statistics collection
- **PortMetricsRequest**: Port-specific metrics configuration
- **MetricsResponse**: Response containing actual statistics
- **PortMetric**: Individual port statistics

**Code Example:**
```python
statistics = api.metrics_request()
statistics.port.port_names = [p.name for p in configuration.ports]
statistics.port.column_names = [statistics.port.FRAMES_TX, statistics.port.FRAMES_RX]
results = api.get_metrics(statistics)
```

**Schema Mapping:**
- `api.metrics_request()` → Creates `MetricsRequest` object
- `statistics.port.port_names[]` → `PortMetricsRequest.port_names[]` (string array)
- `statistics.port.column_names[]` → `PortMetricsRequest.column_names[]` (enum array)
- `api.get_metrics()` → Returns `MetricsResponse` object
- `results.port_metrics[]` → Array of `PortMetric` objects
- `port_metric.frames_tx` → `PortMetric.frames_tx` (integer counter)
- `port_metric.frames_rx` → `PortMetric.frames_rx` (integer counter)

## Key Schema Concepts

### 1. **Hierarchical Structure**
The OTG schema follows a tree structure where each level contains specific configuration options:
- **Config** (root) → **Flows** → **Packet** → **Headers**
- **Config** (root) → **Ports** 
- **ControlState** → **Traffic** → **FlowTransmit**

### 2. **Object Creation Patterns**
- **Fluent API**: Chain method calls for readable configuration
- **Array Access**: Use indices to access specific objects in arrays
- **Property Setting**: Direct assignment to object properties

### 3. **Validation**
- Schema validation occurs when `api.set_config()` is called
- Invalid configurations are rejected with detailed error messages
- All required fields must be populated

### 4. **Stateful Operations**
- Configuration is stateful - once applied, it persists until changed
- Control operations (start/stop) operate on the current configuration
- Statistics reflect the current state of traffic generation

## Benefits of Schema Understanding

1. **Predictable API**: Understanding the schema makes the API behavior predictable
2. **Error Prevention**: Knowing required fields prevents configuration errors
3. **Extensibility**: Schema knowledge enables adding new features easily
4. **Debugging**: Understanding the structure helps troubleshoot issues
5. **Tool Independence**: Schema concepts apply across different traffic generators

## Next Steps

- Explore advanced packet patterns (incrementing fields, random values)
- Learn about protocol-specific configurations (VLAN, MPLS, etc.)
- Understand performance optimization through schema choices
- Study error handling and validation messages
