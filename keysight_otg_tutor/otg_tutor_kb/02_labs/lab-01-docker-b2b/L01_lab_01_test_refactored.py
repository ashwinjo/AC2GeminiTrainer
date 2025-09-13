"""
Refactored Lab 01 Test - Breaking down the monolithic Traffic_Test function
into smaller, more understandable functions for first-time users.

This script demonstrates the OTG (Open Traffic Generator) API workflow:
1. API Connection & Configuration Setup
2. Port Configuration  
3. Flow Configuration
4. Packet Header Configuration
5. Traffic Execution
6. Statistics Verification

Each function maps to specific OTG API schema components.
"""

from time import time
from datetime import datetime
from snappi import snappi


def create_api_connection():
    """
    Step 1: Create API Connection
    
    OTG API Schema Mapping:
    - Uses snappi.api() to create connection to traffic generator controller
    - Maps to the root API object in OTG schema
    
    Returns:
        api: Connected API instance
    """
    print("")
    print("%s Creating API connection to controller..." % datetime.now())
    
    # Configure a new API instance where the location points to controller
    # Ixia-C:       location = "https://<tgen-ip>:<port>"
    # IxNetwork:    location = "https://<tgen-ip>:<port>", ext="ixnetwork"  
    # TRex:         location =         "<tgen-ip>:<port>", ext="trex"
    
    api = snappi.api(location="https://127.0.0.1:8443", verify=False)
    print("%s API connection established successfully" % datetime.now())
    
    return api


def create_base_configuration(api):
    """
    Step 2: Create Base Configuration Object
    
    OTG API Schema Mapping:
    - api.config() creates the root Configuration object
    - This is the top-level container for all test configuration
    - Maps to openapi-generator Config schema
    
    Args:
        api: Connected API instance
        
    Returns:
        configuration: Empty configuration object ready to be populated
    """
    print("%s Creating base configuration object..." % datetime.now())
    
    # Create an empty configuration to be pushed to controller
    # This maps to the Configuration schema in OTG API
    configuration = api.config()
    
    print("%s Base configuration object created" % datetime.now())
    return configuration


def configure_ports(configuration):
    """
    Step 3: Configure Test Ports
    
    OTG API Schema Mapping:
    - configuration.ports maps to Config.ports[] array
    - Each port() call creates a Port object with name and location
    - Port.location specifies the physical/virtual port endpoint
    
    Args:
        configuration: Base configuration object
        
    Returns:
        tuple: (port1, port2) - Configured port objects
    """
    print("%s Configuring test ports..." % datetime.now())
    
    # Configure two ports where the location points to the port location:
    # Ixia-C:       port.location = "localhost:5555"
    # IxNetwork:    port.location = "<chassisip>;card;port"
    # TRex:         port.location = "localhost"
    
    port1, port2 = (
        configuration.ports
        .port(name="Port-1", location="127.0.0.1:5551")
        .port(name="Port-2", location="127.0.0.1:5552")
    )
    
    print("%s Ports configured: %s, %s" % (datetime.now(), port1.name, port2.name))
    return port1, port2


def configure_traffic_flows(configuration, port1, port2):
    """
    Step 4: Configure Traffic Flows
    
    OTG API Schema Mapping:
    - configuration.flows maps to Config.flows[] array
    - Each flow() call creates a Flow object
    - Flow.metrics.enable maps to Flow.metrics boolean
    - Flow.tx_rx.port maps to FlowTxRx.port for defining endpoints
    
    Args:
        configuration: Base configuration object
        port1: First port object
        port2: Second port object
        
    Returns:
        tuple: (flow1, flow2) - Configured flow objects
    """
    print("%s Configuring traffic flows..." % datetime.now())
    
    # Configure two traffic flows - bidirectional traffic
    flow1, flow2 = (
        configuration.flows
        .flow(name="Flow #1 - Port 1 > Port 2")
        .flow(name="Flow #2 - Port 2 > Port 1")
    )
    
    # Enable flow metrics for statistics collection
    # Maps to Flow.metrics.enable in OTG schema
    flow1.metrics.enable = True
    flow2.metrics.enable = True
    
    # Configure source and destination ports for each traffic flow
    # Maps to Flow.tx_rx.port in OTG schema
    flow1.tx_rx.port.tx_name = port1.name
    flow1.tx_rx.port.rx_names = [port2.name]
    flow2.tx_rx.port.tx_name = port2.name
    flow2.tx_rx.port.rx_names = [port1.name]
    
    print("%s Traffic flows configured: %s, %s" % (datetime.now(), flow1.name, flow2.name))
    return flow1, flow2


def configure_flow_properties(configuration, flow1, flow2):
    """
    Step 5: Configure Flow Properties (Size, Rate, Duration)
    
    OTG API Schema Mapping:
    - Flow.size.fixed maps to FlowSize.fixed (packet size in bytes)
    - Flow.duration.fixed_packets.packets maps to FlowDurationFixedPackets.packets
    - Flow.rate.pps maps to FlowRate.pps (packets per second)
    
    Args:
        configuration: Base configuration object
        flow1: First flow object
        flow2: Second flow object
    """
    print("%s Configuring flow properties (size, rate, duration)..." % datetime.now())
    
    # Configure packet size for both flows
    # Maps to Flow.size.fixed in OTG schema
    flow1.size.fixed = 128  # 128 bytes
    flow2.size.fixed = 128  # 128 bytes
    
    # Configure rate and duration for all flows
    for f in configuration.flows:
        # Send 2000 packets per test and then stop
        # Maps to Flow.duration.fixed_packets.packets
        f.duration.fixed_packets.packets = 2000
        
        # Send 100 packets per second  
        # Maps to Flow.rate.pps
        f.rate.pps = 100
    
    print("%s Flow properties configured: 128B packets, 100pps, 2000 packets total" % datetime.now())


def configure_packet_headers(flow1, flow2):
    """
    Step 6: Configure Packet Headers (Ethernet, IPv4, UDP)
    
    OTG API Schema Mapping:
    - Flow.packet[] maps to FlowHeader array
    - flow.packet.add().ethernet maps to FlowEthernet header
    - flow.packet.add().ipv4 maps to FlowIpv4 header  
    - flow.packet.add().udp maps to FlowUdp header
    - Header fields map to respective protocol field schemas
    
    Args:
        flow1: First flow object
        flow2: Second flow object
    """
    print("%s Configuring packet headers (Ethernet, IPv4, UDP)..." % datetime.now())
    
    # Configure packet headers for Flow 1
    # Each add() creates a new header in the packet stack
    eth1 = flow1.packet.add().ethernet  # Maps to FlowEthernet
    ip1 = flow1.packet.add().ipv4       # Maps to FlowIpv4
    udp1 = flow1.packet.add().udp       # Maps to FlowUdp
    
    # Configure packet headers for Flow 2 (alternative syntax)
    flow2.packet.ethernet().ipv4().udp()
    eth2, ip2, udp2 = flow2.packet[0], flow2.packet[1], flow2.packet[2]
    
    # Configure Ethernet MAC addresses
    # Maps to FlowEthernet.src/dst fields
    eth1.src.value, eth1.dst.value = "00:AA:00:00:01:00", "00:AA:00:00:02:00"
    eth2.src.value, eth2.dst.value = "00:AA:00:00:02:00", "00:AA:00:00:01:00"
    
    # Configure IPv4 addresses  
    # Maps to FlowIpv4.src/dst fields
    ip1.src.value, ip1.dst.value = "10.0.0.1", "10.0.0.2"
    ip2.src.value, ip2.dst.value = "10.0.0.2", "10.0.0.1"
    
    print("%s Packet headers configured with MAC and IP addresses" % datetime.now())
    return eth1, ip1, udp1, eth2, ip2, udp2


def configure_udp_port_patterns(udp1, udp2):
    """
    Step 7: Configure UDP Port Patterns
    
    OTG API Schema Mapping:
    - FlowUdp.src_port.increment maps to FlowUdpSrcPort.increment
    - FlowUdpSrcPortIncrement has start, step, count fields
    - FlowUdp.dst_port.values maps to FlowUdpDstPort.values array
    
    Args:
        udp1: UDP header object for flow 1
        udp2: UDP header object for flow 2
    """
    print("%s Configuring UDP port patterns..." % datetime.now())
    
    # Configure UDP Source Ports as incrementing pattern
    # Maps to FlowUdpSrcPort.increment in OTG schema
    udp1.src_port.increment.start = 5100  # Starting port
    udp1.src_port.increment.step = 2      # Increment by 2
    udp1.src_port.increment.count = 10    # 10 different values
    
    udp2.src_port.increment.start = 5200  # Starting port  
    udp2.src_port.increment.step = 4      # Increment by 4
    udp2.src_port.increment.count = 10    # 10 different values
    
    # Configure UDP Destination Ports as value list
    # Maps to FlowUdpDstPort.values array in OTG schema
    udp1.dst_port.values = [6100, 6125, 6150, 6170, 6190]
    udp2.dst_port.values = [6200, 6222, 6244, 6266, 6288]
    
    print("%s UDP port patterns configured with increment and value list patterns" % datetime.now())


def apply_configuration(api, configuration):
    """
    Step 8: Apply Configuration to Traffic Generator
    
    OTG API Schema Mapping:
    - api.set_config() pushes the complete Config object to the traffic generator
    - This validates and applies all configuration settings
    
    Args:
        api: Connected API instance
        configuration: Complete configuration object
    """
    print("%s Applying configuration to traffic generator..." % datetime.now())
    
    # Push configuration to the traffic generator controller
    # This validates the entire configuration against OTG schema
    api.set_config(configuration)
    
    print("%s Configuration applied successfully" % datetime.now())


def start_traffic(api):
    """
    Step 9: Start Traffic Transmission
    
    OTG API Schema Mapping:
    - api.control_state() creates ControlState object
    - ControlState.choice = TRAFFIC maps to traffic control
    - ControlState.traffic.choice = FLOW_TRANSMIT maps to flow control
    - ControlState.traffic.flow_transmit.state = START initiates traffic
    
    Args:
        api: Connected API instance
    """
    print("%s Starting traffic transmission..." % datetime.now())
    
    # Create control state object for traffic control
    # Maps to ControlState schema in OTG API
    cs = api.control_state()
    cs.choice = cs.TRAFFIC                                    # Control traffic
    cs.traffic.choice = cs.traffic.FLOW_TRANSMIT             # Control flows
    cs.traffic.flow_transmit.state = cs.traffic.flow_transmit.START  # Start transmission
    
    # Apply the control state to start traffic
    api.set_control_state(cs)
    
    print("%s Traffic transmission started" % datetime.now())


def verify_traffic_statistics(api, configuration):
    """
    Step 10: Verify Traffic Statistics
    
    OTG API Schema Mapping:
    - api.metrics_request() creates MetricsRequest object
    - MetricsRequest.port.port_names maps to port filter
    - MetricsRequest.port.column_names maps to metric filter
    - api.get_metrics() returns MetricsResponse with actual statistics
    
    Args:
        api: Connected API instance
        configuration: Configuration object for expected values
        
    Returns:
        bool: True if test passes, False otherwise
    """
    print("%s Verifying traffic statistics..." % datetime.now())
    print("====================================================================================")
    print("\t\t\t\t\t\tExpected\tTx\t\tRx")
    
    # Use wait_for utility to poll statistics until test completes or times out
    test_passed = wait_for(lambda: verify_statistics(api, configuration))
    
    print("====================================================================================")
    return test_passed


def verify_statistics(api, configuration):
    """
    Statistics Verification Helper Function
    
    OTG API Schema Mapping:
    - MetricsRequest.port maps to PortMetricsRequest
    - PortMetricsRequest.port_names filters by port names
    - PortMetricsRequest.column_names filters by specific metrics
    - MetricsResponse.port_metrics contains PortMetric objects
    - PortMetric.frames_tx/frames_rx contain actual counters
    
    Args:
        api: Connected API instance  
        configuration: Configuration object for expected values
        
    Returns:
        bool: True if statistics match expected values
    """
    # Create a port statistics request and filter based on port names
    # Maps to MetricsRequest.port in OTG schema
    statistics = api.metrics_request()
    statistics.port.port_names = [p.name for p in configuration.ports]
    
    # Create a filter to include only sent and received packet statistics
    # Maps to PortMetricsRequest.column_names
    statistics.port.column_names = [statistics.port.FRAMES_TX, statistics.port.FRAMES_RX]
    
    # Collect port statistics from traffic generator
    # Returns MetricsResponse with PortMetric objects
    results = api.get_metrics(statistics)
    
    # Calculate total frames sent and received across all ports
    total_frames_tx = sum([m.frames_tx for m in results.port_metrics])
    total_frames_rx = sum([m.frames_rx for m in results.port_metrics])
    total_expected = sum([f.duration.fixed_packets.packets for f in configuration.flows])
    
    print("%s TOTAL  \t\t%d\t\t%d\t\t%d" % (datetime.now(), total_expected, total_frames_tx, total_frames_rx))
    
    # Verify that transmitted packets match expected and received >= expected
    return total_expected == total_frames_tx and total_frames_rx >= total_expected


def wait_for(func, timeout=30, interval=1):
    """
    Utility function to poll a condition until it becomes true or times out.
    
    Args:
        func: Function to call repeatedly (should return bool)
        timeout: Maximum time to wait in seconds
        interval: Time between polls in seconds
        
    Returns:
        bool: True if condition met, False if timeout occurred
    """
    import time
    
    start = time.time()
    
    while time.time() - start <= timeout:
        if func():
            return True
        time.sleep(interval)
    
    return False


def traffic_test_refactored():
    """
    Main test function - orchestrates the complete OTG test workflow.
    
    This refactored version breaks down the monolithic Traffic_Test function
    into logical steps that map clearly to OTG API schema components.
    
    Test Overview:
    - Send 2000 packets back and forth between two ports at 100 packets per second
    - Validate that total packets sent and received match expected values
    """
    starttime = datetime.now()
    print("=" * 80)
    print("Starting OTG Traffic Test - Refactored Version")
    print("=" * 80)
    
    try:
        # Step 1: Create API connection
        api = create_api_connection()
        
        # Step 2: Create base configuration
        configuration = create_base_configuration(api)
        
        # Step 3: Configure ports
        port1, port2 = configure_ports(configuration)
        
        # Step 4: Configure traffic flows
        flow1, flow2 = configure_traffic_flows(configuration, port1, port2)
        
        # Step 5: Configure flow properties
        configure_flow_properties(configuration, flow1, flow2)
        
        # Step 6: Configure packet headers
        eth1, ip1, udp1, eth2, ip2, udp2 = configure_packet_headers(flow1, flow2)
        
        # Step 7: Configure UDP port patterns
        configure_udp_port_patterns(udp1, udp2)
        
        # Step 8: Apply configuration
        apply_configuration(api, configuration)
        
        # Step 9: Start traffic
        start_traffic(api)
        
        # Step 10: Verify statistics
        if verify_traffic_statistics(api, configuration):
            print("%s Test PASSED in %s" % (datetime.now(), datetime.now() - starttime))
            print("=" * 80)
            return True
        else:
            print("%s Test FAILED in %s" % (datetime.now(), datetime.now() - starttime))
            print("=" * 80)
            return False
            
    except Exception as e:
        print("%s Test FAILED with exception: %s" % (datetime.now(), str(e)))
        print("Total test time: %s" % (datetime.now() - starttime))
        print("=" * 80)
        return False


if __name__ == "__main__":
    traffic_test_refactored()
