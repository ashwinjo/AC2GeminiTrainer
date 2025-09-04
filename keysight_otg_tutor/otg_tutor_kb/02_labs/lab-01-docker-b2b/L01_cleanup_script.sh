#!/bin/bash
# L01_cleanup_script.sh - Complete Lab 01 cleanup
# Matches the cleanup steps in L01_Cleanup.md

echo "=== Lab 01 Cleanup Script ==="

# Step 1: Stop containers
echo "Stopping containers..."
docker stop controller traffic-engine-1 traffic-engine-2 2>/dev/null || true

# Step 2: Remove containers
echo "Removing containers..."
docker rm controller traffic-engine-1 traffic-engine-2 2>/dev/null || true

# Step 3: Remove virtual interfaces
echo "Removing virtual interfaces..."
sudo ip link delete veth0 2>/dev/null || true

# Step 4: Clean up networks (if any custom networks were created)
echo "Cleaning up networks..."
docker network rm otg-test-net 2>/dev/null || true

# Step 5: Verification
echo "Verifying cleanup..."
echo "Running containers:"
docker ps | grep -E "(controller|traffic-engine)" || echo "  None found ✅"

echo "All containers:"
docker ps -a | grep -E "(controller|traffic-engine)" || echo "  None found ✅"

echo "Virtual interfaces:"
ip link show | grep veth || echo "  None found ✅"

echo "Docker networks:"
docker network ls | grep otg || echo "  No custom networks found ✅"

echo "=== Cleanup Complete ==="
