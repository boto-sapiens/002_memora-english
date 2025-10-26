#!/bin/bash

echo "Starting FilevskiyBot locally..."

# Activate virtual environment
source venv/bin/activate

# Start bot in background
echo "Starting bot..."
nohup python bot.py > logs/bot.log 2>&1 &
BOT_PID=$!
echo "Bot started with PID: $BOT_PID"

# Start scheduler in background
echo "Starting scheduler..."
nohup python scheduler_runner.py > logs/scheduler.log 2>&1 &
SCHEDULER_PID=$!
echo "Scheduler started with PID: $SCHEDULER_PID"

# Save PIDs
echo $BOT_PID > .bot.pid
echo $SCHEDULER_PID > .scheduler.pid

echo ""
echo "✅ FilevskiyBot started!"
echo ""
echo "View logs:"
echo "  Bot:       tail -f logs/bot.log"
echo "  Scheduler: tail -f logs/scheduler.log"
echo ""
echo "Stop: ./stop_local.sh"

