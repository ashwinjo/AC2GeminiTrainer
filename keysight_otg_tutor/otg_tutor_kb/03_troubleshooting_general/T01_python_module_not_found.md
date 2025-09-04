---
title: "Python Module Not Found"
troubleshooting_id: "T01"
category: "troubleshooting"
objective: "Resolve Python module import errors and missing package issues in OTG development environment."
tags: ["python", "modules", "import-errors", "packages", "environment"]
difficulty: "beginner"
---

# T01: Python Module Not Found

## 🐍 Problem Description
**Error Messages:**
- `ModuleNotFoundError: No module named 'otg_client'`
- `ImportError: cannot import name 'OtgClient'`
- `No module named 'requests'` or similar dependency errors

**When This Occurs:**
- Running Python scripts that import OTG-related modules
- First-time setup of OTG development environment
- After Python version changes or virtual environment issues

## 🔍 Root Cause Analysis

### Common Causes
1. **Missing Package Installation**: OTG client not installed via pip
2. **Virtual Environment Issues**: Wrong environment activated or not activated
3. **Python Path Problems**: Multiple Python installations causing confusion
4. **Version Incompatibility**: Wrong Python version or package version conflicts
5. **Permission Issues**: Insufficient permissions for package installation

## 🛠️ Solution Steps

### Solution 1: Install Missing Packages
```bash
# Install OTG client package
pip install otg-client

# Install additional common dependencies
pip install requests
pip install json-schema
pip install websocket-client

# Verify installation
python -c "import otg_client; print('OTG client installed successfully')"
```

### Solution 2: Virtual Environment Setup
```bash
# Create new virtual environment
python -m venv otg-env

# Activate virtual environment
# On Linux/macOS:
source otg-env/bin/activate

# On Windows:
otg-env\Scripts\activate

# Install packages in virtual environment
pip install otg-client

# Verify environment
which python
pip list | grep otg
```

### Solution 3: Python Version Verification
```bash
# Check Python version (need 3.8+)
python --version
python3 --version

# Use specific Python version if needed
python3.9 -m pip install otg-client
python3.9 your_script.py

# Create virtual environment with specific Python version
python3.9 -m venv otg-env-39
```

### Solution 4: System-Wide Installation (if virtual env not preferred)
```bash
# Install system-wide (may require sudo on Linux/macOS)
sudo pip install otg-client

# On Windows (run as Administrator)
pip install otg-client

# Alternative using python -m pip
python -m pip install otg-client --user
```

### Solution 5: Development Installation (from source)
```bash
# Clone repository
git clone https://github.com/open-traffic-generator/otg-client-python.git
cd otg-client-python

# Install in development mode
pip install -e .

# Or install from local directory
pip install .
```

## 🧪 Verification Steps

### Test 1: Basic Import Test
```python
#!/usr/bin/env python3
"""Test script to verify OTG client installation"""

try:
    import otg_client
    print("✅ otg_client imported successfully")
    print(f"   Version: {otg_client.__version__}")
except ImportError as e:
    print(f"❌ Failed to import otg_client: {e}")

try:
    from otg_client import OtgClient
    print("✅ OtgClient class imported successfully")
except ImportError as e:
    print(f"❌ Failed to import OtgClient: {e}")

try:
    from otg_client.models import Config, Device, Port, Flow
    print("✅ OTG models imported successfully")
except ImportError as e:
    print(f"❌ Failed to import OTG models: {e}")
```

### Test 2: Environment Verification
```bash
# Check current Python environment
echo "Python executable: $(which python)"
echo "Python version: $(python --version)"
echo "Pip location: $(which pip)"

# List installed packages
pip list | grep -E "(otg|requests|websocket)"

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Test 3: Full Connection Test
```python
#!/usr/bin/env python3
"""Complete environment test including OTG connection"""

import sys
import importlib.util

def check_module(module_name):
    """Check if module can be imported"""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def main():
    print("=== OTG Environment Verification ===\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}\n")
    
    # Check required modules
    modules = ['otg_client', 'requests', 'json', 'time']
    for module in modules:
        status = "✅" if check_module(module) else "❌"
        print(f"{status} {module}")
    
    # Try OTG client connection (if modules available)
    if check_module('otg_client'):
        try:
            from otg_client import OtgClient
            client = OtgClient("http://localhost:8080")
            print("\n✅ OTG client created successfully")
            print("   Note: Actual connection requires running OTG controller")
        except Exception as e:
            print(f"\n⚠️  OTG client creation failed: {e}")
    
    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    main()
```

## 🐛 Advanced Troubleshooting

### Issue: Multiple Python Installations
**Problem:** System has multiple Python versions causing confusion

**Solution:**
```bash
# Find all Python installations
ls -la /usr/bin/python*
ls -la /usr/local/bin/python*

# Use specific Python version consistently
alias python=/usr/bin/python3.9
alias pip=/usr/bin/python3.9 -m pip

# Or use full paths in scripts
#!/usr/bin/python3.9
```

### Issue: Permission Denied Errors
**Problem:** Cannot install packages due to permission restrictions

**Solutions:**
```bash
# Option 1: Use --user flag
pip install --user otg-client

# Option 2: Use virtual environment (recommended)
python -m venv ~/.otg-env
source ~/.otg-env/bin/activate
pip install otg-client

# Option 3: Use sudo (not recommended for development)
sudo pip install otg-client
```

### Issue: Proxy/Corporate Network Problems
**Problem:** Package installation fails due to network restrictions

**Solutions:**
```bash
# Configure pip proxy
pip install --proxy http://proxy.company.com:8080 otg-client

# Use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org otg-client

# Download and install offline
pip download otg-client
pip install otg-client*.whl --no-index --find-links .
```

### Issue: Package Version Conflicts
**Problem:** Conflicting package versions causing import errors

**Solutions:**
```bash
# Check for conflicts
pip check

# Create clean environment
python -m venv clean-otg-env
source clean-otg-env/bin/activate
pip install otg-client

# Force reinstall
pip uninstall otg-client
pip install otg-client --force-reinstall
```

## 📋 Prevention Strategies

### Best Practices
1. **Always Use Virtual Environments**: Isolate project dependencies
2. **Pin Package Versions**: Use requirements.txt with specific versions
3. **Regular Environment Testing**: Verify setup after changes
4. **Documentation**: Keep track of setup procedures

### Requirements.txt Example
```txt
# OTG Testing Environment Requirements
otg-client==1.0.0
requests>=2.25.0
websocket-client>=1.0.0
pytest>=6.0.0
```

### Environment Setup Script
```bash
#!/bin/bash
# setup_otg_env.sh - Automated environment setup

set -e

echo "Setting up OTG development environment..."

# Create virtual environment
python3 -m venv otg-env
source otg-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install otg-client requests websocket-client

# Verify installation
python -c "import otg_client; print('✅ Environment setup complete')"

echo "Environment ready! Activate with: source otg-env/bin/activate"
```

## 🆘 When All Else Fails

### Complete Environment Reset
```bash
# Remove all Python packages (use with caution)
pip freeze | xargs pip uninstall -y

# Or remove virtual environment entirely
rm -rf otg-env

# Start completely fresh
python -m venv fresh-otg-env
source fresh-otg-env/bin/activate
pip install --upgrade pip
pip install otg-client
```

### Alternative Installation Methods
```bash
# Using conda instead of pip
conda install -c conda-forge otg-client

# Using poetry
poetry add otg-client

# Direct from GitHub
pip install git+https://github.com/open-traffic-generator/otg-client-python.git
```

## 📞 Getting Help

### Information to Collect
When seeking help, provide:
```bash
# System information
uname -a
python --version
pip --version

# Environment information
pip list
echo $PYTHONPATH
which python
which pip

# Error details
python -c "import otg_client" 2>&1
```

### Support Resources
1. **OTG GitHub Repository**: Issues and discussions
2. **Python Package Index (PyPI)**: Package information
3. **Stack Overflow**: Community Q&A
4. **Official Documentation**: Installation guides

---

**Remember**: Module import errors are usually environment-related and can be resolved by ensuring packages are installed in the correct Python environment. When in doubt, start with a fresh virtual environment!
