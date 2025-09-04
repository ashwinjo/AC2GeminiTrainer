# R02: Common API Snippets

## 🎯 Overview
This reference contains frequently used OTG API code snippets, patterns, and examples. Use these as building blocks for your own tests and automation scripts.

---

## 🔧 Basic Client Setup

### Python Client Initialization
```python
from otg_client import OtgClient
import time
import json

# Basic client setup
client = OtgClient("http://localhost:8080")

# Client with timeout and retries
client = OtgClient(
    base_url="http://localhost:8080",
    timeout=30,
    max_retries=3
)

# Client with authentication (if required)
client = OtgClient(
    base_url="https://otg-server.company.com:8443",
    headers={"Authorization": "Bearer your-token-here"},
    verify_ssl=True
)
```

### Async Client Setup
```python
import asyncio
from otg_client import AsyncOtgClient

async def main():
    async with AsyncOtgClient("http://localhost:8080") as client:
        # Your async code here
        config = await client.get_config()
        await client.set_config(new_config)

# Run async function
asyncio.run(main())
```

---

## 📋 Configuration Patterns

### Basic Device and Port Setup
```python
from otg_client.models import Config, Device, Port

def create_basic_config():
    """Create basic two-device configuration"""
    config = Config()
    
    # Create devices
    device_a = Device(name="device_a")
    device_b = Device(name="device_b")
    
    # Create ports
    port_a = Port(name="port_a", location="eth0")
    port_b = Port(name="port_b", location="eth1")
    
    # Assign ports to devices
    device_a.ports = [port_a]
    device_b.ports = [port_b]
    
    # Add devices to configuration
    config.devices = [device_a, device_b]
    
    return config
```

### Multiple Device Setup
```python
def create_multi_device_config(device_count=4):
    """Create configuration with multiple devices"""
    config = Config()
    devices = []
    
    for i in range(device_count):
        device = Device(name=f"device_{i}")
        port = Port(name=f"port_{i}", location=f"eth{i}")
        device.ports = [port]
        devices.append(device)
    
    config.devices = devices
    return config
```

---

## 🌊 Flow Configuration

### Basic Flow Setup
```python
from otg_client.models import Flow, FlowTx, FlowRx, FlowRate, FlowSize, FlowDuration

def create_basic_flow():
    """Create basic unidirectional flow"""
    flow = Flow(
        name="basic_flow",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b")
    )
    
    # Configure rate (1000 packets per second)
    flow.rate = FlowRate(pps=1000)
    
    # Configure packet size (64 bytes)
    flow.size = FlowSize(fixed=64)
    
    # Configure duration (10,000 packets)
    flow.duration = FlowDuration(packets=10000)
    
    return flow
```

### Multiple Flows
```python
def create_multiple_flows():
    """Create multiple flows with different characteristics"""
    flows = []
    
    # Flow 1: Small packets, high rate
    flow1 = Flow(
        name="small_packets",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b"),
        rate=FlowRate(pps=10000),
        size=FlowSize(fixed=64),
        duration=FlowDuration(seconds=30)
    )
    
    # Flow 2: Large packets, medium rate  
    flow2 = Flow(
        name="large_packets",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b"),
        rate=FlowRate(pps=1000),
        size=FlowSize(fixed=1518),
        duration=FlowDuration(seconds=30)
    )
    
    # Flow 3: Variable size packets
    flow3 = Flow(
        name="variable_size",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b"),
        rate=FlowRate(pps=5000),
        size=FlowSize(increment={
            "start": 64,
            "end": 1518,
            "step": 64
        }),
        duration=FlowDuration(seconds=30)
    )
    
    flows.extend([flow1, flow2, flow3])
    return flows
```

### Bidirectional Flows
```python
def create_bidirectional_flows():
    """Create flows in both directions"""
    flows = []
    
    # A to B flow
    flow_a_to_b = Flow(
        name="a_to_b",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b"),
        rate=FlowRate(gbps=1),
        size=FlowSize(fixed=1024)
    )
    
    # B to A flow
    flow_b_to_a = Flow(
        name="b_to_a",
        tx=FlowTx(device="device_b", port="port_b"),
        rx=FlowRx(device="device_a", port="port_a"),
        rate=FlowRate(gbps=1),
        size=FlowSize(fixed=1024)
    )
    
    flows.extend([flow_a_to_b, flow_b_to_a])
    return flows
```

---

## 📊 Traffic Control

### Start and Stop Traffic
```python
def control_traffic(client):
    """Basic traffic control operations"""
    try:
        # Start all traffic
        response = client.start_traffic()
        if response.status_code == 200:
            print("✅ Traffic started successfully")
        else:
            print(f"❌ Failed to start traffic: {response.status_code}")
            return False
        
        # Monitor for 30 seconds
        time.sleep(30)
        
        # Stop all traffic
        response = client.stop_traffic()
        if response.status_code == 200:
            print("✅ Traffic stopped successfully")
        else:
            print(f"⚠️ Failed to stop traffic: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Traffic control error: {e}")
        return False
```

### Selective Flow Control
```python
def control_specific_flows(client, flow_names):
    """Start/stop specific flows"""
    
    # Start specific flows
    for flow_name in flow_names:
        try:
            response = client.start_traffic(flow_names=[flow_name])
            print(f"Started flow: {flow_name}")
        except Exception as e:
            print(f"Failed to start {flow_name}: {e}")
    
    # Monitor
    time.sleep(10)
    
    # Stop specific flows
    for flow_name in flow_names:
        try:
            response = client.stop_traffic(flow_names=[flow_name])
            print(f"Stopped flow: {flow_name}")
        except Exception as e:
            print(f"Failed to stop {flow_name}: {e}")
```

---

## 📈 Statistics Collection

### Basic Metrics Retrieval
```python
def get_basic_metrics(client):
    """Get and display basic traffic metrics"""
    try:
        response = client.get_metrics()
        if response.status_code == 200:
            metrics = response.json()
            
            print("=== Traffic Statistics ===")
            for flow_metric in metrics.get('flow_metrics', []):
                name = flow_metric.get('name', 'Unknown')
                tx_packets = flow_metric.get('frames_tx', 0)
                rx_packets = flow_metric.get('frames_rx', 0)
                tx_bytes = flow_metric.get('bytes_tx', 0)
                rx_bytes = flow_metric.get('bytes_rx', 0)
                
                loss_pct = 0
                if tx_packets > 0:
                    loss_pct = ((tx_packets - rx_packets) / tx_packets) * 100
                
                print(f"Flow: {name}")
                print(f"  TX: {tx_packets:,} packets, {tx_bytes:,} bytes")
                print(f"  RX: {rx_packets:,} packets, {rx_bytes:,} bytes") 
                print(f"  Loss: {loss_pct:.2f}%")
                print()
            
            return metrics
        else:
            print(f"Failed to get metrics: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting metrics: {e}")
        return None
```

### Real-time Monitoring
```python
def monitor_traffic_realtime(client, duration=60, interval=2):
    """Monitor traffic in real-time"""
    start_time = time.time()
    
    print("Starting real-time monitoring...")
    print("Flow Name | TX Packets | RX Packets | Loss % | TX Rate (pps)")
    print("-" * 70)
    
    previous_metrics = {}
    
    while time.time() - start_time < duration:
        try:
            response = client.get_metrics()
            if response.status_code == 200:
                metrics = response.json()
                
                for flow_metric in metrics.get('flow_metrics', []):
                    name = flow_metric.get('name', 'Unknown')
                    tx_packets = flow_metric.get('frames_tx', 0)
                    rx_packets = flow_metric.get('frames_rx', 0)
                    
                    # Calculate rate
                    tx_rate = 0
                    if name in previous_metrics:
                        prev_tx = previous_metrics[name].get('frames_tx', 0)
                        tx_rate = (tx_packets - prev_tx) / interval
                    
                    # Calculate loss
                    loss_pct = 0
                    if tx_packets > 0:
                        loss_pct = ((tx_packets - rx_packets) / tx_packets) * 100
                    
                    print(f"{name:10} | {tx_packets:10,} | {rx_packets:10,} | {loss_pct:6.2f} | {tx_rate:10.0f}")
                    
                    # Store for next iteration
                    previous_metrics[name] = flow_metric
                
                print("-" * 70)
                
        except Exception as e:
            print(f"Monitoring error: {e}")
        
        time.sleep(interval)
```

### Statistics Export
```python
import csv
import json
from datetime import datetime

def export_metrics_to_csv(metrics, filename=None):
    """Export metrics to CSV file"""
    if filename is None:
        filename = f"otg_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'flow_name', 'frames_tx', 'frames_rx', 'bytes_tx', 'bytes_rx',
            'loss_percent', 'timestamp'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        timestamp = datetime.now().isoformat()
        
        for flow_metric in metrics.get('flow_metrics', []):
            name = flow_metric.get('name', 'Unknown')
            tx_packets = flow_metric.get('frames_tx', 0)
            rx_packets = flow_metric.get('frames_rx', 0)
            tx_bytes = flow_metric.get('bytes_tx', 0)
            rx_bytes = flow_metric.get('bytes_rx', 0)
            
            loss_pct = 0
            if tx_packets > 0:
                loss_pct = ((tx_packets - rx_packets) / tx_packets) * 100
            
            writer.writerow({
                'flow_name': name,
                'frames_tx': tx_packets,
                'frames_rx': rx_packets,
                'bytes_tx': tx_bytes,
                'bytes_rx': rx_bytes,
                'loss_percent': loss_pct,
                'timestamp': timestamp
            })
    
    print(f"Metrics exported to {filename}")

def export_metrics_to_json(metrics, filename=None):
    """Export metrics to JSON file"""
    if filename is None:
        filename = f"otg_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Add timestamp to metrics
    metrics['timestamp'] = datetime.now().isoformat()
    
    with open(filename, 'w') as jsonfile:
        json.dump(metrics, jsonfile, indent=2)
    
    print(f"Metrics exported to {filename}")
```

---

## 🔄 Configuration Management

### Save and Load Configurations
```python
def save_config_to_file(config, filename):
    """Save configuration to JSON file"""
    config_dict = config.to_dict()
    
    with open(filename, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    print(f"Configuration saved to {filename}")

def load_config_from_file(filename):
    """Load configuration from JSON file"""
    with open(filename, 'r') as f:
        config_dict = json.load(f)
    
    config = Config.from_dict(config_dict)
    print(f"Configuration loaded from {filename}")
    return config

def backup_current_config(client, backup_name=None):
    """Backup current configuration"""
    if backup_name is None:
        backup_name = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        response = client.get_config()
        if response.status_code == 200:
            config = response.json()
            
            with open(backup_name, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"Configuration backed up to {backup_name}")
            return backup_name
        else:
            print(f"Failed to get configuration: {response.status_code}")
            return None
    except Exception as e:
        print(f"Backup error: {e}")
        return None
```

### Configuration Validation
```python
def validate_config(config):
    """Validate configuration before applying"""
    errors = []
    
    # Check devices exist
    if not config.devices:
        errors.append("No devices configured")
    
    # Check flows exist
    if not config.flows:
        errors.append("No flows configured")
    
    # Validate flow references
    device_names = [d.name for d in config.devices]
    port_names = []
    for device in config.devices:
        for port in device.ports:
            port_names.append(f"{device.name}.{port.name}")
    
    for flow in config.flows:
        # Check TX device/port
        tx_device = flow.tx.device
        tx_port = flow.tx.port
        if tx_device not in device_names:
            errors.append(f"Flow {flow.name}: TX device '{tx_device}' not found")
        if f"{tx_device}.{tx_port}" not in port_names:
            errors.append(f"Flow {flow.name}: TX port '{tx_port}' not found on device '{tx_device}'")
        
        # Check RX device/port
        if flow.rx:
            rx_device = flow.rx.device
            rx_port = flow.rx.port
            if rx_device not in device_names:
                errors.append(f"Flow {flow.name}: RX device '{rx_device}' not found")
            if f"{rx_device}.{rx_port}" not in port_names:
                errors.append(f"Flow {flow.name}: RX port '{rx_port}' not found on device '{rx_device}'")
    
    return errors
```

---

## 🧪 Test Automation Patterns

### Complete Test Function
```python
def run_complete_test(client, config, test_duration=30):
    """Run a complete test with error handling"""
    results = {
        'success': False,
        'error': None,
        'metrics': None,
        'duration': 0
    }
    
    start_time = time.time()
    
    try:
        # Validate configuration
        errors = validate_config(config)
        if errors:
            results['error'] = f"Configuration errors: {', '.join(errors)}"
            return results
        
        # Apply configuration
        print("Applying configuration...")
        response = client.set_config(config)
        if response.status_code != 200:
            results['error'] = f"Failed to apply configuration: {response.status_code}"
            return results
        
        # Start traffic
        print("Starting traffic...")
        response = client.start_traffic()
        if response.status_code != 200:
            results['error'] = f"Failed to start traffic: {response.status_code}"
            return results
        
        # Monitor traffic
        print(f"Monitoring traffic for {test_duration} seconds...")
        time.sleep(test_duration)
        
        # Stop traffic
        print("Stopping traffic...")
        client.stop_traffic()
        
        # Get final metrics
        print("Collecting metrics...")
        response = client.get_metrics()
        if response.status_code == 200:
            results['metrics'] = response.json()
        
        results['success'] = True
        
    except Exception as e:
        results['error'] = str(e)
        # Try to stop traffic in case of error
        try:
            client.stop_traffic()
        except:
            pass
    
    finally:
        results['duration'] = time.time() - start_time
    
    return results
```

### Parametric Testing
```python
def run_parametric_test(client, base_config, parameter_sets):
    """Run tests with different parameter sets"""
    results = []
    
    for i, params in enumerate(parameter_sets):
        print(f"\n=== Test {i+1}/{len(parameter_sets)} ===")
        print(f"Parameters: {params}")
        
        # Modify configuration based on parameters
        test_config = modify_config_with_params(base_config, params)
        
        # Run test
        result = run_complete_test(client, test_config)
        result['parameters'] = params
        result['test_number'] = i + 1
        
        results.append(result)
        
        # Brief pause between tests
        time.sleep(2)
    
    return results

def modify_config_with_params(config, params):
    """Modify configuration based on parameter set"""
    # Create a copy of the configuration
    import copy
    test_config = copy.deepcopy(config)
    
    # Modify flows based on parameters
    for flow in test_config.flows:
        if 'rate_pps' in params:
            flow.rate = FlowRate(pps=params['rate_pps'])
        if 'packet_size' in params:
            flow.size = FlowSize(fixed=params['packet_size'])
        if 'duration' in params:
            flow.duration = FlowDuration(seconds=params['duration'])
    
    return test_config
```

---

## 🔍 Debugging and Troubleshooting

### Debug Configuration
```python
def debug_config(config):
    """Debug configuration by printing detailed information"""
    print("=== Configuration Debug ===")
    
    print(f"Devices: {len(config.devices)}")
    for device in config.devices:
        print(f"  Device: {device.name}")
        print(f"    Ports: {len(device.ports)}")
        for port in device.ports:
            print(f"      Port: {port.name} -> {port.location}")
    
    print(f"\nFlows: {len(config.flows)}")
    for flow in config.flows:
        print(f"  Flow: {flow.name}")
        print(f"    TX: {flow.tx.device}.{flow.tx.port}")
        if flow.rx:
            print(f"    RX: {flow.rx.device}.{flow.rx.port}")
        if flow.rate:
            if hasattr(flow.rate, 'pps') and flow.rate.pps:
                print(f"    Rate: {flow.rate.pps} pps")
            elif hasattr(flow.rate, 'gbps') and flow.rate.gbps:
                print(f"    Rate: {flow.rate.gbps} Gbps")
        if flow.size:
            if hasattr(flow.size, 'fixed') and flow.size.fixed:
                print(f"    Size: {flow.size.fixed} bytes")
```

### Connection Testing
```python
def test_connection(client):
    """Test connection to OTG controller"""
    try:
        # Test basic connectivity
        response = client.get_version()
        if response.status_code == 200:
            version_info = response.json()
            print(f"✅ Connected to OTG controller")
            print(f"   Version: {version_info.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Connection failed: HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def health_check(client):
    """Perform comprehensive health check"""
    print("=== OTG Health Check ===")
    
    # Test connection
    if not test_connection(client):
        return False
    
    # Test configuration endpoint
    try:
        response = client.get_config()
        print(f"✅ Configuration endpoint: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Configuration endpoint error: {e}")
        return False
    
    # Test metrics endpoint
    try:
        response = client.get_metrics()
        print(f"✅ Metrics endpoint: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Metrics endpoint error: {e}")
        return False
    
    print("✅ All health checks passed")
    return True
```

---

## 🎯 Quick Reference Templates

### Minimal Working Example
```python
#!/usr/bin/env python3
"""Minimal OTG test example"""

from otg_client import OtgClient
from otg_client.models import Config, Device, Port, Flow, FlowTx, FlowRx, FlowRate, FlowSize

def main():
    # Initialize client
    client = OtgClient("http://localhost:8080")
    
    # Create configuration
    config = Config()
    
    # Add devices and ports
    device_a = Device(name="device_a", ports=[Port(name="port_a", location="eth0")])
    device_b = Device(name="device_b", ports=[Port(name="port_b", location="eth1")])
    config.devices = [device_a, device_b]
    
    # Add flow
    flow = Flow(
        name="test_flow",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b"),
        rate=FlowRate(pps=1000),
        size=FlowSize(fixed=64)
    )
    config.flows = [flow]
    
    # Run test
    client.set_config(config)
    client.start_traffic()
    time.sleep(10)
    client.stop_traffic()
    
    # Get results
    metrics = client.get_metrics()
    print(f"Test completed: {metrics.json()}")

if __name__ == "__main__":
    main()
```

### Error Handling Template
```python
def robust_test_execution(client, config):
    """Template for robust test execution with error handling"""
    try:
        # Pre-test validation
        if not health_check(client):
            raise Exception("Health check failed")
        
        # Apply configuration with validation
        errors = validate_config(config)
        if errors:
            raise Exception(f"Configuration errors: {errors}")
        
        response = client.set_config(config)
        if response.status_code != 200:
            raise Exception(f"Configuration failed: {response.status_code}")
        
        # Execute test with monitoring
        client.start_traffic()
        
        # Monitor with timeout
        start_time = time.time()
        timeout = 60
        
        while time.time() - start_time < timeout:
            metrics = client.get_metrics()
            if metrics.status_code == 200:
                # Process metrics
                pass
            time.sleep(1)
        
        # Clean stop
        client.stop_traffic()
        
        # Final metrics collection
        final_metrics = client.get_metrics()
        return final_metrics.json()
        
    except Exception as e:
        print(f"Test failed: {e}")
        # Emergency cleanup
        try:
            client.stop_traffic()
        except:
            pass
        raise
    
    finally:
        # Always cleanup
        try:
            client.clear_config()
        except:
            pass
```

---

**💡 Pro Tips:**
- Always validate configurations before applying
- Use try-catch blocks for robust error handling
- Implement proper cleanup in finally blocks
- Monitor tests in real-time for better insights
- Export results for later analysis
- Use meaningful names for flows and devices

These snippets provide a solid foundation for building your own OTG tests and automation scripts! 🌟
