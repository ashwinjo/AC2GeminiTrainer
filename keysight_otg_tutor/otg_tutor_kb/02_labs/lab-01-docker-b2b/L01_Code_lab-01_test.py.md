---
title: "Lab 1 Python Code Implementation"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Complete Python code implementation for Lab 1 Docker back-to-back testing using OTG API and snappi."
tags: ["code", "python", "implementation", "snappi", "otg-api"]
difficulty: "intermediate"
---

# Lab 01: Python Code Implementation - lab-01_test.py

## Code Overview
This document contains the complete Python implementation for Lab 01's Docker back-to-back testing scenario. The code demonstrates OTG API usage for traffic generation and measurement.

## Complete Code Implementation

```python
#!/usr/bin/env python3
"""
Lab 01: Docker Back-to-Back Testing
OTG Traffic Generation Example

This script demonstrates:
- OTG API connection and configuration
- Back-to-back traffic flow setup
- Traffic execution and statistics collection
"""

import time
import json
from otg_client import OtgClient
from otg_client.models import Config, Device, Port, Flow, FlowTx, FlowRx


def main():
    """Main function to execute the B2B test"""
    
    # Initialize OTG client
    client = OtgClient("http://localhost:8080")
    
    try:
        # Create configuration
        config = create_b2b_config()
        
        # Apply configuration
        print("Applying configuration...")
        client.set_config(config)
        
        # Start traffic
        print("Starting traffic...")
        start_traffic(client)
        
        # Monitor traffic for 30 seconds
        print("Monitoring traffic...")
        monitor_traffic(client, duration=30)
        
        # Stop traffic
        print("Stopping traffic...")
        stop_traffic(client)
        
        # Get final statistics
        print("Collecting final statistics...")
        final_stats = get_statistics(client)
        display_results(final_stats)
        
    except Exception as e:
        print(f"Error during test execution: {e}")
    finally:
        # Cleanup
        cleanup(client)


def create_b2b_config():
    """Create back-to-back configuration"""
    config = Config()
    
    # Create devices
    device_a = Device(name="device_a")
    device_b = Device(name="device_b")
    
    # Create ports
    port_a = Port(name="port_a", location="veth0")
    port_b = Port(name="port_b", location="veth1")
    
    device_a.ports = [port_a]
    device_b.ports = [port_b]
    
    # Create traffic flow
    flow = Flow(
        name="flow_a_to_b",
        tx=FlowTx(device="device_a", port="port_a"),
        rx=FlowRx(device="device_b", port="port_b")
    )
    
    # Configure flow parameters
    flow.rate.pps = 1000  # 1000 packets per second
    flow.size.fixed = 64  # 64 byte packets
    flow.duration.packets = 10000  # Send 10,000 packets
    
    # Add to configuration
    config.devices = [device_a, device_b]
    config.flows = [flow]
    
    return config


def start_traffic(client):
    """Start traffic generation"""
    response = client.start_traffic()
    if response.status_code == 200:
        print("✓ Traffic started successfully")
    else:
        raise Exception(f"Failed to start traffic: {response.status_code}")


def stop_traffic(client):
    """Stop traffic generation"""
    response = client.stop_traffic()
    if response.status_code == 200:
        print("✓ Traffic stopped successfully")
    else:
        print(f"Warning: Failed to stop traffic: {response.status_code}")


def monitor_traffic(client, duration=30):
    """Monitor traffic for specified duration"""
    start_time = time.time()
    
    while time.time() - start_time < duration:
        stats = get_statistics(client)
        display_realtime_stats(stats)
        time.sleep(2)  # Update every 2 seconds


def get_statistics(client):
    """Get current traffic statistics"""
    try:
        response = client.get_metrics()
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Warning: Failed to get statistics: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {}


def display_realtime_stats(stats):
    """Display real-time statistics"""
    if not stats:
        return
        
    print(f"\r📊 Tx: {stats.get('tx_packets', 0):,} packets | "
          f"Rx: {stats.get('rx_packets', 0):,} packets | "
          f"Loss: {calculate_loss_percentage(stats):.2f}%", end="")


def display_results(stats):
    """Display final test results"""
    print("\n" + "="*50)
    print("FINAL TEST RESULTS")
    print("="*50)
    
    if not stats:
        print("❌ No statistics available")
        return
    
    tx_packets = stats.get('tx_packets', 0)
    rx_packets = stats.get('rx_packets', 0)
    loss_pct = calculate_loss_percentage(stats)
    
    print(f"📤 Transmitted Packets: {tx_packets:,}")
    print(f"📥 Received Packets:    {rx_packets:,}")
    print(f"📊 Packet Loss:        {loss_pct:.2f}%")
    
    if loss_pct == 0:
        print("✅ Test PASSED - No packet loss detected")
    elif loss_pct < 0.01:
        print("⚠️  Test WARNING - Minimal packet loss detected")
    else:
        print("❌ Test FAILED - Significant packet loss detected")


def calculate_loss_percentage(stats):
    """Calculate packet loss percentage"""
    tx = stats.get('tx_packets', 0)
    rx = stats.get('rx_packets', 0)
    
    if tx == 0:
        return 0.0
    
    return ((tx - rx) / tx) * 100


def cleanup(client):
    """Cleanup resources"""
    try:
        print("\nCleaning up...")
        client.stop_traffic()
        client.clear_config()
        print("✓ Cleanup completed")
    except Exception as e:
        print(f"Warning during cleanup: {e}")


if __name__ == "__main__":
    main()
```

## Code Explanation

### Key Components

1. **Client Initialization**: Connects to the OTG controller
2. **Configuration Creation**: Defines devices, ports, and traffic flows
3. **Traffic Control**: Start/stop traffic generation
4. **Statistics Monitoring**: Real-time and final result collection
5. **Error Handling**: Robust error management and cleanup

### Important Functions

- `create_b2b_config()`: Sets up the back-to-back test configuration
- `monitor_traffic()`: Provides real-time traffic monitoring
- `display_results()`: Shows formatted test results
- `cleanup()`: Ensures proper resource cleanup

### Running the Code

1. Ensure Docker containers are running
2. Install required Python packages:
   ```bash
   pip install otg-client
   ```
3. Execute the script:
   ```bash
   python lab-01_test.py
   ```

## Expected Output
```
Applying configuration...
✓ Configuration applied successfully
Starting traffic...
✓ Traffic started successfully
Monitoring traffic...
📊 Tx: 10,000 packets | Rx: 10,000 packets | Loss: 0.00%
Stopping traffic...
✓ Traffic stopped successfully
Collecting final statistics...

==================================================
FINAL TEST RESULTS
==================================================
📤 Transmitted Packets: 10,000
📥 Received Packets:    10,000
📊 Packet Loss:        0.00%
✅ Test PASSED - No packet loss detected

Cleaning up...
✓ Cleanup completed
```

## Customization Options

- Modify `flow.rate.pps` to change traffic rate
- Adjust `flow.size.fixed` for different packet sizes
- Change `flow.duration.packets` for longer/shorter tests
- Add multiple flows for complex scenarios

## Troubleshooting

If you encounter issues, refer to:
- L01_Troubleshooting.md for specific error solutions
- General troubleshooting section for common Docker/Python issues
