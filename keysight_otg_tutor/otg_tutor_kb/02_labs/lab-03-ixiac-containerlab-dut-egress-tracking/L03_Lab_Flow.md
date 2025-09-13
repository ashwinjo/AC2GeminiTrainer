---
title: "Lab 3 Interactive Flow - IxiaC-ContainerLab-DUT-Egress-Tracking"
lab_id: "lab-03-ixiac-containerlab-dut-egress-tracking"
category: "lab"
objective: "Complete guided walkthrough of Lab 3 with interactive checkpoints, validation, and adaptive learning paths for egress tracking with DUT testing."
tags: ["interactive", "flow", "guided", "checkpoints", "validation", "egress-tracking", "containerlab", "dut"]
difficulty: "advanced"
tutor_mode: "interactive"
---

# Lab 03: Interactive Lab Flow - IxiaC-ContainerLab-DUT-Egress-Tracking

## 🎯 Lab Overview for Gemini Tutor

This document provides the complete interactive flow for guiding users through Lab 03. As the AI tutor, use this to:
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
    B -->|Yes| D[Phase 0.5: Egress Tracking Fundamentals]
    C --> D
    
    D --> E[Phase 1: Environment Setup]
    E --> F[Phase 2: ContainerLab Deployment]
    F --> G{All 6 Containers Running?}
    G -->|No| H[Troubleshoot Containers]
    G -->|Yes| I[Phase 3: DUT Configuration]
    H --> I
    
    I --> J[Phase 4: OTG Configuration & Egress Setup]
    J --> K[Phase 5: Test Execution with Egress Tracking]
    K --> L{Egress Tracking Working?}
    L -->|No| M[Troubleshoot Egress Tracking]
    L -->|Yes| N[Phase 6: Packet Capture Analysis]
    M --> N
    
    N --> O[Phase 7: Advanced Egress Analysis]
    O --> P[Phase 8: Challenge (Optional)]
    P --> Q[Phase 9: Cleanup & Reflection]
    Q --> R[Lab Complete]
    
    style A fill:#e1f5fe
    style D fill:#fff3e0
    style I fill:#f3e5f5
    style K fill:#e8f5e8
    style N fill:#fff9c4
    style R fill:#e8f5e8
```

## 📚 Reference Files Available
- **L03_Lab_Goals.md** - Learning objectives and architecture
- **L03_Lab_Configuration.md** - ContainerLab setup instructions
- **L03_Lab_Test_Execution.md** - Test execution steps
- **L03_Lab_Metrics.md** - Metrics collection and egress tracking analysis
- **L03_Egress_Tracking.md** - Comprehensive egress tracking guide
- **L03_Challenge.md** - Advanced egress tracking exercises
- **L03_Cleanup.md** - Environment cleanup
- **L03_FAQ.md** - Common questions and answers
- **L03_Troubleshooting.md** - Issue resolution
- **L03_Command_Reference.md** - Quick command reference
- **L03_Use_Cases.md** - Real-world applications

## 🚀 Interactive Lab Flow

### Phase 0: Pre-Lab Assessment
**Tutor Action: Assess user readiness**

**Check Prerequisites:**
1. Use commands from **S01_environment_prerequisites.md** to verify Docker installation
2. Use commands from **S01_environment_prerequisites.md** to verify Python version and snappi package
3. Verify ContainerLab installation and version
4. Verify Lab 01 and Lab 02 completion and cleanup
5. Confirm understanding of basic networking and QoS concepts


**Adaptive Response:**
- If prerequisites missing → Guide to **S01_environment_prerequisites.md**
- If Docker issues → Reference **T02_docker_daemon_not_running.md**
- If Python issues → Reference **T01_python_module_not_found.md**
- If ContainerLab not installed → Guide to ContainerLab installation
- If Lab 01/02 not completed → Recommend completing previous labs first
- If networking concepts unclear → Provide additional background
- If all good → Proceed to Phase 0.5

**Questions to Ask:**
- "Have you successfully completed Labs 01 and 02?"
- "What's your experience level with QoS and VLAN concepts? (beginner/intermediate/advanced)"
- "Are you familiar with ContainerLab orchestration?"
- "Have you worked with Nokia SRL or similar network devices?"
- "Would you prefer step-by-step guidance or more independent exploration?"

### Phase 0.5: Egress Tracking Fundamentals
**Tutor Action: Introduce advanced egress tracking concepts**

**Learning Checkpoint 0.5.1: Deep Dive into Egress Tracking**
- Reference **L03_Egress_Tracking.md** for comprehensive explanation
- Ask: "What do you think 'egress tracking' means in network testing?"
- Explain core concept: "Egress tracking is like a packet detective that monitors how packets are modified as they traverse network devices"
- Use the detailed comparisons from **L03_Egress_Tracking.md**

**Learning Checkpoint 0.5.2: Traditional vs. Egress Tracking Approach**
- Show detailed comparison from **L03_Egress_Tracking.md**:
  - Traditional: `[TX Port] → [DUT] → [RX Port]` (basic TX/RX stats)
  - Egress Tracking: `[TX Port] → [DUT] → [RX Port]` (TX Stats → Packet Changes → RX Stats + Tagged Metrics)
- Ask: "Why would basic TX/RX counters be insufficient for DUT testing?"
- Expected answers: Need to verify packet transformations, QoS markings, VLAN operations

**Learning Checkpoint 0.5.3: OTG/KENG Egress Tracking API**
- Walk through **L03_Egress_Tracking.md** API examples:
  ```python
  # Define egress packet structure
  f.egress_packet.ethernet()
  eg_vlan = f.egress_packet.add().vlan
  eg_ip = f.egress_packet.add().ipv4
  
  # Add metric tags for tracking
  eg_vlan.id.metric_tags.add(name="vlanIdRx")
  eg_ip.priority.dscp.metric_tags.add(name="dscpValuesRx")
  ```
- Explain: "This tells OTG what packet structure to expect and which fields to track"

**Learning Checkpoint 0.5.4: Lab 03 Specific Use Case**
- Reference **L03_Egress_Tracking.md** Lab 03 section
- Explain the test topology: OTG → Nokia SRL DUT → OTG (with sub-interfaces)
- Describe expected transformations:
  - VLAN tag insertion (101, 102, 103)
  - DSCP remarking (10 → 20)
  - Traffic distribution across sub-interfaces

**Interactive Questions:**
- "What types of DUT behaviors would you want to validate with egress tracking?"
- "How does egress tracking differ from manual packet capture?"
- "What advantages does automated egress tracking provide?"
- "In what scenarios might egress tracking be essential?"

**Adaptive Response:**
- If user is beginner → Focus on concepts, provide more examples
- If user is intermediate/advanced → Dive deeper into API details and use cases
- If user shows strong interest → Reference advanced sections from **L03_Egress_Tracking.md**

**Knowledge Bridge to Lab 03:**
- "This lab will demonstrate egress tracking in a real DUT scenario"
- "You'll see how Nokia SRL modifies packets and how we track those changes"
- "The skills you learn here apply to any DUT testing scenario"

### Phase 1: Environment Setup
**Tutor Action: Guide through initial setup**

**Learning Checkpoint 1.1: Understanding the ContainerLab Architecture**
- Show architecture diagram from **L03_Lab_Goals.md**
- Reference lab-03.yml topology structure
- Ask: "What's different about this lab compared to Labs 01 and 02?"
- Expected answer: Addition of DUT (Nokia SRL), ContainerLab orchestration, egress tracking focus
- If incorrect → Provide explanation and reference **L03_FAQ.md**

**Learning Checkpoint 1.2: ContainerLab vs Docker Compose**
- Explain why ContainerLab is used for Lab 03
- Reference **L03_Lab_Configuration.md** for topology structure
- Ask: "Why do we use ContainerLab instead of Docker Compose for this lab?"
- Expected answer: Better suited for network device emulation, topology management

**Validation Questions:**
- "How many containers will be deployed in this lab?" (Expected: 6 - controller, 2x TE, 2x PE, 1x SRL)
- "What's the role of the Nokia SRL container?"
- "How do Traffic Engines and Protocol Engines work together?"

**Adaptive Response:**
- If user struggles with ContainerLab → Provide more detailed explanations
- If user is advanced → Allow them to examine lab-03.yml independently
- If errors occur → Reference **L03_Troubleshooting.md**

### Phase 2: ContainerLab Deployment
**Tutor Action: Guide through container orchestration**

**Learning Checkpoint 2.1: ContainerLab Deployment**
- Guide user through **L03_Lab_Configuration.md** deployment steps
- Use the exact `containerlab deploy -t lab-03.yml` command
- Monitor container startup and readiness

**Learning Checkpoint 2.2: Container Network Architecture**
- Explain ContainerLab networking concepts
- Show how containers are interconnected
- Use verification commands from **L03_Lab_Configuration.md**

**Interactive Questions:**
- "Which containers share network namespaces and why?"
- "How does the Nokia SRL connect to the OTG traffic engines?"
- "What ports are exposed and for what purpose?"

**Common Issues to Watch For:**
- ContainerLab installation issues → Guide to installation
- Container startup failures → Check **L03_Troubleshooting.md**
- Network connectivity problems → Verify topology links
- Resource constraints → Check system requirements

### Phase 3: DUT Configuration
**Tutor Action: Guide through Nokia SRL setup**

**Learning Checkpoint 3.1: Nokia SRL Fundamentals**
- Explain Nokia SRL role as DUT
- Reference lab-03-srl.cfg configuration
- Ask: "What network functions will the SRL perform in this test?"
- Expected answer: VLAN tagging, QoS/DSCP remarking, sub-interface routing

**Learning Checkpoint 3.2: QoS and VLAN Configuration Analysis**
- Walk through **L03_Lab_Configuration.md** SRL configuration
- Explain QoS policies: DSCP 10 → FC1 → DSCP 20
- Explain VLAN subinterfaces: 101, 102, 103
- Show IP addressing scheme

**Interactive Validation:**
- "What DSCP value should we expect on egress?" (Expected: 20)
- "Which VLAN IDs will be added to packets?" (Expected: 101, 102, 103)
- "How will traffic be distributed across sub-interfaces?"

**Configuration Verification:**
- Use Nokia SRL CLI to verify configuration
- Check interface status and IP addresses
- Validate QoS policies are active

### Phase 4: OTG Configuration & Egress Setup
**Tutor Action: Guide through advanced OTG configuration**

**Learning Checkpoint 4.1: Test Script Analysis**
- Walk through **L03_Lab_Test_Execution.md** script analysis
- Reference lab-03-1_test.py for egress tracking configuration
- Explain device and flow setup with sub-interfaces

**Learning Checkpoint 4.2: Egress Tracking Configuration**
- Detailed walkthrough of egress packet definition:
  ```python
  f.egress_packet.ethernet()
  eg_vlan = f.egress_packet.add().vlan
  eg_ip = f.egress_packet.add().ipv4
  eg_vlan.id.metric_tags.add(name="vlanIdRx")
  ```
- Ask: "Why do we define the egress packet structure?"
- Expected answer: To tell OTG what packet format to expect after DUT processing

**Learning Checkpoint 4.3: Metric Tags Setup**
- Explain metric tag configuration
- Show how tagged metrics will be collected
- Reference **L03_Egress_Tracking.md** for detailed examples

**Interactive Questions:**
- "What fields are we tracking in this test?" (Expected: VLAN ID)
- "How will the results be different from basic flow metrics?"
- "What happens if the actual egress packets don't match our definition?"

### Phase 5: Test Execution with Egress Tracking
**Tutor Action: Guide through test execution and monitoring**

**Learning Checkpoint 5.1: Test Execution**
- Guide user through **L03_Lab_Test_Execution.md** execution steps
- Monitor test progress in real-time
- Watch for egress tracking metric collection

**Learning Checkpoint 5.2: Real-time Egress Monitoring**
- Use commands from **L03_Lab_Metrics.md** to monitor egress metrics
- Show tagged metrics as they're collected
- Explain the correlation between transmitted and received packets

**Interactive Analysis:**
- "Are packets being received on all expected VLAN IDs?"
- "Is the traffic distribution what you expected?"
- "Do you see the DSCP values being tracked correctly?"

**Real-time Troubleshooting:**
- Egress tracking not working → Check packet structure definition
- No tagged metrics → Verify metric tag configuration
- Unexpected results → Validate DUT configuration


### Phase 7: Advanced Egress Analysis
**Tutor Action: Teach comprehensive egress tracking analysis**

**Learning Checkpoint 7.1: Tagged Metrics Deep Dive**
- Use commands from **L03_Lab_Metrics.md** for detailed analysis
- Show tagged metrics breakdown by VLAN ID
- Calculate traffic distribution percentages

**Learning Checkpoint 7.2: Statistical Analysis**
- Reference **L03_Egress_Tracking.md** statistical analysis examples
- Analyze traffic distribution patterns
- Identify any anomalies or unexpected behavior

**Learning Checkpoint 7.3: Performance Correlation**
- Correlate egress tracking with overall flow performance
- Compare standard metrics with tagged metrics
- Assess impact of DUT processing on traffic

**Advanced Analysis Questions:**
- "Is the traffic distribution even across all VLANs?"
- "Are there any performance implications from the DUT processing?"
- "How would you detect and troubleshoot egress tracking anomalies?"

### Phase 8: Challenge (Optional)
**Tutor Action: Assess advanced understanding**

**Learning Checkpoint 8.1: Advanced Egress Scenarios**
- Guide through **L03_Challenge.md**
- Ask user to modify egress tracking parameters:
  - Add DSCP tracking alongside VLAN tracking
  - Change DUT QoS policies and observe results
  - Test failure scenarios

**Learning Checkpoint 8.2: Custom Egress Tracking**
- Follow specific modifications outlined in **L03_Challenge.md**
- Implement multiple field tracking
- Create custom analysis scripts

**Assessment Questions:**
- "What impact did adding DSCP tracking have on the results?"
- "How did changing QoS policies affect egress tracking?"
- "What happens when egress packet definition doesn't match reality?"

**Adaptive Learning:**
- If user struggles → Provide more guidance and egress tracking examples
- If user excels → Introduce advanced concepts from **L03_Use_Cases.md**

### Phase 9: Cleanup and Reflection
**Tutor Action: Ensure proper cleanup and knowledge consolidation**

**Learning Checkpoint 9.1: ContainerLab Cleanup**
- Guide through **L03_Cleanup.md**
- Use `containerlab destroy -t lab-03.yml` command
- Validate complete resource cleanup

**Learning Checkpoint 9.2: Knowledge Consolidation**
- Review key egress tracking concepts learned
- Ask user to explain the complete workflow
- Identify areas for further egress tracking study

**Reflection Questions:**
- "What was the most valuable aspect of egress tracking you learned?"
- "How would you apply egress tracking in a real network testing scenario?"
- "What egress tracking concepts would you like to explore further?"
- "How does this lab change your approach to DUT validation?"

## 🎓 Tutor Guidance Framework

### Adaptive Responses Based on User Type

**Beginner User:**
- Provide detailed explanations for egress tracking concepts
- Ask more validation questions about packet transformations
- Offer additional context about DUT testing
- Reference FAQ frequently for egress tracking basics
- Be patient with complex egress analysis

**Intermediate User:**
- Allow faster progression through basic egress concepts
- Focus on deeper technical egress tracking details
- Encourage egress tracking experimentation
- Introduce advanced topics from use cases
- Challenge with "what if" egress scenarios

**Advanced User:**
- Provide high-level egress tracking guidance
- Focus on architecture and egress tracking design decisions
- Encourage independent egress troubleshooting
- Introduce egress tracking optimization concepts
- Discuss real-world egress tracking deployment challenges

### Error Handling Strategy

**Common Error Categories:**
1. **Environment Issues** → Reference troubleshooting guides
2. **Egress Tracking Misunderstandings** → Return to fundamentals
3. **ContainerLab Issues** → Provide topology debugging
4. **DUT Configuration Problems** → Validate Nokia SRL setup
5. **Packet Analysis Confusion** → Correlate capture with tracking

**Escalation Path:**
1. Try guided egress tracking troubleshooting
2. Reference specific egress tracking documentation
3. Provide alternative egress tracking approaches
4. If persistent issues → Suggest environment reset

### Assessment Criteria

**Knowledge Checkpoints:**
- Understanding of egress tracking architecture ✓
- ContainerLab container management ✓
- DUT testing concepts ✓
- Egress tracking API configuration ✓
- Tagged metrics analysis skills ✓
- Packet capture correlation with egress tracking ✓
- Advanced egress troubleshooting capabilities ✓

**Practical Skills:**
- Can set up ContainerLab environment independently
- Can configure egress tracking in OTG
- Can interpret tagged metrics results
- Can correlate packet capture with egress data
- Can troubleshoot egress tracking issues
- Can clean up ContainerLab resources properly

### Success Indicators
- User completes all phases without major egress tracking issues
- Demonstrates understanding through egress Q&A
- Successfully configures and analyzes egress tracking
- Can explain egress tracking concepts to others
- Shows confidence in egress troubleshooting

### Next Steps Recommendations
Based on user performance:
- **Struggling:** Review egress fundamentals, repeat egress sections
- **Progressing well:** Explore advanced egress use cases or real-world applications
- **Advanced:** Consider contributing to egress tracking documentation or mentoring others

## 📋 Session Management

### Pre-Session Checklist
- [ ] Verify user environment meets egress tracking prerequisites
- [ ] Confirm all reference files are accessible
- [ ] Set appropriate egress tracking difficulty level
- [ ] Establish egress tracking learning objectives

### During Session
- [ ] Monitor user progress at each egress checkpoint
- [ ] Provide timely feedback and encouragement for egress concepts
- [ ] Adapt pace based on egress tracking understanding
- [ ] Document any egress issues or suggestions

### Post-Session
- [ ] Ensure complete ContainerLab cleanup
- [ ] Summarize key egress tracking learnings
- [ ] Identify areas for egress improvement
- [ ] Recommend next egress tracking steps
- [ ] Collect feedback for egress tutorial improvement

---

**Note for Gemini:** This flow document should be used as your primary guide for conducting interactive Lab 03 sessions with egress tracking focus. Adapt the content, pace, and depth based on each user's responses and demonstrated understanding of both ContainerLab orchestration and egress tracking concepts. Always ensure safety through proper cleanup and validation at each step, with special attention to ContainerLab resource management and egress tracking configuration validation.
