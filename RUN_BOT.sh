#!/bin/bash
# Quick script to run the Newscaster Bot

cd /home/cali/newscaster_bot
source venv/bin/activate

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         🤖 STARTING NEWSCASTER BOT                      ║"
echo "║                                                          ║"
echo "║  LLM: ROUTELLM (DeepSeek v3.1)                          ║"
echo "║  Topics: Interstellar Objects & Crypto Markets          ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Choose mode:"
echo "  1) Run once (immediate update, then listen for commands)"
echo "  2) Scheduled (updates every 6 hours)"
echo "  3) Exit"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Running in SINGLE-RUN mode..."
        echo "💡 The bot will fetch news now and stay online for commands"
        echo "💡 Press Ctrl+C to stop"
        echo ""
        python main.py --mode once
        ;;
    2)
        echo ""
        echo "⏰ Running in SCHEDULED mode..."
        echo "💡 Bot will update every 6 hours automatically"
        echo "💡 Press Ctrl+C to stop"
        echo ""
        python main.py --mode schedule
        ;;
    3)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run again."
        exit 1
        ;;
esac
