#!/bin/bash

echo "Starting FilevskiyBot..."
docker-compose up -d

echo ""
echo "Bot is running!"
echo "View logs: docker-compose logs -f"
echo "Stop bot: ./stop.sh"

