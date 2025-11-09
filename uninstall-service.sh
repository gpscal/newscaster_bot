#!/bin/bash
# Uninstallation script for Newscaster Bot systemd service

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     🗑️  NEWSCASTER BOT - SERVICE UNINSTALLER            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run with sudo"
    echo ""
    echo "Usage: sudo ./uninstall-service.sh"
    exit 1
fi

# Stop the service if running
echo "🛑 Stopping service..."
systemctl stop newscaster-bot.service 2>/dev/null || echo "   ℹ️  Service was not running"
echo ""

# Disable the service
echo "🔧 Disabling service..."
systemctl disable newscaster-bot.service 2>/dev/null || echo "   ℹ️  Service was not enabled"
echo ""

# Remove service file
echo "🗑️  Removing service file..."
rm -f /etc/systemd/system/newscaster-bot.service
echo "   ✅ Service file removed"
echo ""

# Reload systemd daemon
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload
echo "   ✅ Daemon reloaded"
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     ✅ SERVICE UNINSTALLED SUCCESSFULLY!                ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "ℹ️  Note: Log files are kept in /home/cali/newscaster_bot/logs/"
echo "   You can delete them manually if desired."
echo ""
