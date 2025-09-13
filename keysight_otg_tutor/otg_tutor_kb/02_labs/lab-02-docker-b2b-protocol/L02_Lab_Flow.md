---
title: "Lab 2 Interactive Flow - Docker Back-to-Back Testing with Protocol Engines"
lab_id: "lab-02-docker-b2b-protocol"
category: "lab"
objective: "Complete guided walkthrough of Lab 2 with interactive checkpoints, validation, and adaptive learning paths for protocol engine testing."
tags: ["interactive", "flow", "guided", "checkpoints", "validation", "protocol", "bgp"]
difficulty: "intermediate"
tutor_mode: "interactive"
---

# Lab 02: Interactive Lab Flow - Docker Back-to-Back Testing with Protocol Engines

## 🎯 Lab Overview for Gemini Tutor

This document provides the complete interactive flow for guiding users through Lab 02. As the AI tutor, use this to:
- **Assess user readiness** before starting each phase
- **Provide contextual help** based on user responses  
- **Validate progress** at each checkpoint
- **Adapt the learning path** based on user needs and errors
- **Ensure proper cleanup** and knowledge retention

## 📊 Lab Flow Visualization

```mermaid
flowchart TD
    A[Phase 0: Pre-Lab Assessment] --> B{Prerequisites Met?}
    B -->|No| C[Guide to Prerequisites]
    B -->|Yes| D[Phase 1: Environment Setup]
    C --> D
    
    D --> E[Phase 2: Docker Compose Deployment]
    E --> F{All 5 Containers Running?}
    F -->|No| G[Troubleshoot Containers]
    F -->|Yes| H[Phase 3: Protocol Configuration]
    G --> H
    
    H --> I[Phase 4: BGP Session Establishment]
    I --> J{BGP Sessions Established?}
    J -->|No| K[Protocol Troubleshooting]
    J -->|Yes| L[Phase 5: Protocol-Aware Traffic]
    K --> L
    
    L --> M[Phase 6: Metrics Analysis]
    M --> N[Phase 7: Challenge (Optional)]
    N --> O[Phase 8: Cleanup & Reflection]
    O --> P[Lab Complete]
    
    style A fill:#e1f5fe
    style H fill:#fff3e0
    style I fill:#f3e5f5
    style L fill:#e8f5e8
    style P fill:#e8f5e8
```

## 📚 Reference Files Available
- **L02_Lab_Goals.md** - Learning objectives and architecture
- **L02_Lab_Configuration.md** - Docker Compose setup instructions
- **L02_Lab_Test_Execution.md** - Protocol test execution steps
- **L02_Lab_Metrics.md** - Protocol and traffic metrics collection
- **L02_Challenge.md** - Advanced protocol exercises
- **L02_Cleanup.md** - Environment cleanup
- **L02_FAQ.md** - Common questions and answers
- **L02_Troubleshooting.md** - Issue resolution
- **L02_Command_Reference.md** - Quick command reference
- **L02_Code_lab-02_test.py.md** - Complete code walkthrough
- **L02_OTGEN.md** - CLI tool usage
- **L02_Use_Cases.md** - Real-world applications

## 🚀 Interactive Lab Flow

### Phase 0: Pre-Lab Assessment
**Tutor Action: Assess user readiness**

**Check Prerequisites:**
1. Use commands from **S01_environment_prerequisites.md** to verify Docker and Docker Compose installation
2. Use commands from **S01_environment_prerequisites.md** to verify Python version and snappi package
3. Verify Lab 01 completion and cleanup
4. Confirm basic BGP protocol knowledge
5. Verify tshark installation for packet capture analysis (see **L03_Lab_Packet_Capture.md**)

**Adaptive Response:**
- If prerequisites missing → Guide to **S01_environment_prerequisites.md**
- If Docker issues → Reference **T02_docker_daemon_not_running.md**
- If Python issues → Reference **T01_python_module_not_found.md**
- If Lab 01 not completed → Recommend completing Lab 01 first
- If tshark not installed → Guide to packet capture setup in **L03_Lab_Packet_Capture.md**
- If all good → Proceed to Phase 1

**Questions to Ask:**
- "Have you successfully completed Lab 01?"
- "What's your experience level with BGP protocol? (beginner/intermediate/advanced)"
- "Are you familiar with Docker Compose orchestration?"
- "Would you prefer step-by-step guidance or more independent exploration?"
- "Have you used packet capture tools like Wireshark/tshark before?"

**Packet Capture Preparation:**
- Review packet capture configuration in **L03_Lab_Packet_Capture.md**
- Understand BGP protocol message types for analysis
- Familiarize with tshark commands for traffic inspection
- Check storage space for PCAP files

### Phase 1: Environment Setup
**Tutor Action: Guide through initial setup**

**Learning Checkpoint 1.1: Understanding the Protocol Architecture**
- Show architecture diagram from **L02_Lab_Goals.md**
- Ask: "What's the difference between this lab and Lab 01?"
- Expected answer: Addition of Protocol Engines for BGP emulation
- If incorrect → Provide explanation and reference **L02_FAQ.md** Q1

**Learning Checkpoint 1.2: Docker Compose vs Docker Run**
- Explain why Docker Compose is used for Lab 02
- Reference **L02_Lab_Configuration.md** for compose.yml structure
- Ask: "Why do we use Docker Compose instead of individual docker run commands?"

**Validation Questions:**
- "How many containers will be deployed in this lab?" (Expected: 5)
- "What's the role of Protocol Engines in network testing?"
- "How does shared network architecture work between TE and PE?"

**Adaptive Response:**
- If user struggles with Docker Compose → Provide more detailed explanations
- If user is advanced → Allow them to examine compose.yml independently
- If errors occur → Reference **L02_Troubleshooting.md**

### Phase 2: Docker Compose Deployment
**Tutor Action: Guide through container orchestration**

**Learning Checkpoint 2.1: Docker Compose Deployment**
- Guide user through **L02_Lab_Configuration.md** deployment steps
- Use the exact `docker-compose -f compose.yml up -d` command from **L02_Lab_Configuration.md**
- Use the verification commands from **L02_Lab_Configuration.md**

**Learning Checkpoint 2.2: Container Network Architecture**
- Explain shared network namespace concept (`network_mode: service:`)
- Guide through **L02_Lab_Configuration.md** network inspection commands
- Use the verification commands from **L02_Lab_Configuration.md**

**Interactive Questions:**
- "How many Docker bridges are created?" (Expected: 1 - lab-02_default)
- "Why do Protocol Engines share Traffic Engine network namespaces?"
- "What ports are exposed and why?"

**Common Issues to Watch For:**
- Port conflicts → Reference **T04_port_is_already_allocated.md**
- Container startup failures → Check **L02_Troubleshooting.md**
- Network namespace issues → Provide troubleshooting steps

### Phase 3: Protocol Configuration
**Tutor Action: Guide through BGP protocol setup**

**Learning Checkpoint 3.1: BGP Fundamentals**
- Explain BGP concepts from **L02_Lab_Test_Execution.md**
- Ask: "What is an Autonomous System (AS)?"
- Expected answer: Administrative domain with unified routing policy
- Reference **L02_FAQ.md** for BGP fundamentals

**Learning Checkpoint 3.2: Protocol Configuration Analysis**
- Walk through **L02_Lab_Test_Execution.md** script analysis
- Explain AS numbers: 65001 and 65002 (private AS range)
- Discuss route advertisement: 10,000 routes per peer

**Interactive Validation:**
- "What IP addresses are used for BGP peering?" (Expected: 192.168.1.1, 192.168.1.2)
- "How many total routes will be advertised?" (Expected: 20,000)
- "What's the difference between IBGP and EBGP?" (This lab uses EBGP)

**Troubleshooting Triggers:**
- Protocol Engine connectivity issues → Check container health
- BGP configuration errors → Validate script parameters
- Network connectivity problems → Verify veth interfaces

### Phase 4: BGP Session Establishment
**Tutor Action: Guide through protocol session establishment**

**Learning Checkpoint 4.1: Test Script Execution**
- Guide user through **L02_Lab_Test_Execution.md** for the exact test execution command
- Monitor BGP session establishment in real-time
- Explain session states: Idle → Active → Established

**Learning Checkpoint 4.2: Protocol Convergence Monitoring**
- Use commands from **L02_Lab_Metrics.md** to monitor BGP sessions
- Set expectation: 30-60 seconds for full convergence
- Explain convergence process and timing

**Interactive Analysis:**
- "How long did BGP convergence take?"
- "Are both BGP sessions in 'Established' state?"
- "How many routes were advertised and received?"

**Real-time Troubleshooting:**
- BGP session failures → Check protocol engine logs
- Slow convergence → Verify container resources
- Route learning issues → Validate BGP configuration

### Phase 5: Protocol-Aware Traffic Testing
**Tutor Action: Teach protocol-traffic integration**

**Learning Checkpoint 5.1: Understanding Protocol-Aware Traffic**
- Explain how traffic uses BGP-learned routes
- Compare with Lab 01 static routing approach
- Reference **L02_Lab_Test_Execution.md** traffic configuration

**Learning Checkpoint 5.2: Traffic Generation Through Protocol Routes**
- Monitor traffic generation through established BGP routes
- Use commands from **L02_Lab_Test_Execution.md** for traffic monitoring
- Validate traffic success through protocol paths

**Critical Thinking Questions:**
- "How does traffic routing differ from Lab 01?"
- "What happens if BGP sessions fail during traffic generation?"
- "Why is protocol convergence important for traffic testing?"

### Phase 6: Metrics Analysis
**Tutor Action: Teach comprehensive metrics interpretation**

**Learning Checkpoint 6.1: Protocol Metrics Collection**
- Guide through **L02_Lab_Metrics.md** BGP metrics collection
- Use the exact commands from **L02_Lab_Metrics.md** for protocol monitoring
- Compare protocol metrics with traffic statistics

**Learning Checkpoint 6.2: Integrated Analysis**
- Use commands from **L02_Lab_Metrics.md** to correlate protocol and traffic metrics
- Explain the relationship between protocol state and traffic success
- Reference OpenAPI documentation for additional metrics

**Critical Thinking Questions:**
- "What's the correlation between BGP session state and traffic success?"
- "How would you troubleshoot traffic loss in a protocol-aware setup?"
- "What metrics indicate successful protocol-traffic integration?"

### Phase 7: Hands-on Challenge (Optional)
**Tutor Action: Assess practical understanding**

**Learning Checkpoint 7.1: Advanced Protocol Scenarios**
- Guide through **L02_Challenge.md**
- Ask user to modify protocol parameters:
  - Change AS numbers
  - Modify route advertisement counts
  - Test protocol failure scenarios

**Learning Checkpoint 7.2: Protocol Optimization**
- Follow the specific modifications outlined in **L02_Challenge.md**
- Use the validation methods specified in **L02_Challenge.md**
- Explore advanced BGP features

**Assessment Questions:**
- "What impact did changing AS numbers have on peering?"
- "How did route count changes affect convergence time?"
- "What happens when one BGP session fails?"

**Adaptive Learning:**
- If user struggles → Provide more guidance and protocol explanations
- If user excels → Introduce advanced concepts from **L02_Use_Cases.md**

### Phase 8: CLI Tool Exploration (Optional)
**Tutor Action: Introduce alternative interfaces**

**Learning Checkpoint 8.1: OTGEN CLI with Protocols**
- Guide through **L02_OTGEN.md**
- Show protocol configuration via CLI
- Compare with Python/snappi approach

**Discussion Points:**
- "How does CLI protocol configuration differ from Python?"
- "When might you prefer CLI over scripting for protocol testing?"

### Phase 9: Cleanup and Reflection
**Tutor Action: Ensure proper cleanup and knowledge consolidation**

**Learning Checkpoint 9.1: Protocol-Aware Cleanup**
- Guide through **L02_Cleanup.md**
- Emphasize graceful BGP session termination
- Validate each cleanup step including Docker Compose cleanup

**Learning Checkpoint 9.2: Knowledge Consolidation**
- Review key protocol concepts learned
- Ask user to explain the complete protocol-traffic workflow
- Identify areas for further protocol study

**Reflection Questions:**
- "What was the most challenging aspect of protocol engine testing?"
- "How would you apply protocol testing in a real network environment?"
- "What protocol concepts would you like to explore further?"

## 🎓 Tutor Guidance Framework

### Adaptive Responses Based on User Type

**Beginner User:**
- Provide detailed explanations for BGP protocol concepts
- Ask more validation questions about protocol fundamentals
- Offer additional context about routing protocols
- Reference FAQ frequently for protocol basics
- Be patient with protocol convergence timing

**Intermediate User:**
- Allow faster progression through basic protocol concepts
- Focus on deeper technical protocol details
- Encourage protocol parameter experimentation
- Introduce advanced topics from use cases
- Challenge with "what if" protocol scenarios

**Advanced User:**
- Provide high-level protocol guidance
- Focus on protocol architecture and design decisions
- Encourage independent protocol troubleshooting
- Introduce protocol optimization concepts
- Discuss real-world protocol deployment challenges

### Error Handling Strategy

**Common Error Categories:**
1. **Environment Issues** → Reference troubleshooting guides
2. **Protocol Misunderstandings** → Return to BGP fundamentals
3. **Container Issues** → Provide Docker Compose debugging
4. **BGP Configuration Problems** → Validate protocol parameters

**Escalation Path:**
1. Try guided protocol troubleshooting
2. Reference specific protocol documentation
3. Provide alternative protocol approaches
4. If persistent issues → Suggest environment reset

### Assessment Criteria

**Knowledge Checkpoints:**
- Understanding of protocol engine architecture ✓
- Docker Compose container management ✓
- BGP protocol fundamentals ✓
- Protocol-traffic integration concepts ✓
- Protocol metrics analysis skills ✓
- Protocol troubleshooting capabilities ✓

**Practical Skills:**
- Can set up protocol testing environment independently
- Can modify BGP protocol parameters
- Can interpret protocol and traffic results
- Can troubleshoot protocol-specific issues
- Can clean up protocol resources properly

### Success Indicators
- User completes all phases without major protocol issues
- Demonstrates understanding through protocol Q&A
- Successfully establishes BGP sessions
- Can explain protocol-traffic integration concepts
- Shows confidence in protocol troubleshooting

### Next Steps Recommendations
Based on user performance:
- **Struggling:** Review protocol fundamentals, repeat protocol sections
- **Progressing well:** Move to advanced protocol labs or explore use cases
- **Advanced:** Consider protocol optimization or multi-protocol scenarios

## 📋 Session Management

### Pre-Session Checklist
- [ ] Verify user environment meets protocol testing prerequisites
- [ ] Confirm all reference files are accessible
- [ ] Set appropriate protocol difficulty level
- [ ] Establish protocol learning objectives

### During Session
- [ ] Monitor user progress at each protocol checkpoint
- [ ] Provide timely feedback and encouragement for protocol concepts
- [ ] Adapt pace based on protocol understanding
- [ ] Document any protocol issues or suggestions

### Post-Session
- [ ] Ensure complete protocol-aware cleanup
- [ ] Summarize key protocol learnings
- [ ] Identify areas for protocol improvement
- [ ] Recommend next protocol steps
- [ ] Collect feedback for protocol tutorial improvement

---

**Note for Gemini:** This flow document should be used as your primary guide for conducting interactive Lab 02 sessions with protocol engines. Adapt the content, pace, and depth based on each user's responses and demonstrated understanding of both Docker orchestration and BGP protocol concepts. Always ensure safety through proper cleanup and validation at each step, with special attention to graceful protocol session termination.