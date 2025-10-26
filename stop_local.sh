#!/bin/bash

echo "Stopping FilevskiyBot..."

# Kill bot
if [ -f .bot.pid ]; then
    BOT_PID=$(cat .bot.pid)
    if kill -0 $BOT_PID 2>/dev/null; then
        kill $BOT_PID
        echo "Bot stopped (PID: $BOT_PID)"
    fi
    rm .bot.pid
fi

# Kill scheduler
if [ -f .scheduler.pid ]; then
    SCHEDULER_PID=$(cat .scheduler.pid)
    if kill -0 $SCHEDULER_PID 2>/dev/null; then
        kill $SCHEDULER_PID
        echo "Scheduler stopped (PID: $SCHEDULER_PID)"
    fi
    rm .scheduler.pid
fi

# Fallback: kill by name
pkill -f "python bot.py"
pkill -f "python scheduler_runner.py"

echo "✅ FilevskiyBot stopped!"

