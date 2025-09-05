---
title: "Lab 1 Interactive Flow - Docker Back-to-Back Testing"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Complete guided walkthrough of Lab 1 with interactive checkpoints, validation, and adaptive learning paths."
tags: ["interactive", "flow", "guided", "checkpoints", "validation"]
difficulty: "beginner"
tutor_mode: "interactive"
---

# Lab 01: Interactive Lab Flow - Docker Back-to-Back Testing

## 🎯 Lab Overview for Gemini Tutor

This document provides the complete interactive flow for guiding users through Lab 01. As the AI tutor, use this to:
- **Assess user readiness** before starting each phase
- **Provide contextual help** based on user responses
- **Validate progress** at each checkpoint
- **Adapt the learning path** based on user needs and errors
- **Ensure proper cleanup** and knowledge retention

## 📚 Reference Files Available
- **L01_Lab_Goals.md** - Learning objectives and architecture
- **L01_Lab_Configuration.md** - Docker setup instructions
- **L01_Lab_Test_Execution.md** - Test execution steps
- **L01_Lab_Metrics.md** - Metrics collection
- **L01_Challenge.md** - Parameter modification exercises
- **L01_Cleanup.md** - Environment cleanup
- **L01_FAQ.md** - Common questions and answers
- **L01_Troubleshooting.md** - Issue resolution
- **L01_Command_Reference.md** - Quick command reference
- **L01_Code_lab-01_test.py.md** - Complete code walkthrough
- **L01_OTGEN.md** - CLI tool usage
- **L01_Use_Cases.md** - Real-world applications

## 🚀 Interactive Lab Flow

### Phase 0: Pre-Lab Assessment
**Tutor Action: Assess user readiness**

**Check Prerequisites:**
1. Ask user to confirm Docker installation: `docker --version`
2. Verify Python 3.8+: `python3 --version`
3. Check sudo access: `sudo echo "test"`
4. Confirm basic networking knowledge

**Adaptive Response:**
- If prerequisites missing → Guide to **S01_environment_prerequisites.md**
- If Docker issues → Reference **T02_docker_daemon_not_running.md**
- If Python issues → Reference **T01_python_module_not_found.md**
- If all good → Proceed to Phase 1

**Questions to Ask:**
- "What's your experience level with Docker? (beginner/intermediate/advanced)"
- "Have you worked with network testing tools before?"
- "Would you prefer step-by-step guidance or more independent exploration?"

### Phase 1: Environment Setup
**Tutor Action: Guide through initial setup**

**Learning Checkpoint 1.1: Understanding the Architecture**
- Show architecture diagram from **L01_Lab_Goals.md**
- Ask: "Can you explain what back-to-back testing means?"
- Expected answer: Direct connection between devices without intermediate equipment
- If incorrect → Provide explanation and reference **L01_FAQ.md** Q1

**Learning Checkpoint 1.2: Docker Image Setup**
- Guide user through **L01_Lab_Configuration.md** Step 1
- Ask user to execute: `docker pull` commands
- Validate: `docker images | grep -E "(keng-controller|ixia-c-traffic-engine)"`

**Validation Questions:**
- "Why do we use specific image versions rather than 'latest'?"
- "What's the difference between the controller and traffic engine containers?"

**Adaptive Response:**
- If user struggles with Docker → Provide more detailed explanations
- If user is advanced → Allow them to proceed faster
- If errors occur → Reference **L01_Troubleshooting.md**

### Phase 2: Network Interface Creation
**Tutor Action: Explain virtual networking concepts**

**Learning Checkpoint 2.1: Virtual Interfaces**
- Explain veth pairs concept
- Guide user through **L01_Lab_Configuration.md** Step 2
- Guide through: `sudo ip link add name veth0 type veth peer name veth1`
- Validate: `ip link show | grep veth`

**Interactive Questions:**
- "What happens when we create a veth pair?"
- "Why do we need virtual interfaces for this lab?"

**Common Issues to Watch For:**
- Permission errors → Guide to use `sudo`
- Interface already exists → Show cleanup commands
- Network namespace issues → Provide troubleshooting steps

### Phase 3: Container Deployment
**Tutor Action: Guide through container orchestration**

**Learning Checkpoint 3.1: Controller Container**
- Explain controller role in OTG architecture
- Guide through controller startup
- Guide user through **L01_Lab_Configuration.md** Step 3
- Test connectivity: `curl -k https://localhost:8443/api/v1/config`

**Learning Checkpoint 3.2: Traffic Engine Containers**
- Explain traffic engine purpose
- Guide user through **L01_Lab_Configuration.md** Step 4
- Guide through both traffic engine deployments
- Validate: `docker ps | grep ixia-c-traffic-engine`

**Interactive Validation:**
- "How many containers should be running now?" (Expected: 3)
- "What ports are the containers listening on?"
- "What would happen if we used the same port for both traffic engines?"

**Troubleshooting Triggers:**
- Port conflicts → Reference **T04_port_is_already_allocated.md**
- Container startup failures → Check **L01_Troubleshooting.md**
- Network connectivity issues → Validate Docker networking

### Phase 4: Test Execution
**Tutor Action: Guide through traffic generation**

**Learning Checkpoint 4.1: Code Understanding**
- Walk through **L01_Code_lab-01_test.py.md**
- Ask: "What traffic parameters are configured in the test?"
- Expected: 2000 packets, 100 pps, bidirectional

**Learning Checkpoint 4.2: Test Execution**
- Guide user to run: `python3 L01_lab_01_test.py`
- Monitor execution in real-time
- Ask user to observe the output

**Interactive Analysis:**
- "How long did the test take to complete?"
- "What was the actual vs expected duration?"
- "Were there any packet losses? Why or why not?"

**Real-time Troubleshooting:**
- Connection errors → Check container status
- Import errors → Reference **T01_python_module_not_found.md**
- Timeout issues → Verify network setup

### Phase 5: Metrics Analysis
**Tutor Action: Teach metrics interpretation**

**Learning Checkpoint 5.1: Understanding Metrics**
- Guide through **L01_Lab_Metrics.md**
- Ask user to check interface counters: `cat /proc/net/dev`
- Compare before/after test execution

**Learning Checkpoint 5.2: OTG API Metrics**
- Show how to query API directly: `curl -k https://localhost:8443/api/v1/results/metrics`
- Explain different metric types

**Critical Thinking Questions:**
- "Why might there be a difference between interface counters and OTG metrics?"
- "What factors could cause packet loss in a B2B setup?"
- "How would you troubleshoot if packets weren't being received?"

### Phase 6: Hands-on Challenge
**Tutor Action: Assess practical understanding**

**Learning Checkpoint 6.1: Parameter Modification**
- Guide through **L01_Challenge.md**
- Ask user to modify test parameters:
  - Change rate from 100 to 200 pps
  - Change duration from 20 to 5 seconds
  - Change frame size from 128 to 512 bytes

**Learning Checkpoint 6.2: Advanced Modifications**
- Remove UDP header from one flow
- Change to unidirectional traffic
- Validate changes with `git diff`

**Assessment Questions:**
- "What impact did changing the rate have on test duration?"
- "How did frame size affect the total bytes transmitted?"
- "What's the difference between unidirectional and bidirectional traffic?"

**Adaptive Learning:**
- If user struggles → Provide more guidance and examples
- If user excels → Introduce advanced concepts from **L01_Use_Cases.md**

### Phase 7: CLI Tool Exploration (Optional)
**Tutor Action: Introduce alternative interfaces**

**Learning Checkpoint 7.1: OTGEN CLI**
- Guide through **L01_OTGEN.md**
- Show alternative configuration method
- Compare with Python/snappi approach

**Discussion Points:**
- "When might you prefer CLI over Python scripting?"
- "What are the advantages of each approach?"

### Phase 8: Cleanup and Reflection
**Tutor Action: Ensure proper cleanup and knowledge consolidation**

**Learning Checkpoint 8.1: Proper Cleanup**
- Guide through **L01_Cleanup.md**
- Validate each cleanup step
- Ensure no resources left running

**Learning Checkpoint 8.2: Knowledge Consolidation**
- Review key concepts learned
- Ask user to explain the complete workflow
- Identify areas for further study

**Reflection Questions:**
- "What was the most challenging part of this lab?"
- "How would you apply this knowledge in a real-world scenario?"
- "What would you like to explore further?"

## 🎓 Tutor Guidance Framework

### Adaptive Responses Based on User Type

**Beginner User:**
- Provide detailed explanations for each step
- Ask more validation questions
- Offer additional context and background
- Reference FAQ frequently
- Be patient with troubleshooting

**Intermediate User:**
- Allow faster progression through basic steps
- Focus on deeper technical concepts
- Encourage experimentation
- Introduce advanced topics from use cases
- Challenge with "what if" scenarios

**Advanced User:**
- Provide high-level guidance
- Focus on architecture and design decisions
- Encourage independent problem-solving
- Introduce optimization concepts
- Discuss real-world implementation challenges

### Error Handling Strategy

**Common Error Categories:**
1. **Environment Issues** → Reference troubleshooting guides
2. **Conceptual Misunderstandings** → Return to fundamentals
3. **Execution Errors** → Provide step-by-step debugging
4. **Configuration Problems** → Validate prerequisites

**Escalation Path:**
1. Try guided troubleshooting
2. Reference specific documentation
3. Provide alternative approaches
4. If persistent issues → Suggest environment reset

### Assessment Criteria

**Knowledge Checkpoints:**
- Understanding of OTG architecture ✓
- Docker container management ✓
- Virtual networking concepts ✓
- Traffic generation principles ✓
- Metrics analysis skills ✓
- Troubleshooting capabilities ✓

**Practical Skills:**
- Can set up lab environment independently
- Can modify test parameters
- Can interpret results
- Can troubleshoot common issues
- Can clean up resources properly

### Success Indicators
- User completes all phases without major issues
- Demonstrates understanding through Q&A
- Successfully modifies test parameters
- Can explain concepts to others
- Shows confidence in troubleshooting

### Next Steps Recommendations
Based on user performance:
- **Struggling:** Review fundamentals, repeat sections
- **Progressing well:** Move to Lab 02 or explore use cases
- **Advanced:** Consider contributing to documentation or helping others

## 📋 Session Management

### Pre-Session Checklist
- [ ] Verify user environment meets prerequisites
- [ ] Confirm all reference files are accessible
- [ ] Set appropriate difficulty level
- [ ] Establish learning objectives

### During Session
- [ ] Monitor user progress at each checkpoint
- [ ] Provide timely feedback and encouragement
- [ ] Adapt pace based on user responses
- [ ] Document any issues or suggestions

### Post-Session
- [ ] Ensure complete cleanup
- [ ] Summarize key learnings
- [ ] Identify areas for improvement
- [ ] Recommend next steps
- [ ] Collect feedback for tutorial improvement

---

**Note for Gemini:** This flow document should be used as your primary guide for conducting interactive Lab 01 sessions. Adapt the content, pace, and depth based on each user's responses and demonstrated understanding. Always ensure safety through proper cleanup and validation at each step.