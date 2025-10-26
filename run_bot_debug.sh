#!/bin/bash

cd ~/projects/FilevskiyBot
source venv/bin/activate

echo "Starting bot in debug mode..."
python -u bot.py 2>&1 | tee logs/bot_debug.log

