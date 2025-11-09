#!/bin/bash

# Newscaster Bot Setup Script
# This script helps you set up the bot quickly

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         🤖 NEWSCASTER BOT - SETUP WIZARD                ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file first."
    exit 1
fi

echo "✅ Found .env file"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✅ $python_version"
else
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo ""

# Check if pip is installed
echo "📦 Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 is installed"
else
    echo "❌ pip3 not found. Please install pip."
    exit 1
fi
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Check .env configuration
echo "🔍 Checking .env configuration..."

check_env_var() {
    local var_name=$1
    if grep -q "^${var_name}=.\+$" .env; then
        echo "  ✅ $var_name is set"
        return 0
    else
        echo "  ⚠️  $var_name is NOT set or empty"
        return 1
    fi
}

all_set=true

# Check required variables
check_env_var "OPENROUTER_API_KEY" || all_set=false
check_env_var "OPENROUTER_BASE_URL" || all_set=false
check_env_var "OPENROUTER_MODEL" || all_set=false
check_env_var "NEWS_API_AI" || all_set=false
check_env_var "CRYPTOCOMPARE_API_KEY" || all_set=false
check_env_var "DISCORD_BOT_TOKEN" || all_set=false
check_env_var "DISCORD_CHANNEL_ID" || all_set=false

echo ""

if [ "$all_set" = false ]; then
    echo "⚠️  WARNING: Some environment variables are missing or empty!"
    echo ""
    echo "Please update your .env file with the required values:"
    echo "  - DISCORD_BOT_TOKEN (from Discord Developer Portal)"
    echo "  - DISCORD_CHANNEL_ID (right-click channel in Discord → Copy ID)"
    echo ""
    echo "See DISCORD_SETUP_GUIDE.md for detailed instructions."
    echo ""
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Make main.py executable
chmod +x main.py

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         ✅ SETUP COMPLETE!                              ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 You can now run the bot with:"
echo ""
echo "   Single run:    python3 main.py --mode once"
echo "   Scheduled:     python3 main.py --mode schedule"
echo ""
echo "📖 For Discord setup instructions, see: DISCORD_SETUP_GUIDE.md"
echo ""
