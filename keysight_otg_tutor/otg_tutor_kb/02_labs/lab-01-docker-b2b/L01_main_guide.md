# Lab 01: Docker Back-to-Back Testing - Main Guide

## Overview
This lab introduces you to setting up a basic Docker-based back-to-back (B2B) testing environment using OTG (Open Traffic Generator). You'll learn to create, configure, and run traffic between two endpoints in a controlled Docker environment.

## Learning Objectives
By the end of this lab, you will be able to:
- Set up Docker containers for OTG testing
- Configure basic back-to-back traffic flows
- Execute traffic generation and measurement
- Analyze basic traffic statistics

## Prerequisites
- Docker installed and running
- Python 3.8+ with pip
- Basic understanding of networking concepts
- Familiarity with command line interface

## Lab Architecture
```
[Traffic Generator A] <---> [Traffic Generator B]
     (Container 1)              (Container 2)
```

## Step-by-Step Instructions

### Step 1: Environment Setup
1. Verify Docker is running:
   ```bash
   docker --version
   docker ps
   ```

2. Pull the required OTG Docker images:
   ```bash
   docker pull keysight/otg-gnmi:latest
   docker pull keysight/otg-controller:latest
   ```

### Step 2: Container Configuration
1. Create a Docker network for the test:
   ```bash
   docker network create otg-test-net
   ```

2. Launch the OTG controller:
   ```bash
   docker run -d --name otg-controller \
     --network otg-test-net \
     -p 8080:8080 \
     keysight/otg-controller:latest
   ```

### Step 3: Traffic Configuration
1. Create your first OTG configuration
2. Define traffic flows between endpoints
3. Set traffic parameters (rate, duration, packet size)

### Step 4: Execute Test
1. Start traffic generation
2. Monitor real-time statistics
3. Stop traffic and collect results

### Step 5: Results Analysis
1. Review traffic statistics
2. Verify expected vs actual results
3. Identify any anomalies or issues

## Expected Results
- Successful container startup
- Traffic flows established between endpoints
- Statistics showing transmitted and received packets
- Zero packet loss in ideal conditions

## Next Steps
- Proceed to Lab 01 Code Implementation
- Review FAQ for common questions
- Attempt the Lab 01 Challenge for advanced practice

## Time Estimate
- Setup: 15 minutes
- Configuration: 20 minutes  
- Execution: 10 minutes
- Analysis: 15 minutes
- **Total: ~60 minutes**
