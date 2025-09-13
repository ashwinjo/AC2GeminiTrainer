---
title: "Lab 4 Metrics Collection and Analysis"
lab_id: "lab-04-ixiac-containerlab-dut-convergence"
category: "lab"
objective: "Comprehensive metrics collection, BGP convergence analysis, and DUT recovery validation for Lab 4."
tags: ["metrics", "analysis", "bgp", "convergence", "recovery-time", "ixia-c-one"]
difficulty: "advanced"
---

# Lab 04: Metrics Collection and BGP Convergence Analysis

## 🎯 Overview
Lab 04 focuses on **advanced BGP convergence metrics** with emphasis on **network recovery time analysis** and **path selection validation**. Unlike previous labs that focused on basic flow metrics or egress tracking, Lab 04 provides:
- **BGP convergence time measurement** for network resilience validation
- **Path selection analysis** during failure and recovery scenarios
- **Comparative analysis** between hard failures (link down) and soft failures (route withdrawal)
- **Route scale impact assessment** on convergence performance
- **Real-time monitoring** of BGP state changes and traffic recovery

## 📊 Metrics Collection Methods

### Method 1: Real-time BGP Convergence Monitoring

Monitor BGP convergence metrics during test execution using Ixia-C-One:

```bash
# Monitor BGP session status during test
curl -k -X POST https://clab-lab-04-ixia-c-one:8443/api/v1/results/metrics \
  -H "Content-Type: application/json" \
  -d '{"choice": "bgpv4"}'

# Monitor flow metrics during convergence events
curl -k -X POST https://clab-lab-04-ixia-c-one:8443/api/v1/results/metrics \
  -H "Content-Type: application/json" \
  -d '{"choice": "flow"}'
```

**🧠 Understanding BGP convergence output:**
```json
{
  "bgpv4_metrics": [
    {
      "name": "bgp_peer_eth2",
      "session_state": "established",
      "routes_advertised": 100,
      "routes_received": 100,
      "session_flaps": 1
    },
    {
      "name": "bgp_peer_eth3", 
      "session_state": "established",
      "routes_advertised": 100,
      "routes_received": 100,
      "session_flaps": 0
    }
  ]
}
```

**Key BGP metrics:**
- **Session State**: Current BGP session status (idle, active, established)
- **Routes Advertised/Received**: Route exchange counters
- **Session Flaps**: Number of session state changes (indicates failure events)
- **Convergence Time**: Time for session recovery after failure

### Method 2: DUT-Side BGP Metrics Collection

Collect detailed BGP metrics directly from the Nokia SRL DUT:

```bash
# Connect to Nokia SRL for detailed BGP analysis
ssh admin@clab-lab-04-srl

# Monitor BGP neighbor status
show network-instance default protocols bgp neighbor

# Check route table changes
show network-instance default protocols bgp routes ipv4 summary

# Monitor BGP session statistics
show network-instance default protocols bgp neighbor statistics

# Check route reflector status
show network-instance default protocols bgp route-reflector
```

**🧠 Key DUT metrics to analyze:**
```bash
# BGP neighbor state transitions
Neighbor: 192.168.22.2 (eth2)
State: Established → Idle → Established
Uptime: 00:05:23
Routes Received: 100 → 0 → 100

# Route selection changes
Best Path: 192.168.22.2 → 192.168.33.2 → 192.168.22.2
Next Hop: eth2 → eth3 → eth2
```

### Method 3: Traffic Flow Analysis During Convergence

Monitor traffic behavior during convergence events:

```python
def monitor_traffic_during_convergence(api, duration_seconds=60):
    """Monitor traffic patterns during BGP convergence"""
    
    convergence_data = []
    start_time = time.time()
    
    while time.time() - start_time < duration_seconds:
        # Collect current flow metrics
        req = api.metrics_request()
        req.flow.flow_names = []
        metrics = api.get_metrics(req).flow_metrics
        
        timestamp = time.time() - start_time
        for m in metrics:
            convergence_data.append({
                'timestamp': timestamp,
                'flow_name': m.name,
                'frames_tx': m.frames_tx,
                'frames_rx': m.frames_rx,
                'frames_tx_rate': m.frames_tx_rate,
                'frames_rx_rate': m.frames_rx_rate,
                'packet_loss': m.frames_tx - m.frames_rx
            })
        
        time.sleep(0.1)  # Sample every 100ms for high resolution
    
    return convergence_data
```

### Method 4: Port-Level Statistics Analysis

Analyze port-level statistics to understand traffic path changes:

```bash
# Monitor port statistics during convergence
curl -k -X POST https://clab-lab-04-ixia-c-one:8443/api/v1/results/metrics \
  -H "Content-Type: application/json" \
  -d '{"choice": "port", "port": {"port_names": ["eth1", "eth2", "eth3"]}}'
```

**Port metrics interpretation:**
- **eth1**: Traffic ingress/egress (should remain constant)
- **eth2**: BGP peer 1 traffic (decreases during eth2 failure)
- **eth3**: BGP peer 2 traffic (increases during eth2 failure)

## 🔍 BGP Convergence Analysis Techniques

### **1. Convergence Time Calculation**

Calculate precise convergence time using packet loss analysis:

```python
def calculate_convergence_time(flow_metrics_history, tx_rate_pps):
    """
    Calculate BGP convergence time based on packet loss
    
    Args:
        flow_metrics_history: List of flow metrics over time
        tx_rate_pps: Transmission rate in packets per second
    
    Returns:
        Dict with convergence analysis
    """
    
    # Find convergence event by detecting packet loss spike
    max_loss = 0
    convergence_start = None
    convergence_end = None
    
    for i, metrics in enumerate(flow_metrics_history):
        current_loss = metrics['frames_tx'] - metrics['frames_rx']
        
        # Detect start of convergence (packet loss begins)
        if current_loss > 0 and convergence_start is None:
            convergence_start = metrics['timestamp']
        
        # Track maximum loss during convergence
        if current_loss > max_loss:
            max_loss = current_loss
        
        # Detect end of convergence (traffic recovery)
        if current_loss == 0 and convergence_start is not None and convergence_end is None:
            convergence_end = metrics['timestamp']
            break
    
    # Calculate convergence time
    if convergence_start and convergence_end:
        convergence_time = convergence_end - convergence_start
    else:
        # Alternative calculation using packet loss
        convergence_time = max_loss / tx_rate_pps if tx_rate_pps > 0 else 0
    
    return {
        'convergence_time_seconds': convergence_time,
        'packets_lost': max_loss,
        'convergence_start': convergence_start,
        'convergence_end': convergence_end,
        'recovery_method': 'packet_loss_analysis'
    }
```

### **2. Path Selection Analysis**

Analyze BGP path selection changes during convergence:

```python
def analyze_path_selection(bgp_metrics_history):
    """Analyze BGP path selection changes during convergence"""
    
    path_changes = []
    previous_best_path = None
    
    for metrics in bgp_metrics_history:
        # Determine current best path based on session states
        current_best_path = None
        
        for peer in metrics['bgp_peers']:
            if peer['session_state'] == 'established' and peer['routes_received'] > 0:
                # Simple best path logic (in reality, considers Local Preference, MED, etc.)
                if current_best_path is None or peer['local_preference'] > current_best_path['local_preference']:
                    current_best_path = peer
        
        # Detect path changes
        if previous_best_path and current_best_path:
            if previous_best_path['peer_address'] != current_best_path['peer_address']:
                path_changes.append({
                    'timestamp': metrics['timestamp'],
                    'from_peer': previous_best_path['peer_address'],
                    'to_peer': current_best_path['peer_address'],
                    'reason': 'bgp_convergence'
                })
        
        previous_best_path = current_best_path
    
    return path_changes
```

### **3. Failure Type Classification**

Classify and compare different failure scenarios:

```python
def classify_failure_type(convergence_metrics):
    """Classify failure type based on convergence characteristics"""
    
    convergence_time = convergence_metrics['convergence_time_seconds']
    packets_lost = convergence_metrics['packets_lost']
    
    # Classification based on convergence characteristics
    if convergence_time > 2.0:
        failure_type = "hard_failure"
        description = "Link down or physical failure (longer detection time)"
    elif convergence_time < 0.5:
        failure_type = "soft_failure"
        description = "Route withdrawal or BGP update (fast processing)"
    else:
        failure_type = "moderate_failure"
        description = "BGP session failure or timeout"
    
    return {
        'failure_type': failure_type,
        'description': description,
        'convergence_time': convergence_time,
        'severity': 'high' if packets_lost > 100 else 'medium' if packets_lost > 10 else 'low'
    }
```

## 📈 Performance Metrics and Benchmarking

### **BGP Convergence Performance Analysis**

Measure BGP convergence performance under different conditions:

```python
def analyze_convergence_performance(test_results):
    """Comprehensive BGP convergence performance analysis"""
    
    performance_metrics = {
        'baseline_performance': {},
        'convergence_impact': {},
        'recovery_analysis': {},
        'scalability_assessment': {}
    }
    
    # Baseline performance (before convergence event)
    baseline = test_results['baseline_phase']
    performance_metrics['baseline_performance'] = {
        'avg_throughput_pps': calculate_average_throughput(baseline),
        'packet_loss_rate': calculate_packet_loss_rate(baseline),
        'latency_ms': calculate_average_latency(baseline),
        'bgp_sessions_stable': count_stable_bgp_sessions(baseline)
    }
    
    # Convergence impact analysis
    convergence = test_results['convergence_phase']
    performance_metrics['convergence_impact'] = {
        'max_packet_loss': calculate_max_packet_loss(convergence),
        'throughput_degradation': calculate_throughput_impact(baseline, convergence),
        'convergence_duration': calculate_convergence_duration(convergence),
        'affected_flows': count_affected_flows(convergence)
    }
    
    # Recovery analysis
    recovery = test_results['recovery_phase']
    performance_metrics['recovery_analysis'] = {
        'recovery_time': calculate_recovery_time(convergence, recovery),
        'performance_restoration': calculate_performance_restoration(baseline, recovery),
        'stability_after_recovery': assess_post_recovery_stability(recovery)
    }
    
    return performance_metrics
```

### **Route Scale Impact Assessment**

Analyze the impact of route count on convergence time:

```python
def analyze_route_scale_impact(test_results_by_route_count):
    """Analyze how route count affects convergence performance"""
    
    scale_analysis = {
        'route_counts': [],
        'convergence_times': [],
        'scaling_factor': None,
        'recommendations': []
    }
    
    for route_count, results in test_results_by_route_count.items():
        scale_analysis['route_counts'].append(route_count)
        scale_analysis['convergence_times'].append(results['convergence_time'])
    
    # Calculate scaling factor (linear regression)
    if len(scale_analysis['route_counts']) > 1:
        scaling_factor = calculate_scaling_factor(
            scale_analysis['route_counts'],
            scale_analysis['convergence_times']
        )
        scale_analysis['scaling_factor'] = scaling_factor
        
        # Generate recommendations
        if scaling_factor > 0.1:  # More than 100ms per 1000 routes
            scale_analysis['recommendations'].append(
                "Consider route aggregation to reduce convergence time"
            )
        if max(scale_analysis['convergence_times']) > 5.0:
            scale_analysis['recommendations'].append(
                "Convergence time exceeds typical SLA requirements"
            )
    
    return scale_analysis
```

## 🔄 Real-time Monitoring Techniques

### **Continuous BGP State Monitoring**

Set up continuous monitoring of BGP states during convergence testing:

```python
def setup_bgp_monitoring(api, dut_ssh_connection, monitoring_duration=300):
    """Set up comprehensive BGP monitoring during convergence tests"""
    
    monitoring_data = {
        'otg_metrics': [],
        'dut_metrics': [],
        'convergence_events': []
    }
    
    def otg_monitoring_loop():
        """Monitor OTG BGP metrics"""
        while monitoring_active:
            try:
                # Collect OTG BGP metrics
                req = api.metrics_request()
                req.bgpv4.peer_names = []
                bgp_metrics = api.get_metrics(req).bgpv4_metrics
                
                monitoring_data['otg_metrics'].append({
                    'timestamp': time.time(),
                    'bgp_peers': [
                        {
                            'name': peer.name,
                            'session_state': peer.session_state,
                            'routes_advertised': peer.routes_advertised,
                            'routes_received': peer.routes_received
                        } for peer in bgp_metrics
                    ]
                })
                
                time.sleep(1)  # Sample every second
            except Exception as e:
                logging.error(f"OTG monitoring error: {e}")
    
    def dut_monitoring_loop():
        """Monitor DUT BGP state"""
        while monitoring_active:
            try:
                # Execute BGP status command on DUT
                result = dut_ssh_connection.execute_command(
                    "show network-instance default protocols bgp neighbor brief"
                )
                
                monitoring_data['dut_metrics'].append({
                    'timestamp': time.time(),
                    'bgp_output': result.stdout,
                    'parsed_neighbors': parse_bgp_neighbor_output(result.stdout)
                })
                
                time.sleep(2)  # Sample every 2 seconds
            except Exception as e:
                logging.error(f"DUT monitoring error: {e}")
    
    # Start monitoring threads
    monitoring_active = True
    otg_thread = threading.Thread(target=otg_monitoring_loop, daemon=True)
    dut_thread = threading.Thread(target=dut_monitoring_loop, daemon=True)
    
    otg_thread.start()
    dut_thread.start()
    
    return monitoring_data
```

## 🎯 Metrics Validation and Success Criteria

### **Automated BGP Convergence Validation**

Create automated validation for BGP convergence test success:

```python
def validate_bgp_convergence_test(test_results, expected_criteria):
    """Automated validation of BGP convergence test results"""
    
    validation_results = {
        "bgp_session_establishment": False,
        "route_advertisement": False,
        "traffic_forwarding": False,
        "convergence_performance": False,
        "path_selection": False,
        "overall_success": False
    }
    
    # Validate BGP session establishment
    bgp_sessions = test_results.get('bgp_sessions', [])
    established_sessions = [s for s in bgp_sessions if s['state'] == 'established']
    validation_results["bgp_session_establishment"] = len(established_sessions) >= 2
    
    # Validate route advertisement
    for session in established_sessions:
        if session['routes_advertised'] > 0 and session['routes_received'] > 0:
            validation_results["route_advertisement"] = True
            break
    
    # Validate traffic forwarding
    flow_metrics = test_results.get('flow_metrics', {})
    if flow_metrics.get('frames_tx', 0) > 0 and flow_metrics.get('frames_rx', 0) > 0:
        packet_loss_rate = (flow_metrics['frames_tx'] - flow_metrics['frames_rx']) / flow_metrics['frames_tx']
        validation_results["traffic_forwarding"] = packet_loss_rate < 0.01  # Less than 1% loss
    
    # Validate convergence performance
    convergence_time = test_results.get('convergence_time', float('inf'))
    validation_results["convergence_performance"] = convergence_time < expected_criteria.get('max_convergence_time', 10.0)
    
    # Validate path selection behavior
    path_changes = test_results.get('path_changes', [])
    validation_results["path_selection"] = len(path_changes) > 0  # At least one path change occurred
    
    # Overall success
    validation_results["overall_success"] = all([
        validation_results["bgp_session_establishment"],
        validation_results["route_advertisement"],
        validation_results["traffic_forwarding"],
        validation_results["convergence_performance"]
    ])
    
    return validation_results
```

## 📋 Metrics Collection Best Practices

### **1. Comprehensive Data Collection**
- Collect metrics from both OTG and DUT perspectives
- Monitor at high frequency during convergence events (100ms intervals)
- Capture baseline performance before convergence testing
- Record environmental factors (route count, BGP timers, etc.)

### **2. Convergence Event Correlation**
- Synchronize timestamps between OTG and DUT metrics
- Correlate BGP session state changes with traffic impacts
- Track cause-and-effect relationships between failures and recovery
- Document manual intervention points for repeatability

### **3. Performance Benchmarking**
- Establish baseline performance metrics for comparison
- Test multiple failure scenarios for comprehensive analysis
- Vary route counts to understand scalability impact
- Compare results across different DUT configurations

### **4. Automated Analysis**
- Implement automated convergence time calculation
- Set up threshold-based alerting for performance degradation
- Generate comparative reports across test runs
- Create trend analysis for long-term performance tracking

---

**🎯 Success Criteria for Lab 04:**
- ✅ iBGP sessions established and stable (< 1% session flaps)
- ✅ Route advertisement successful with proper BGP attributes
- ✅ Traffic forwarding with < 1% packet loss during steady state
- ✅ Convergence time < 5 seconds for link down events
- ✅ Convergence time < 1 second for route withdrawal events
- ✅ Path selection follows BGP best path algorithm correctly
- ✅ Traffic recovery to baseline performance levels post-convergence
- ✅ Scalability demonstrated with varying route counts

**Next Step**: Proceed to L04_Challenge.md to explore advanced BGP convergence testing scenarios and optimization techniques.
