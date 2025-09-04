
---
title: "Lab 1 Challenge - Modify Test Parameters"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Practice modifying OTG test parameters by changing traffic rates, durations, packet sizes, and flow configurations."
tags: ["challenge", "modification", "parameters", "hands-on"]
difficulty: "beginner"
---

## 🚀 Step-by-Step Instructions to make edits to scripts and see the changes

### Step 1: Modify Test Configuration

Edit the test script to change parameters:

```bash
vim L01_lab_01_test.py
```

**Required changes:**
- **(a)** Rate: 200 fps instead of 100 fps
- **(b)** Duration: 5 seconds instead of 20 seconds
- **(c)** Frame size: 512 bytes instead of 128 bytes
- **(d)** Remove UDP header from one flow (ETH + IP only)
- **(e)** Change to unidirectional traffic (same direction)

**Verify changes:**
```bash
git diff
```

### Step 2: Execute Modified Test

Run the updated script:

```bash
python3 lab-01_test.py
```

**Compare results:**
```bash
# Save new interface counters
cat /proc/net/dev > counters2.log

# Compare before and after
diff counters1.log counters2.log

# Verify containers still running
docker ps -a
```
