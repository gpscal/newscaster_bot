#!/bin/bash
# Installation script for Newscaster Bot systemd service

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     🤖 NEWSCASTER BOT - SERVICE INSTALLER               ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run with sudo"
    echo ""
    echo "Usage: sudo ./install-service.sh"
    exit 1
fi

# Get the actual user (not root)
ACTUAL_USER=${SUDO_USER:-$USER}
echo "📝 Installing service for user: $ACTUAL_USER"
echo ""

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p /home/cali/newscaster_bot/logs
chown cali:cali /home/cali/newscaster_bot/logs
echo "   ✅ Logs directory created"
echo ""

# Copy service file to systemd directory
echo "📋 Installing systemd service file..."
cp /home/cali/newscaster_bot/newscaster-bot.service /etc/systemd/system/
echo "   ✅ Service file copied to /etc/systemd/system/"
echo ""

# Reload systemd daemon
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload
echo "   ✅ Daemon reloaded"
echo ""

# Enable service to start on boot
echo "🚀 Enabling service to start on boot..."
systemctl enable newscaster-bot.service
echo "   ✅ Service enabled"
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     ✅ SERVICE INSTALLED SUCCESSFULLY!                  ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Service Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Start the bot:"
echo "   sudo systemctl start newscaster-bot"
echo ""
echo "🛑 Stop the bot:"
echo "   sudo systemctl stop newscaster-bot"
echo ""
echo "🔄 Restart the bot:"
echo "   sudo systemctl restart newscaster-bot"
echo ""
echo "📊 Check status:"
echo "   sudo systemctl status newscaster-bot"
echo ""
echo "📜 View logs (live):"
echo "   sudo journalctl -u newscaster-bot -f"
echo ""
echo "📜 View logs (last 50 lines):"
echo "   sudo journalctl -u newscaster-bot -n 50"
echo ""
echo "📝 View bot output log:"
echo "   tail -f /home/cali/newscaster_bot/logs/bot.log"
echo ""
echo "❌ View error log:"
echo "   tail -f /home/cali/newscaster_bot/logs/bot-error.log"
echo ""
echo "🔧 Disable service (stop auto-start on boot):"
echo "   sudo systemctl disable newscaster-bot"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Next Steps:"
echo "   1. Start the service: sudo systemctl start newscaster-bot"
echo "   2. Check status: sudo systemctl status newscaster-bot"
echo "   3. View logs: tail -f /home/cali/newscaster_bot/logs/bot.log"
echo ""
echo "🎉 The bot will now:"
echo "   ✅ Start automatically on system boot"
echo "   ✅ Restart automatically if it crashes"
echo "   ✅ Run in the background (no SSH session needed)"
echo "   ✅ Log all output to logs/bot.log"
echo ""
