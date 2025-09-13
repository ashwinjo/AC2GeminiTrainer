---
title: "Lab 4 Interactive Flow - IxiaC-ContainerLab-DUT-Convergence"
lab_id: "lab-04-ixiac-containerlab-dut-convergence"
category: "lab"
objective: "Complete guided walkthrough of Lab 4 with interactive checkpoints, validation, and adaptive learning paths for BGP convergence testing."
tags: ["interactive", "flow", "guided", "checkpoints", "validation", "convergence", "bgp", "ixia-c-one"]
difficulty: "advanced"
tutor_mode: "interactive"
---

# Lab 04: Interactive Lab Flow - IxiaC-ContainerLab-DUT-Convergence

## 🎯 Lab Overview for Gemini Tutor

This document provides the complete interactive flow for guiding users through Lab 04. As the AI tutor, use this to:
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
    B -->|Yes| D[Phase 0.5: BGP Convergence Fundamentals]
    C --> D
    
    D --> E[Phase 1: Environment Setup]
    E --> F[Phase 2: ContainerLab Deployment]
    F --> G{Both Containers Running?}
    G -->|No| H[Troubleshoot Deployment]
    G -->|Yes| I[Phase 3: BGP Configuration Validation]
    H --> I
    
    I --> J[Phase 4: Baseline Traffic Establishment]
    J --> K{Traffic Flowing Correctly?}
    K -->|No| L[Troubleshoot BGP/Traffic]
    K -->|Yes| M[Phase 5: Link Down Convergence Test]
    L --> M
    
    M --> N[Phase 6: Route Withdrawal Convergence Test]
    N --> O[Phase 7: Convergence Analysis & Comparison]
    O --> P[Phase 8: Advanced Scenarios (Optional)]
    P --> Q[Phase 9: Cleanup & Reflection]
    Q --> R[Lab Complete]
    
    style A fill:#e1f5fe
    style D fill:#fff3e0
    style I fill:#f3e5f5
    style M fill:#e8f5e8
    style N fill:#e8f5e8
    style O fill:#fff9c4
    style R fill:#e8f5e8
```

## 📚 Reference Files Available
- **L04_Lab_Goals.md** - Learning objectives and BGP convergence architecture
- **L04_Lab_Configuration.md** - ContainerLab setup with Ixia-C-One
- **L04_Lab_Test_Execution.md** - BGP convergence test execution steps
- **L04_Lab_Metrics.md** - Convergence metrics collection and analysis
- **L04_Challenge.md** - Advanced convergence testing exercises
- **L04_Cleanup.md** - Environment cleanup
- **L04_FAQ.md** - Common questions and answers
- **L04_Troubleshooting.md** - Issue resolution
- **L04_Command_Reference.md** - Quick command reference
- **L04_Use_Cases.md** - Real-world applications

## 🚀 Interactive Lab Flow

### Phase 0: Pre-Lab Assessment
**Tutor Action: Assess user readiness for advanced BGP convergence testing**

**Check Prerequisites:**
1. Use commands from **S01_environment_prerequisites.md** to verify Docker installation
2. Use commands from **S01_environment_prerequisites.md** to verify Python version and snappi package
3. Verify ContainerLab installation and version
4. Confirm completion of Lab 01, Lab 02, and Lab 03
5. Assess BGP protocol knowledge and convergence concepts
6. Check understanding of network resilience principles

**Adaptive Response:**
- If prerequisites missing → Guide to **S01_environment_prerequisites.md**
- If Docker issues → Reference **T02_docker_daemon_not_running.md**
- If Python issues → Reference **T01_python_module_not_found.md**
- If ContainerLab not installed → Guide to ContainerLab installation
- If previous labs not completed → Recommend completing prerequisite labs
- If BGP knowledge gaps → Provide BGP fundamentals overview
- If all good → Proceed to Phase 0.5

**Questions to Ask:**
- "Have you successfully completed Labs 01, 02, and 03?"
- "What's your experience level with BGP protocol? (beginner/intermediate/advanced)"
- "Are you familiar with network convergence concepts like failover and recovery time?"
- "Have you worked with Ixia-C-One all-in-one containers before?"
- "What's your understanding of the difference between hard and soft failures?"

### Phase 0.5: BGP Convergence Fundamentals
**Tutor Action: Introduce advanced BGP convergence concepts**

**Learning Checkpoint 0.5.1: Understanding Network Convergence**
- Reference **L04_Lab_Goals.md** for comprehensive convergence explanation
- Ask: "What do you think 'network convergence' means in BGP context?"
- Explain core concept: "Network convergence is the time it takes for a network to adapt to topology changes and restore connectivity"
- Use real-world analogies: "Like GPS recalculating route after road closure"

**Learning Checkpoint 0.5.2: BGP Convergence vs Basic Connectivity**
- Show comparison from **L04_Lab_Goals.md**:
  - Basic Testing: "Is traffic flowing?" (Labs 01-03)
  - Convergence Testing: "How quickly does network recover from failures?" (Lab 04)
- Ask: "Why is convergence time important for production networks?"
- Expected answers: SLA compliance, user experience, business continuity

**Learning Checkpoint 0.5.3: Types of Network Failures**
- Explain failure classifications from **L04_Lab_Goals.md**:
  ```
  Hard Failure (Link Down): Physical link failure
  - Detection: Physical layer monitoring
  - Recovery: Route recalculation + path switch
  - Time: 1-5 seconds (includes detection delay)
  
  Soft Failure (Route Withdrawal): BGP route removal
  - Detection: Immediate BGP UPDATE processing
  - Recovery: Best path recalculation
  - Time: 0.1-1 second (no physical detection)
  ```

**Learning Checkpoint 0.5.4: Lab 04 Specific Scenario**
- Reference **L04_Lab_Goals.md** architecture section
- Explain the test topology: Ixia-C-One → Nokia SRL → Dual BGP paths
- Describe expected behavior:
  - Primary path: eth2 (higher Local Preference)
  - Backup path: eth3 (lower Local Preference)  
  - Convergence trigger: Link down or route withdrawal on primary path

**Interactive Questions:**
- "What factors might affect network convergence time?"
- "How would you measure convergence time in a production environment?"
- "What's the difference between convergence time and detection time?"
- "Why might route withdrawal be faster than link failure recovery?"

**Adaptive Response:**
- If user is beginner → Focus on concepts, provide more examples
- If user is intermediate/advanced → Dive deeper into BGP path selection details
- If user shows strong interest → Reference advanced sections from **L04_Lab_Goals.md**

**Knowledge Bridge to Lab 04:**
- "This lab will demonstrate both hard and soft failure scenarios"
- "You'll measure actual convergence times and understand the factors that influence them"
- "The skills you learn apply to any production network resilience testing"

### Phase 1: Environment Setup
**Tutor Action: Guide through ContainerLab and Ixia-C-One setup**

**Learning Checkpoint 1.1: Understanding Ixia-C-One Architecture**
- Show architecture comparison from **L04_Lab_Configuration.md**
- Ask: "What's different about Ixia-C-One compared to previous lab setups?"
- Expected answer: All-in-one container vs separate controller/traffic engines
- Explain benefits: Simplified deployment, integrated management, resource efficiency

**Learning Checkpoint 1.2: ContainerLab Topology Analysis**
- Guide user through **L04_Lab_Configuration.md** topology analysis
- Reference the lab-04.yml structure
- Ask: "Why do we need three interfaces between Ixia-C-One and Nokia SRL?"
- Expected answer: eth1 (traffic), eth2 (BGP peer 1), eth3 (BGP peer 2)

**Validation Questions:**
- "How many containers will be deployed?" (Expected: 2)
- "What's the role of Nokia SRL in this convergence testing?"
- "How does Ixia-C-One simplify the testing architecture?"

**Adaptive Response:**
- If user struggles with ContainerLab → Provide more detailed explanations
- If user is advanced → Allow them to examine lab-04.yml independently
- If errors occur → Reference **L04_Troubleshooting.md**

### Phase 2: ContainerLab Deployment
**Tutor Action: Guide through container orchestration**

**Learning Checkpoint 2.1: ContainerLab Deployment**
- Guide user through **L04_Lab_Configuration.md** deployment steps
- Use the exact `sudo containerlab deploy -t lab-04.yml` command
- Monitor container startup and readiness

**Learning Checkpoint 2.2: Ixia-C-One Verification**
- Explain Ixia-C-One integration testing from **L04_Lab_Configuration.md**
- Use verification commands to test API connectivity
- Show how all-in-one architecture simplifies management

**Interactive Questions:**
- "What advantages do you see with the all-in-one approach?"
- "How does this compare to the multi-container setup in previous labs?"
- "What might be the trade-offs of using Ixia-C-One vs separate components?"

**Common Issues to Watch For:**
- Ixia-C-One image download time → Set expectations for first run
- Container startup sequence → Explain dependency management
- API connectivity issues → Provide troubleshooting steps

### Phase 3: BGP Configuration Validation
**Tutor Action: Guide through BGP setup verification**

**Learning Checkpoint 3.1: Nokia SRL BGP Configuration**
- Guide through **L04_Lab_Test_Execution.md** DUT verification steps
- Explain iBGP vs eBGP concepts from previous labs
- Ask: "What's different about iBGP that requires a route reflector?"
- Expected answer: iBGP split-horizon rule prevents peer-to-peer route sharing

**Learning Checkpoint 3.2: BGP Path Selection Attributes**
- Explain Local Preference and MED configuration from **L04_Lab_Test_Execution.md**
- Show BGP path selection hierarchy:
  1. Local Preference (higher wins)
  2. AS Path length (shorter wins)
  3. MED (lower wins)
  4. Other tie-breakers

**Interactive Validation:**
- "Which BGP peer should be the primary path and why?" (Expected: eth2 due to higher Local Preference)
- "What happens if both peers have the same Local Preference?"
- "How does the route reflector enable iBGP communication?"

**Configuration Deep Dive:**
- Use Nokia SRL CLI to examine BGP configuration
- Show route reflector setup and client configuration
- Validate interface addressing and connectivity

### Phase 4: Baseline Traffic Establishment
**Tutor Action: Establish baseline performance before convergence testing**

**Learning Checkpoint 4.1: Test Script Configuration**
- Walk through **L04_Lab_Test_Execution.md** script configuration
- Explain Ixia-C-One addressing simplification (eth1, eth2, eth3)
- Show BGP peer configuration with different attributes

**Learning Checkpoint 4.2: Baseline Traffic Validation**
- Execute baseline traffic test without convergence events
- Monitor BGP session establishment and route learning
- Validate traffic flows via primary path (eth2)

**Interactive Analysis:**
- "Are both BGP sessions established successfully?"
- "Which peer is being used for traffic forwarding and why?"
- "What's the baseline packet loss rate?"
- "How do you verify traffic is flowing via the expected path?"

**Troubleshooting Guidance:**
- BGP sessions not establishing → Check IP addressing and routing
- Traffic not flowing → Verify route advertisement and path selection
- Unexpected path selection → Review BGP attributes configuration

### Phase 5: Link Down Convergence Test
**Tutor Action: Execute and analyze hard failure scenario**

**Learning Checkpoint 5.1: Link Down Event Execution**
- Guide through **L04_Lab_Test_Execution.md** link down scenario
- Explain the test sequence: Baseline → Link Down → Recovery → Analysis
- Set expectations for convergence behavior and timing

**Learning Checkpoint 5.2: Real-time Monitoring**
- Show parallel monitoring from **L04_Lab_Test_Execution.md**:
  - OTG traffic metrics
  - Nokia SRL BGP status
  - Route table changes
- Explain what to observe during convergence

**Interactive Observation:**
- "What do you see happening in the BGP neighbor status?"
- "How long does it take for traffic to switch to the backup path?"
- "What's the pattern of packet loss during convergence?"

**Learning Checkpoint 5.3: Convergence Time Calculation**
- Use **L04_Lab_Metrics.md** calculation methodology
- Formula: Convergence Time = (Lost Packets ÷ Transmission Rate)
- Show practical example with actual test results

**Critical Analysis Questions:**
- "What factors contributed to the total convergence time?"
- "How does this compare to your expectations?"
- "What could be done to improve convergence time?"

### Phase 6: Route Withdrawal Convergence Test
**Tutor Action: Execute and analyze soft failure scenario**

**Learning Checkpoint 6.1: Route Withdrawal Event**
- Guide through **L04_Lab_Test_Execution.md** route withdrawal scenario
- Explain the difference from link down: BGP UPDATE vs physical failure
- Set expectations for faster convergence

**Learning Checkpoint 6.2: Comparative Analysis**
- Monitor the same metrics as link down test
- Compare convergence behavior and timing
- Analyze why route withdrawal is typically faster

**Interactive Comparison:**
- "How does this convergence compare to the link down scenario?"
- "Why is route withdrawal typically faster?"
- "What are the pros and cons of each failure type?"

**Learning Checkpoint 6.3: BGP UPDATE Message Analysis**
- Explain BGP UPDATE withdrawal mechanism
- Show how graceful shutdown differs from abrupt failure
- Discuss real-world scenarios for each failure type

### Phase 7: Convergence Analysis & Comparison
**Tutor Action: Comprehensive analysis of both scenarios**

**Learning Checkpoint 7.1: Metrics Analysis**
- Use **L04_Lab_Metrics.md** analysis techniques
- Compare convergence times, packet loss, and recovery patterns
- Generate comparative charts and statistics

**Learning Checkpoint 7.2: Route Scale Impact Assessment**
- If time permits, test with different route counts (50, 100, 500 routes)
- Analyze scaling impact on convergence time
- Understand linear relationship between routes and processing time

**Interactive Analysis:**
- "What's the relationship between route count and convergence time?"
- "Which scenario would be more disruptive in production?"
- "How do these results compare to typical SLA requirements?"

**Learning Checkpoint 7.3: Production Implications**
- Discuss SLA compliance and user impact
- Explain how convergence testing validates network resilience
- Connect lab results to real-world network operations

### Phase 8: Advanced Scenarios (Optional)
**Tutor Action: Explore advanced convergence concepts**

**Learning Checkpoint 8.1: Multiple Failure Scenarios**
- Guide through **L04_Challenge.md** advanced scenarios
- Test sequential failures and recovery patterns
- Analyze complex failure interactions

**Learning Checkpoint 8.2: Optimization Techniques**
- Discuss BGP timer tuning for faster convergence
- Explore route aggregation impact
- Consider hardware vs software forwarding differences

**Assessment Questions:**
- "How would you optimize this network for faster convergence?"
- "What trade-offs exist between convergence speed and stability?"
- "How would you apply these concepts in a production environment?"

### Phase 9: Cleanup & Reflection
**Tutor Action: Ensure proper cleanup and knowledge consolidation**

**Learning Checkpoint 9.1: Environment Cleanup**
- Guide through **L04_Cleanup.md** ContainerLab cleanup
- Use `sudo containerlab destroy -t lab-04.yml --cleanup` command
- Validate complete resource cleanup

**Learning Checkpoint 9.2: Knowledge Consolidation**
- Review key BGP convergence concepts learned
- Ask user to explain convergence testing methodology
- Identify areas for further convergence study

**Reflection Questions:**
- "What was the most surprising aspect of convergence testing you learned?"
- "How would you apply BGP convergence testing in your network environment?"
- "What convergence concepts would you like to explore further?"
- "How does this lab change your approach to network resilience planning?"

## 🎓 Tutor Guidance Framework

### Adaptive Responses Based on User Type

**Beginner User (New to BGP/Convergence):**
- Provide detailed explanations for BGP convergence concepts
- Ask more validation questions about fundamental principles
- Offer additional context about network resilience importance
- Reference FAQ frequently for convergence basics
- Be patient with complex convergence analysis

**Intermediate User (Some BGP Experience):**
- Allow faster progression through basic BGP concepts
- Focus on deeper convergence analysis techniques
- Encourage convergence parameter experimentation
- Introduce advanced topics from use cases
- Challenge with "what if" convergence scenarios

**Advanced User (Network Operations Experience):**
- Provide high-level convergence guidance
- Focus on production implications and optimization
- Encourage independent convergence troubleshooting
- Introduce convergence optimization concepts
- Discuss real-world convergence deployment challenges

### Error Handling Strategy

**Common Error Categories:**
1. **Environment Issues** → Reference troubleshooting guides
2. **BGP Convergence Misunderstandings** → Return to fundamentals
3. **ContainerLab Issues** → Provide topology debugging
4. **Ixia-C-One Configuration Problems** → Validate all-in-one setup
5. **Convergence Analysis Confusion** → Simplify metrics interpretation

**Escalation Path:**
1. Try guided convergence troubleshooting
2. Reference specific BGP convergence documentation
3. Provide alternative convergence approaches
4. If persistent issues → Suggest environment reset

### Assessment Criteria

**Knowledge Checkpoints:**
- Understanding of BGP convergence principles ✓
- ContainerLab and Ixia-C-One management ✓
- Network failure classification concepts ✓
- Convergence time calculation methodology ✓
- BGP path selection and route reflection ✓
- Comparative analysis skills (hard vs soft failures) ✓
- Production application understanding ✓

**Practical Skills:**
- Can deploy ContainerLab with Ixia-C-One independently
- Can configure and execute BGP convergence tests
- Can interpret convergence metrics and calculate recovery times
- Can differentiate between failure types and their characteristics
- Can troubleshoot BGP convergence issues
- Can apply convergence concepts to production scenarios

### Success Indicators
- User completes all phases without major convergence issues
- Demonstrates understanding through convergence Q&A
- Successfully executes both hard and soft failure scenarios
- Can explain convergence concepts and their production implications
- Shows confidence in convergence analysis and troubleshooting

### Next Steps Recommendations
Based on user performance:
- **Struggling:** Review BGP fundamentals, repeat convergence sections
- **Progressing well:** Explore advanced convergence optimization or real-world applications
- **Advanced:** Consider contributing to convergence testing methodologies or mentoring others

---

**Note for Gemini:** This flow document should be used as your primary guide for conducting interactive Lab 04 sessions with BGP convergence focus. The lab involves complex concepts, so adapt the content, pace, and depth based on each user's responses and demonstrated understanding. Always ensure safety through proper cleanup and validation at each step, with special attention to helping users understand the practical implications of network convergence testing.