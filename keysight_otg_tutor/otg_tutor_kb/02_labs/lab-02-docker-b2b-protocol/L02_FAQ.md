---
title: "Lab 2 Frequently Asked Questions (FAQ)"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Find answers to common questions about protocol engine testing, BGP configuration, and advanced OTG scenarios."
tags: ["faq", "troubleshooting", "protocol", "bgp", "help"]
difficulty: "intermediate"
---

# Lab 02: Frequently Asked Questions (FAQ)

## Protocol Engine Questions

### Q1: What's the difference between traffic engines and protocol engines?
**A:** Traffic engines generate and receive packets at high rates, while protocol engines emulate network protocols (BGP, OSPF, ARP, etc.). Protocol engines establish sessions, exchange control messages, and maintain protocol state machines.

### Q2: Why do we need both traffic and protocol engines?
**A:** Protocol engines establish the control plane (routing tables, protocol sessions), while traffic engines handle the data plane (actual packet forwarding). This separation allows realistic network protocol testing.

### Q3: How long does BGP convergence typically take?
**A:** In lab environments, BGP convergence usually takes 30-60 seconds depending on:
- Number of routes being advertised
- BGP timer configurations
- System resource availability
- Network complexity

## BGP Configuration Questions

### Q4: What BGP parameters can I modify in the test?
**A:** Key configurable BGP parameters:
```python
# BGP peer configuration
bgp_peer.as_number = 65001
bgp_peer.router_id = "192.168.1.1"
bgp_peer.hold_time = 180
bgp_peer.keepalive_interval = 60

# Route advertisement
bgp_routes.prefix = "10.0.0.0/8"
bgp_routes.count = 10000
bgp_routes.step = 256
```

### Q5: How do I troubleshoot BGP session establishment failures?
**A:** Follow this troubleshooting sequence:
1. **Check container connectivity**: `docker ps -a`
2. **Verify protocol engine logs**: `docker logs protocol-engine-1`
3. **Check BGP configuration**: Validate AS numbers, router IDs
4. **Monitor session states**: Use API to check BGP session status
5. **Network connectivity**: Ensure virtual interfaces are up

### Q6: Can I test other protocols besides BGP?
**A:** Yes! Protocol engines support multiple protocols:
- **BGP**: Route advertisement and path selection
- **OSPF**: Link-state routing protocol
- **ARP**: Address resolution
- **LACP**: Link aggregation
- **STP**: Spanning tree protocol

## Advanced Protocol Questions

### Q7: How do I implement route filtering?
**A:** Configure prefix lists or route maps:
```python
# Prefix list filtering
bgp_peer.route_filter = {
    "prefix_list": ["10.1.0.0/16", "10.2.0.0/16"],
    "action": "permit"
}

# AS path filtering
bgp_peer.as_path_filter = {
    "as_path_regex": "^65001_",
    "action": "deny"
}
```

### Q8: What happens if a protocol session fails during traffic?
**A:** Behavior depends on the failure scenario:
- **Session flap**: Traffic may be dropped until reconvergence
- **Route withdrawal**: Traffic reroutes if alternate paths exist
- **Complete failure**: All traffic through that peer stops
- **Recovery**: Automatic reconvergence when session restores

## Performance and Scaling Questions

### Q9: How many BGP routes can I advertise?
**A:** Typical limits in lab environment:
- **Small scale**: 1,000-10,000 routes per peer
- **Medium scale**: 10,000-100,000 routes per peer
- **Large scale**: 100,000+ routes (requires more resources)

Resource requirements increase with route count.

### Q10: How do I optimize protocol convergence time?
**A:** Several optimization strategies:
- **Reduce BGP timers**: Lower hold time and keepalive intervals
- **Limit route advertisements**: Start with fewer routes
- **Resource allocation**: Ensure adequate container resources
- **Network stability**: Minimize interface flapping

## Troubleshooting Protocol Issues

### Q11: BGP sessions stuck in "Active" state
**A:** Common causes and solutions:
- **Configuration mismatch**: Verify AS numbers and router IDs
- **Network connectivity**: Check virtual interface status
- **Resource constraints**: Monitor container CPU/memory usage
- **Timer conflicts**: Adjust BGP hold time and keepalive intervals

### Q12: Routes not being learned/advertised
**A:** Troubleshooting steps:
1. **Check BGP session state**: Must be "Established"
2. **Verify route configuration**: Confirm prefix and count settings
3. **Check route policies**: Ensure no filtering is blocking routes
4. **Monitor protocol logs**: Look for error messages in container logs

### Q13: Traffic not flowing through established routes
**A:** Possible issues:
- **Route installation**: Check if routes are installed in forwarding table
- **Traffic configuration**: Verify traffic uses correct source/destination
- **Protocol convergence**: Ensure full convergence before traffic start
- **Interface mapping**: Confirm traffic engines use correct interfaces

## Integration Questions

### Q14: How does this integrate with real network devices?
**A:** Protocol engines can peer with real network equipment:
- Configure real routers to peer with protocol engine IPs
- Use appropriate AS numbers and routing policies
- Monitor both simulated and real protocol sessions
- Validate end-to-end connectivity

### Q15: Can I save and replay protocol configurations?
**A:** Yes, use configuration templates:
```python
# Save configuration
protocol_config = bgp_peer.to_dict()
with open('bgp_config.json', 'w') as f:
    json.dump(protocol_config, f)

# Load and replay
with open('bgp_config.json', 'r') as f:
    saved_config = json.load(f)
bgp_peer = BgpPeer.from_dict(saved_config)
```

---

*Need more help with protocol-specific questions? Check the troubleshooting guides or reach out to the community!*
