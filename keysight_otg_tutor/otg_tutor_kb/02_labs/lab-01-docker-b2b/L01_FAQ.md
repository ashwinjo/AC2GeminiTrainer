# Lab 01: Frequently Asked Questions (FAQ)

## General Questions

### Q1: What is back-to-back (B2B) testing?
**A:** Back-to-back testing is a network testing methodology where two devices are directly connected to each other without any intermediate network equipment. This creates a controlled environment for testing traffic generation, protocol behavior, and performance metrics.

### Q2: Why use Docker for OTG testing?
**A:** Docker provides several advantages:
- **Isolation**: Each container runs independently
- **Reproducibility**: Consistent environment across different machines
- **Scalability**: Easy to spin up multiple test instances
- **Resource Efficiency**: Lightweight compared to full VMs
- **Version Control**: Container images can be versioned and shared

### Q3: What's the difference between OTG and traditional traffic generators?
**A:** OTG (Open Traffic Generator) is an open-source, API-driven approach that:
- Uses standardized APIs for configuration
- Supports containerized deployments
- Provides vendor-neutral interfaces
- Enables programmatic control and automation

## Technical Questions

### Q4: How do I know if my Docker setup is correct?
**A:** Verify these components:
```bash
# Check Docker is running
docker --version
docker ps

# Verify network connectivity
docker network ls
docker network inspect otg-test-net

# Check container logs
docker logs otg-controller
```

### Q5: What ports does the OTG controller use?
**A:** The default OTG controller uses:
- **Port 8080**: HTTP API endpoint
- **Port 8443**: HTTPS API endpoint (if SSL enabled)
- **Port 9090**: gNMI interface (if enabled)

### Q6: How can I modify the traffic parameters?
**A:** Key parameters you can adjust:
```python
# Traffic rate
flow.rate.pps = 1000        # Packets per second
flow.rate.bps = 1000000     # Bits per second

# Packet size
flow.size.fixed = 64        # Fixed size
flow.size.increment = {...} # Incrementing size

# Duration
flow.duration.packets = 10000  # Number of packets
flow.duration.seconds = 30     # Time duration
```

### Q7: Why am I seeing packet loss in a B2B setup?
**A:** Common causes:
- **Buffer overflow**: Traffic rate too high for system capacity
- **CPU limitations**: Host system overloaded
- **Container resource limits**: Insufficient memory/CPU allocated
- **Network interface issues**: Virtual interface problems

## Troubleshooting Questions

### Q8: The containers won't start. What should I check?
**A:** Follow this checklist:
1. **Docker daemon running**: `systemctl status docker`
2. **Port availability**: `netstat -tulpn | grep 8080`
3. **Image availability**: `docker images | grep otg`
4. **Resource limits**: Check available memory and CPU
5. **Firewall settings**: Ensure ports are not blocked

### Q9: I'm getting "Connection refused" errors. How to fix?
**A:** Try these solutions:
1. **Wait for startup**: Controllers need time to initialize
2. **Check container status**: `docker ps -a`
3. **Verify network**: `docker network inspect otg-test-net`
4. **Test connectivity**: `curl http://localhost:8080/health`

### Q10: The statistics don't match expected values. Why?
**A:** Possible reasons:
- **Timing issues**: Statistics collected during ramp-up/down
- **Buffering effects**: Network buffers affecting packet counts
- **Measurement granularity**: Statistics update intervals
- **Configuration mismatch**: Flow settings not as expected

## Best Practices Questions

### Q11: What are the recommended system requirements?
**A:** Minimum requirements:
- **CPU**: 2+ cores
- **RAM**: 4GB available
- **Disk**: 10GB free space
- **OS**: Linux/macOS/Windows with Docker support

### Q12: How should I structure my test scripts?
**A:** Follow these patterns:
```python
# 1. Setup and initialization
# 2. Configuration creation
# 3. Resource allocation
# 4. Test execution
# 5. Results collection
# 6. Cleanup and teardown
```

### Q13: How can I make my tests more reliable?
**A:** Implement these practices:
- **Error handling**: Try-catch blocks around API calls
- **Retry logic**: For transient failures
- **Resource cleanup**: Always cleanup in finally blocks
- **Validation**: Verify configuration before execution
- **Logging**: Comprehensive logging for debugging

## Advanced Questions

### Q14: Can I run multiple flows simultaneously?
**A:** Yes! Create multiple flow objects:
```python
flow1 = Flow(name="flow_1", ...)
flow2 = Flow(name="flow_2", ...)
config.flows = [flow1, flow2]
```

### Q15: How do I implement bidirectional traffic?
**A:** Create flows in both directions:
```python
# A to B flow
flow_a_to_b = Flow(
    name="a_to_b",
    tx=FlowTx(device="device_a", port="port_a"),
    rx=FlowRx(device="device_b", port="port_b")
)

# B to A flow
flow_b_to_a = Flow(
    name="b_to_a", 
    tx=FlowTx(device="device_b", port="port_b"),
    rx=FlowRx(device="device_a", port="port_a")
)
```

### Q16: How can I save and load test configurations?
**A:** Use JSON serialization:
```python
# Save configuration
import json
config_dict = config.to_dict()
with open('test_config.json', 'w') as f:
    json.dump(config_dict, f, indent=2)

# Load configuration
with open('test_config.json', 'r') as f:
    config_dict = json.load(f)
config = Config.from_dict(config_dict)
```

## Getting Help

### Q17: Where can I find more documentation?
**A:** Additional resources:
- **OTG GitHub**: Official repository and documentation
- **API Reference**: Detailed API documentation
- **Community Forums**: User discussions and solutions
- **Keysight Support**: Official technical support

### Q18: How do I report bugs or request features?
**A:** Use these channels:
- **GitHub Issues**: For code-related problems
- **Community Forums**: For general questions
- **Support Tickets**: For critical issues
- **Feature Requests**: Through official channels

---

*Need more help? Check the troubleshooting guides or reach out to the community!*
