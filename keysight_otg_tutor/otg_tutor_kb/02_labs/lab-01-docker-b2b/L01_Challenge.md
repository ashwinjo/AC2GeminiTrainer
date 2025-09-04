# Lab 01: Advanced Challenge

## 🎯 Challenge Overview
Now that you've mastered the basic back-to-back testing, it's time to push your skills further! This challenge will test your understanding of OTG concepts and your ability to implement more complex scenarios.

## 🏆 Challenge Goals
By completing this challenge, you will demonstrate:
- Advanced OTG configuration skills
- Multi-flow traffic management
- Performance analysis and optimization
- Problem-solving with real-world constraints

## 📋 Challenge Requirements

### Challenge 1: Multi-Flow Bidirectional Traffic
**Difficulty:** ⭐⭐⭐

**Objective:** Create a test with multiple bidirectional traffic flows with different characteristics.

**Requirements:**
- 3 flows from Device A to Device B:
  - Flow 1: 64-byte packets at 1000 pps
  - Flow 2: 1518-byte packets at 500 pps  
  - Flow 3: Variable size packets (64-1518 bytes) at 750 pps
- 2 flows from Device B to Device A:
  - Flow 4: 128-byte packets at 2000 pps
  - Flow 5: 256-byte packets at 1500 pps

**Success Criteria:**
- All flows start and stop successfully
- Packet loss < 0.1% for all flows
- Statistics reported for each flow individually
- Total test duration: 60 seconds

**Starter Code Framework:**
```python
def create_multi_flow_config():
    """Create configuration with multiple bidirectional flows"""
    config = Config()
    
    # TODO: Implement your multi-flow configuration
    # Hint: Create separate Flow objects for each requirement
    
    return config

def analyze_multi_flow_stats(stats):
    """Analyze statistics for multiple flows"""
    # TODO: Implement per-flow analysis
    # Hint: Loop through flow statistics and validate each
    pass
```

### Challenge 2: Performance Optimization
**Difficulty:** ⭐⭐⭐⭐

**Objective:** Optimize the test setup to achieve maximum throughput without packet loss.

**Requirements:**
- Start with 1000 pps traffic rate
- Incrementally increase rate by 500 pps every 10 seconds
- Stop increasing when packet loss exceeds 0.01%
- Report the maximum sustainable rate
- Implement automatic rate adjustment

**Success Criteria:**
- Automated rate discovery algorithm
- Clear reporting of maximum sustainable rate
- Graceful handling of system limits
- Performance data logging

**Starter Code Framework:**
```python
def find_maximum_rate(client, initial_rate=1000, increment=500):
    """Find maximum sustainable traffic rate"""
    current_rate = initial_rate
    max_sustainable_rate = 0
    
    # TODO: Implement rate discovery algorithm
    # Hint: Loop with increasing rates, monitor packet loss
    
    return max_sustainable_rate

def performance_test(client):
    """Execute performance optimization test"""
    # TODO: Implement the complete performance test
    pass
```

### Challenge 3: Custom Protocol Stack
**Difficulty:** ⭐⭐⭐⭐⭐

**Objective:** Create a test with custom Ethernet/IP/UDP packet structure and validate packet content.

**Requirements:**
- Custom Ethernet header with specific MAC addresses
- IP header with custom DSCP markings
- UDP payload with incrementing sequence numbers
- Packet validation on receiver side
- Support for VLAN tagging (optional bonus)

**Success Criteria:**
- Packets generated with exact specifications
- Receiver validates packet structure and content
- Sequence number validation (detect missing/duplicate packets)
- DSCP markings preserved end-to-end

**Starter Code Framework:**
```python
def create_custom_packet_config():
    """Create configuration with custom packet structure"""
    config = Config()
    
    # TODO: Implement custom packet configuration
    # Hint: Use Flow.packet to define custom headers
    
    return config

def validate_packet_content(received_packets):
    """Validate received packet structure and content"""
    # TODO: Implement packet validation logic
    # Hint: Check headers, sequence numbers, DSCP markings
    pass
```

## 🛠️ Implementation Guidelines

### Getting Started
1. **Start with Challenge 1** - Build on your existing knowledge
2. **Use incremental development** - Test each flow individually first
3. **Implement robust error handling** - Challenges will stress your system
4. **Add comprehensive logging** - You'll need it for debugging

### Development Tips
```python
# Use this enhanced base class for challenges
class ChallengeTest:
    def __init__(self):
        self.client = OtgClient("http://localhost:8080")
        self.results = {}
        
    def setup(self):
        """Common setup for all challenges"""
        # TODO: Implement common setup
        pass
        
    def teardown(self):
        """Common cleanup for all challenges"""
        # TODO: Implement cleanup
        pass
        
    def run_challenge(self, challenge_func):
        """Run a challenge with proper setup/teardown"""
        try:
            self.setup()
            return challenge_func()
        except Exception as e:
            print(f"Challenge failed: {e}")
            return False
        finally:
            self.teardown()
```

### Validation Framework
```python
def validate_results(expected, actual, tolerance=0.01):
    """Validate test results with tolerance"""
    for metric in expected:
        exp_val = expected[metric]
        act_val = actual.get(metric, 0)
        
        if abs(exp_val - act_val) / exp_val > tolerance:
            return False, f"{metric}: expected {exp_val}, got {act_val}"
    
    return True, "All metrics within tolerance"
```

## 📊 Scoring and Evaluation

### Scoring Criteria
- **Functionality (40%)**: Does the solution work correctly?
- **Code Quality (25%)**: Is the code clean, readable, and well-structured?
- **Error Handling (20%)**: How well does it handle edge cases and errors?
- **Performance (15%)**: How efficiently does it execute?

### Bonus Points
- **Creative Solutions**: Novel approaches to the challenges
- **Additional Features**: Going beyond the basic requirements  
- **Documentation**: Well-commented code and clear explanations
- **Testing**: Unit tests or additional validation

## 🎖️ Achievement Levels

### 🥉 Bronze Level
- Complete Challenge 1 successfully
- Basic error handling implemented
- Code runs without crashes

### 🥈 Silver Level  
- Complete Challenges 1 and 2
- Robust error handling and logging
- Performance optimizations implemented

### 🥇 Gold Level
- Complete all three challenges
- Exceptional code quality and documentation
- Creative solutions and bonus features

## 📝 Submission Guidelines

### What to Submit
1. **Complete source code** for all attempted challenges
2. **Test results** showing successful execution
3. **Brief documentation** explaining your approach
4. **Performance data** (for Challenge 2)

### Code Structure
```
challenge_submission/
├── challenge_1_multi_flow.py
├── challenge_2_performance.py  
├── challenge_3_custom_protocol.py
├── results/
│   ├── challenge_1_results.log
│   ├── challenge_2_performance.json
│   └── challenge_3_validation.log
└── README.md
```

## 🤔 Hints and Tips

### General Hints
- **Start simple**: Get basic functionality working first
- **Test incrementally**: Don't try to implement everything at once
- **Monitor resources**: Watch CPU and memory usage during tests
- **Use timeouts**: Prevent infinite loops in optimization algorithms

### Challenge-Specific Hints

**Challenge 1:**
- Create flows in a loop to avoid repetitive code
- Use dictionaries to store flow configurations
- Implement per-flow statistics collection

**Challenge 2:**
- Use binary search for faster rate discovery
- Implement moving average for packet loss calculation
- Add safety limits to prevent system overload

**Challenge 3:**
- Study the OTG packet API documentation carefully
- Use packet capture tools for validation
- Implement checksum verification

## 🆘 Getting Help

### Debugging Resources
- Enable debug logging: `logging.basicConfig(level=logging.DEBUG)`
- Use packet capture: `tcpdump` or `Wireshark`
- Monitor system resources: `htop`, `docker stats`

### Community Support
- Post questions in the discussion forum
- Share non-solution code snippets for help
- Collaborate on debugging (but submit individual solutions)

---

## 🚀 Ready to Start?

Choose your challenge level and begin! Remember:
- **Quality over speed** - Take time to implement robust solutions
- **Learn from failures** - Each error teaches you something valuable
- **Ask questions** - The community is here to help
- **Have fun** - Challenges should be engaging, not frustrating!

Good luck, and may your packets flow without loss! 📡✨
