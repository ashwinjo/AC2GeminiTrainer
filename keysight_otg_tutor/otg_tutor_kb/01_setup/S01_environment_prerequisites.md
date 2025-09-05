---
title: "Environment Prerequisites"
setup_id: "S01"
category: "setup"
objective: "Configure essential prerequisites starting from a minimal Ubuntu 22.04 installation for OTG lab exercises."
tags: ["prerequisites", "docker", "python", "ubuntu", "environment"]
difficulty: "beginner"
---

# S01: Environment Prerequisites

## 🎯 Overview

This guide starts from a minimal installation of Ubuntu 22.04 and guides the students through the configuration of most important prerequisites for the rest of the labs.

Please note that a typical test environment usually consists of one separate host for script execution and other hosts for running the test topology. The following lab exercises will however utilize an all-in-one deployment which combines the script execution environment with the test topology environment. This is very useful for learning purposes, and it is also an environment used by some network developers.

## 🖥️ PREPARATION: Connect to your lab machine

Login to the console of your assigned server. Feel free to use any SSH client terminal with the provided key. You should find a CloudShare link in your email with instructions for connecting to your virtual environment. If it's not there, please reach out to your instructor.

## 🐳 PREPARATION: Check DOCKER

Docker and docker-compose were installed as Ubuntu packages (e.g. "sudo apt install docker.io && sudo apt install docker-compose"). Check the version of the Docker Container Engine already installed on this machine.

Verify the list of container images which are already loaded in the local registry. You will notice no images exist in the registry.

Verify the list of containers which are already running on this host. You will notice there are no running containers.

## 🐍 PREPARATION: Check PYTHON and clone repository

Check the version of Python already installed on this Ubuntu machine.

## 📋 Commands to Execute

### Check System Information
```bash
#0-01
cat /etc/lsb-release
uname -a
```

### Check Docker Installation
```bash
#0-02
docker version && docker-compose version
```

### Verify Docker Images
```bash
#0-03
docker images
```

### Check Running Containers
```bash
#0-04
docker ps
```

### Check Python Version
```bash
#0-05
python3 --version
```

### Install Required Python Package
```bash
#0-06
python3 -m pip install snappi==1.14.0
```

---

**🎯 Key Points:**
- Start with minimal Ubuntu 22.04 installation
- Verify Docker and docker-compose are pre-installed
- Confirm Python 3 is available
- Install snappi version 1.14.0 for OTG testing

Your basic environment is now ready for the lab exercises! 🌟
