#!/bin/bash
echo "STARTING IN DEV MODE"

if [ ! -f .env ]; then
    echo "unable to locate .env, run /scripts/setup-env.sh first"
else
    free_port(){
        port=$1
        container_id=$(docker ps -q --filter "publish=$port")

        if [ -n "$container_id" ]; then
            echo "Releasing port $port (used by container $container_id).."
            docker stop "$container_id" >/dev/null 2>&1
            docker rm "$container_id" >/dev/null 2>&1
        fi
    }

    echo "🧹 Cleaning up ports..."
    free_port 5432
    free_port 7000


    echo "🛑 Stopping existing containers..."
    docker compose down

    echo "🏗️  Building and starting development containers..."

    if docker compose up --build; then
        echo "✨ Development environment ready!"
        echo "📊 Database: localhost:5432"
    else
        echo "❌ Failed to start containers"
    fi
fi