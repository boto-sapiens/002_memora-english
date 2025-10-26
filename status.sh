#!/bin/bash

echo "=== FilevskiyBot Status ==="
echo ""

# Check bot
if pgrep -f "python bot.py" > /dev/null; then
    BOT_PID=$(pgrep -f "python bot.py")
    echo "✅ Bot:       Running (PID: $BOT_PID)"
else
    echo "❌ Bot:       Not running"
fi

# Check scheduler
if pgrep -f "python scheduler_runner.py" > /dev/null; then
    SCHEDULER_PID=$(pgrep -f "python scheduler_runner.py")
    echo "✅ Scheduler: Running (PID: $SCHEDULER_PID)"
else
    echo "❌ Scheduler: Not running"
fi

echo ""
echo "=== Data Status ==="
if [ -f data/users.json ]; then
    USERS=$(cat data/users.json | grep -o '"[0-9]*"' | wc -l)
    echo "📊 Users: $USERS"
    echo ""
    echo "Users data:"
    cat data/users.json | head -20
else
    echo "❌ No data/users.json found"
fi

echo ""
echo "=== Recent Logs ==="
if [ -f logs/bot.log ]; then
    echo "Last 5 lines from bot.log:"
    tail -5 logs/bot.log
else
    echo "No logs/bot.log"
fi

