#!/bin/bash
# Quick service health check script

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     🔍 NEWSCASTER BOT - SERVICE HEALTH CHECK           ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if service exists
if ! systemctl list-unit-files | grep -q newscaster-bot.service; then
    echo "❌ Service is NOT installed"
    echo ""
    echo "💡 To install: sudo ./install-service.sh"
    exit 1
fi

echo "✅ Service is installed"
echo ""

# Check if service is enabled
if systemctl is-enabled --quiet newscaster-bot.service; then
    echo "✅ Service is enabled (will start on boot)"
else
    echo "⚠️  Service is disabled (won't start on boot)"
    echo "   To enable: sudo systemctl enable newscaster-bot"
fi
echo ""

# Check if service is running
if systemctl is-active --quiet newscaster-bot.service; then
    echo "✅ Service is RUNNING"
    echo ""
    
    # Get process info
    PID=$(systemctl show -p MainPID --value newscaster-bot.service)
    UPTIME=$(systemctl show -p ActiveEnterTimestamp --value newscaster-bot.service)
    
    echo "📊 Service Details:"
    echo "   Process ID: $PID"
    echo "   Started: $UPTIME"
    echo ""
else
    echo "❌ Service is NOT running"
    echo ""
    echo "💡 To start: sudo systemctl start newscaster-bot"
    echo "💡 Check logs: tail -f logs/bot-error.log"
    exit 1
fi

# Check log files
echo "📜 Log Files:"
if [ -f "/home/cali/newscaster_bot/logs/bot.log" ]; then
    SIZE=$(du -h /home/cali/newscaster_bot/logs/bot.log | cut -f1)
    LINES=$(wc -l < /home/cali/newscaster_bot/logs/bot.log)
    echo "   ✅ bot.log: $SIZE ($LINES lines)"
else
    echo "   ⚠️  bot.log: Not found"
fi

if [ -f "/home/cali/newscaster_bot/logs/bot-error.log" ]; then
    SIZE=$(du -h /home/cali/newscaster_bot/logs/bot-error.log | cut -f1)
    LINES=$(wc -l < /home/cali/newscaster_bot/logs/bot-error.log)
    echo "   ✅ bot-error.log: $SIZE ($LINES lines)"
else
    echo "   ⚠️  bot-error.log: Not found"
fi
echo ""

# Show recent log entries
echo "📋 Recent Activity (last 10 lines):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -n 10 /home/cali/newscaster_bot/logs/bot.log 2>/dev/null || echo "   No logs yet"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "✅ Service health check complete!"
echo ""
echo "💡 Useful commands:"
echo "   View live logs: tail -f /home/cali/newscaster_bot/logs/bot.log"
echo "   Check status: sudo systemctl status newscaster-bot"
echo "   Restart service: sudo systemctl restart newscaster-bot"
