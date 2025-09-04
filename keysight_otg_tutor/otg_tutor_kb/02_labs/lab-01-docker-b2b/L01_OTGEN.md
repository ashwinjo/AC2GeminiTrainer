
---
title: "Lab 1 OTGEN CLI Usage"
lab_id: "lab-01-docker-b2b"
category: "lab"
objective: "Learn how to use the OTGEN command-line interface tool to control OTG traffic generation and configuration."
tags: ["otgen", "cli", "command-line", "configuration", "traffic-control"]
difficulty: "intermediate"
---

## 🚀 Step-by-Step Instructions to use OTGEN with Ixia-c Controller

### Step 1: Install and Use OTGEN Tool

Install the otgen CLI utility:

```bash
# Install otgen tool
bash -c "$(curl -sL https://get.otgcdn.net/otgen)" -- -v 0.6.2
```

**Export current configuration:**
```bash
# Save current config to JSON
curl -k https://127.0.0.1:8443/config > ./lab-01-config.json

# View configuration
more lab-01-config.json
```

### Step 2: Run Tests with OTGEN

Execute tests using otgen tool:

```bash
# Run with flow metrics display
otgen run -k -a https://127.0.0.1:8443 -f lab-01-config.json -m flow | \
otgen transform -m flow | \
otgen display --mode table

# Run with port metrics display
otgen run -k -a https://127.0.0.1:8443 -f lab-01-config.json -m port | \
otgen transform -m port | \
otgen display --mode table
```

### Step 3: Modify JSON Configuration

Edit the JSON file to update flow parameters:

```bash
vi lab-01-config.json
```

**Changes to make:**
- Flow #1: 10,000 packets at 1,000 pps
- Rename second flow to "Flow #2 - Port 1 > Port 2"
- Update lines ~118, 123, and 280

**Test modified configuration:**
```bash
otgen run -k -a https://127.0.0.1:8443 -f lab-01-config.json -m flow | \
otgen transform -m flow | \
otgen display --mode table
```

### Step 4: Create Configuration with OTGEN

Set environment variables:

```bash
export OTG_API="https://localhost:8443"
export OTG_LOCATION_P1="localhost:5551"
export OTG_LOCATION_P2="localhost:5552"
```

**Create and run basic flow:**
```bash
# Create simple flow configuration and run
otgen create flow -s 1.1.1.1 -d 2.2.2.2 -p 80 --rate 100 --count 2000 | \
otgen run --insecure --metrics flow | \
otgen transform --metrics flow --counters frames | \
otgen display --mode table
```

**View created configuration:**
```bash
curl -k https://127.0.0.1:8443/config
```
