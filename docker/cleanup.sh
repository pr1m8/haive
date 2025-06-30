#!/bin/bash

# 🧹 NUCLEAR Docker Cleanup Script
# WARNING: This will delete EVERYTHING Docker-related!
# Use when you have 150GB+ of Docker data to clean

echo "🚨 DOCKER NUCLEAR CLEANUP - This will delete EVERYTHING!"
echo "This will remove:"
echo "  - All containers (running and stopped)"
echo "  - All images (including base images)"
echo "  - All volumes"
echo "  - All networks"
echo "  - All build cache"
echo "  - All BuildKit cache"
echo ""

read -p "Are you sure? Type 'YES' to continue: " confirm
if [ "$confirm" != "YES" ]; then
    echo "❌ Cleanup cancelled"
    exit 1
fi

echo "🧹 Starting nuclear cleanup..."

# Step 1: Stop all running containers
echo "1️⃣ Stopping all containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "No containers to stop"

# Step 2: Remove all containers
echo "2️⃣ Removing all containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

# Step 3: Remove all images (including base images)
echo "3️⃣ Removing ALL images..."
docker rmi $(docker images -aq) --force 2>/dev/null || echo "No images to remove"

# Step 4: Remove all volumes
echo "4️⃣ Removing all volumes..."
docker volume rm $(docker volume ls -q) 2>/dev/null || echo "No volumes to remove"

# Step 5: Remove all networks
echo "5️⃣ Removing custom networks..."
docker network rm $(docker network ls -q) 2>/dev/null || echo "No custom networks to remove"

# Step 6: System prune with extreme prejudice
echo "6️⃣ System prune (everything)..."
docker system prune -af --volumes

# Step 7: Builder prune (BuildKit cache)
echo "7️⃣ Removing BuildKit cache..."
docker builder prune -af

# Step 8: Final check
echo "✅ Cleanup complete! New usage:"
docker system df 2>/dev/null || echo "Docker not available"

echo ""
echo "🎉 Docker cleanup finished!"
echo "💾 You should have freed up ~150GB of space!"
echo ""
echo "To restart fresh:"
echo "  ./run.sh up" 