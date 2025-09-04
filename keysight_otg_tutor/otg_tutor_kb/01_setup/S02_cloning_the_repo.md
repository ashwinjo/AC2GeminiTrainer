# S02: Cloning the Repository

## 🎯 Overview
This guide walks you through cloning the OTG tutorial repository, understanding its structure, and setting up your local development environment for hands-on learning.

## 📂 Repository Structure
Before cloning, let's understand what you'll be working with:

```
keysight_otg_tutor/
├── tutor_prompt_manual_state.txt    # AI tutor configuration
├── session_state.json               # Your learning progress
└── otg_tutor_kb/                     # Knowledge base
    ├── 00_concepts/                  # Fundamental concepts
    ├── 01_setup/                     # Setup guides (this file!)
    ├── 02_labs/                      # Hands-on laboratories
    ├── 03_troubleshooting_general/   # Common issue solutions
    └── 04_reference/                 # Quick reference materials
```

## 🔗 Repository Information

### Primary Repository
- **URL**: `https://github.com/keysight/otg-tutor`
- **Type**: Public repository
- **License**: MIT License
- **Language**: Python, Markdown, YAML

### Alternative Sources
- **Mirror**: `https://gitlab.com/keysight/otg-tutor`
- **Archive**: Available as ZIP download
- **Codespaces**: GitHub Codespaces ready

## 🚀 Cloning Methods

### Method 1: HTTPS Clone (Recommended for beginners)
```bash
# Clone the repository
git clone https://github.com/keysight/otg-tutor.git

# Navigate to the directory
cd otg-tutor

# Verify the clone
ls -la
```

### Method 2: SSH Clone (For experienced Git users)
```bash
# First, ensure SSH key is set up with GitHub
# Then clone using SSH
git clone git@github.com:keysight/otg-tutor.git

# Navigate to the directory
cd otg-tutor
```

### Method 3: GitHub CLI (Modern approach)
```bash
# Install GitHub CLI if not already installed
# Linux: sudo apt install gh
# macOS: brew install gh
# Windows: winget install GitHub.cli

# Authenticate with GitHub
gh auth login

# Clone the repository
gh repo clone keysight/otg-tutor

# Navigate to the directory
cd otg-tutor
```

### Method 4: Download ZIP (No Git required)
```bash
# Download and extract ZIP file
curl -L https://github.com/keysight/otg-tutor/archive/main.zip -o otg-tutor.zip
unzip otg-tutor.zip
cd otg-tutor-main
```

## 🔧 Post-Clone Setup

### 1. Verify Repository Contents
```bash
# Check repository structure
tree -L 3  # If tree is installed
# Or use ls -la for basic listing

# Verify important files exist
ls -la tutor_prompt_manual_state.txt
ls -la session_state.json
ls -la otg_tutor_kb/

# Check Git status
git status
git log --oneline -5  # See recent commits
```

### 2. Set Up Python Environment
```bash
# Create virtual environment in the repo directory
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    # Install basic OTG requirements
    pip install otg-client requests pyyaml pytest
fi
```

### 3. Environment Configuration
```bash
# Create .env file for local configuration
cat > .env << EOF
# Local OTG Configuration
OTG_CONTROLLER_URL=http://localhost:8080
OTG_LOG_LEVEL=INFO
OTG_TIMEOUT=30

# Docker Configuration  
DOCKER_NETWORK=otg-test-net
DOCKER_SUBNET=172.20.0.0/16

# Development Settings
DEVELOPMENT_MODE=true
AUTO_CLEANUP=true
EOF

# Make .env file readable only by user
chmod 600 .env
```

### 4. Git Configuration (Optional but recommended)
```bash
# Set up Git for contributions
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create development branch
git checkout -b my-learning-branch

# Set up remote tracking
git push -u origin my-learning-branch
```

## 📋 Repository Exploration

### Understanding the Knowledge Base
```bash
# Explore concepts
ls otg_tutor_kb/00_concepts/
cat otg_tutor_kb/00_concepts/C01_what_is_otg.md | head -20

# Check available labs
ls otg_tutor_kb/02_labs/
ls otg_tutor_kb/02_labs/lab-01-docker-b2b/

# Review troubleshooting guides
ls otg_tutor_kb/03_troubleshooting_general/

# Check reference materials
ls otg_tutor_kb/04_reference/
```

### Session State Understanding
```bash
# View your progress tracking file
cat session_state.json | python3 -m json.tool

# The session state tracks:
# - Your learning progress
# - Completed labs and exercises
# - Performance metrics
# - Personal preferences
```

### Tutor Configuration
```bash
# Review the AI tutor's configuration
cat tutor_prompt_manual_state.txt

# This file contains:
# - Teaching methodology
# - Interaction guidelines
# - Knowledge scope
# - Assessment criteria
```

## 🧪 Verification and Testing

### Repository Integrity Check
```bash
#!/bin/bash
# verify_repo.sh - Verify repository integrity

echo "=== Repository Verification ==="

# Check Git status
echo "Git status:"
git status --porcelain

# Verify directory structure
echo "Checking directory structure..."
required_dirs=(
    "otg_tutor_kb/00_concepts"
    "otg_tutor_kb/01_setup" 
    "otg_tutor_kb/02_labs"
    "otg_tutor_kb/03_troubleshooting_general"
    "otg_tutor_kb/04_reference"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir exists"
    else
        echo "❌ $dir missing"
    fi
done

# Check key files
key_files=(
    "tutor_prompt_manual_state.txt"
    "session_state.json"
    "otg_tutor_kb/02_labs/lab-01-docker-b2b/L01_main_guide.md"
)

for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

echo "=== Verification Complete ==="
```

### Environment Test
```python
#!/usr/bin/env python3
"""test_repo_setup.py - Test repository setup"""

import os
import sys
import json
from pathlib import Path

def test_repository_structure():
    """Test that repository has expected structure"""
    print("=== Testing Repository Structure ===")
    
    # Check if we're in the right directory
    if not Path("tutor_prompt_manual_state.txt").exists():
        print("❌ Not in otg-tutor repository directory")
        return False
    
    # Check directory structure
    required_dirs = [
        "otg_tutor_kb/00_concepts",
        "otg_tutor_kb/01_setup",
        "otg_tutor_kb/02_labs", 
        "otg_tutor_kb/03_troubleshooting_general",
        "otg_tutor_kb/04_reference"
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} missing")
            return False
    
    return True

def test_session_state():
    """Test session state file"""
    print("\n=== Testing Session State ===")
    
    try:
        with open("session_state.json", "r") as f:
            session_data = json.load(f)
        
        # Check required keys
        required_keys = ["user_profile", "progress", "session_data", "preferences"]
        for key in required_keys:
            if key in session_data:
                print(f"✅ {key} section exists")
            else:
                print(f"❌ {key} section missing")
                return False
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in session_state.json: {e}")
        return False
    except FileNotFoundError:
        print("❌ session_state.json not found")
        return False

def test_python_environment():
    """Test Python environment setup"""
    print("\n=== Testing Python Environment ===")
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}")
    else:
        print(f"❌ Python {version.major}.{version.minor} too old")
        return False
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment active")
    else:
        print("⚠️  No virtual environment detected")
    
    # Test package imports
    try:
        import otg_client
        print("✅ otg_client available")
    except ImportError:
        print("❌ otg_client not installed")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Repository Setup Test\n")
    
    tests = [
        test_repository_structure,
        test_session_state,
        test_python_environment
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    if all_passed:
        print("\n✅ All tests passed! Repository is ready for use.")
        print("\n🚀 Next steps:")
        print("1. Review otg_tutor_kb/00_concepts/ to understand OTG")
        print("2. Start with otg_tutor_kb/02_labs/lab-01-docker-b2b/")
        print("3. Use troubleshooting guides when needed")
    else:
        print("\n❌ Some tests failed. Please fix issues before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 🔄 Keeping Repository Updated

### Pulling Latest Changes
```bash
# Check for updates
git fetch origin

# View changes
git log HEAD..origin/main --oneline

# Pull latest changes
git pull origin main

# If you have local changes, use rebase
git pull --rebase origin main
```

### Handling Conflicts
```bash
# If there are conflicts during pull
git status  # See conflicted files

# Edit conflicted files to resolve
# Then add resolved files
git add <resolved-file>

# Continue rebase if using --rebase
git rebase --continue

# Or commit if using regular pull
git commit -m "Resolve merge conflicts"
```

### Creating Your Own Fork
```bash
# Fork on GitHub (use web interface)
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/otg-tutor.git

# Add upstream remote
git remote add upstream https://github.com/keysight/otg-tutor.git

# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your fork
git checkout main
git merge upstream/main
git push origin main
```

## 📁 Working with the Repository

### Creating Practice Space
```bash
# Create personal practice directory
mkdir my-practice
cd my-practice

# Copy lab templates for practice
cp -r ../otg_tutor_kb/02_labs/lab-01-docker-b2b/ ./my-lab-01/

# Make modifications without affecting original
cd my-lab-01
# ... make your changes ...
```

### Organizing Your Work
```bash
# Create branch for each lab
git checkout -b lab-01-practice
# ... work on lab 01 ...
git add .
git commit -m "Complete lab 01 exercises"

git checkout -b lab-02-practice
# ... work on lab 02 ...
```

### Saving Progress
```bash
# Commit your progress regularly
git add .
git commit -m "Progress on lab 01: completed basic setup"

# Push to your fork (if you have one)
git push origin lab-01-practice

# Create backup of session state
cp session_state.json session_state_backup_$(date +%Y%m%d).json
```

## 🚨 Troubleshooting Clone Issues

### Common Problems and Solutions

#### Permission Denied (SSH)
```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub account
cat ~/.ssh/id_ed25519.pub
# Copy and paste into GitHub Settings > SSH Keys
```

#### Network/Proxy Issues
```bash
# Configure Git proxy
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy https://proxy.company.com:8080

# Or use environment variables
export https_proxy=http://proxy.company.com:8080
export http_proxy=http://proxy.company.com:8080
```

#### Large Repository Size
```bash
# Shallow clone (less history)
git clone --depth 1 https://github.com/keysight/otg-tutor.git

# Clone specific branch only
git clone -b main --single-branch https://github.com/keysight/otg-tutor.git
```

#### Disk Space Issues
```bash
# Check available space
df -h

# Clean up if needed
docker system prune -a
pip cache purge

# Use sparse checkout for specific directories only
git clone --filter=blob:none --sparse https://github.com/keysight/otg-tutor.git
cd otg-tutor
git sparse-checkout set otg_tutor_kb/02_labs
```

## 🎓 Next Steps

After successfully cloning and setting up:

1. **Explore the Knowledge Base**: Start with `00_concepts/`
2. **Review Prerequisites**: Ensure all requirements from S01 are met
3. **Begin Lab 01**: Navigate to `02_labs/lab-01-docker-b2b/`
4. **Join Community**: Connect with other learners
5. **Set Up Development Tools**: Configure your preferred IDE

## 📚 Additional Resources

### Git Learning Resources
- [Pro Git Book](https://git-scm.com/book) - Comprehensive Git guide
- [GitHub Learning Lab](https://lab.github.com/) - Interactive Git tutorials
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) - Practical Git guides

### Repository Maintenance
- Keep your fork updated with upstream changes
- Use meaningful commit messages
- Create pull requests for contributions
- Follow the project's contribution guidelines

---

**🎯 Key Points:**
- Choose the cloning method that fits your experience level
- Set up virtual environment in the repository directory
- Verify repository integrity after cloning
- Keep repository updated with latest changes
- Use branches for different learning activities

You're now ready to dive into the OTG learning materials! 🌟
