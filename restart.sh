#!/bin/bash

echo "Stopping all processes..."
pkill -9 -f "python bot.py" 2>/dev/null
pkill -9 -f "python scheduler" 2>/dev/null
sleep 2

echo "Starting bot..."
cd ~/projects/FilevskiyBot
source venv/bin/activate

nohup python bot.py > logs/bot.log 2>&1 &
BOT_PID=$!
echo "Bot started: PID $BOT_PID"

nohup python scheduler_runner.py > logs/scheduler.log 2>&1 &
SCHED_PID=$!
echo "Scheduler started: PID $SCHED_PID"

sleep 3

echo ""
echo "=== Status Check ==="
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Bot is running (PID: $BOT_PID)"
else
    echo "❌ Bot failed to start"
    echo "Last 10 lines of bot.log:"
    tail -10 logs/bot.log
fi

if ps -p $SCHED_PID > /dev/null; then
    echo "✅ Scheduler is running (PID: $SCHED_PID)"
else
    echo "❌ Scheduler failed to start"
fi

echo ""
echo "To check logs:"
echo "  tail -f ~/projects/FilevskiyBot/logs/bot.log"
echo "  tail -f ~/projects/FilevskiyBot/logs/scheduler.log"

