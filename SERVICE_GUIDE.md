# 🚀 Newscaster Bot - Systemd Service Guide

## Run Your Bot as a Background Service!

This guide shows you how to run your bot as a **systemd service** so it:
- ✅ Runs in the background (no SSH session needed)
- ✅ Starts automatically on system boot
- ✅ Restarts automatically if it crashes
- ✅ Logs all output to files
- ✅ Can be controlled with systemd commands

---

## 📋 Quick Installation

### **Step 1: Install the Service**

```bash
cd /home/cali/newscaster_bot
sudo ./install-service.sh
```

### **Step 2: Start the Service**

```bash
sudo systemctl start newscaster-bot
```

### **Step 3: Check Status**

```bash
sudo systemctl status newscaster-bot
```

You should see:
```
● newscaster-bot.service - Newscaster Bot - News aggregation and analysis bot
     Loaded: loaded (/etc/systemd/system/newscaster-bot.service; enabled)
     Active: active (running) since...
```

**That's it!** Your bot is now running as a service! 🎉

---

## 🎛️ Service Control Commands

### **Start the Bot**
```bash
sudo systemctl start newscaster-bot
```

### **Stop the Bot**
```bash
sudo systemctl stop newscaster-bot
```

### **Restart the Bot**
```bash
sudo systemctl restart newscaster-bot
```

### **Check Status**
```bash
sudo systemctl status newscaster-bot
```

### **Enable Auto-Start on Boot** (already done by installer)
```bash
sudo systemctl enable newscaster-bot
```

### **Disable Auto-Start on Boot**
```bash
sudo systemctl disable newscaster-bot
```

---

## 📜 Viewing Logs

### **Method 1: Bot Log Files** (Recommended)

**Live output log:**
```bash
tail -f /home/cali/newscaster_bot/logs/bot.log
```

**Error log:**
```bash
tail -f /home/cali/newscaster_bot/logs/bot-error.log
```

**Last 100 lines:**
```bash
tail -n 100 /home/cali/newscaster_bot/logs/bot.log
```

### **Method 2: Systemd Journal**

**Live logs:**
```bash
sudo journalctl -u newscaster-bot -f
```

**Last 50 lines:**
```bash
sudo journalctl -u newscaster-bot -n 50
```

**Logs from today:**
```bash
sudo journalctl -u newscaster-bot --since today
```

**Logs from last hour:**
```bash
sudo journalctl -u newscaster-bot --since "1 hour ago"
```

---

## 📂 File Locations

### **Service File:**
```
/etc/systemd/system/newscaster-bot.service
```

### **Log Files:**
```
/home/cali/newscaster_bot/logs/bot.log          # Standard output
/home/cali/newscaster_bot/logs/bot-error.log    # Errors only
```

### **Bot Files:**
```
/home/cali/newscaster_bot/                      # Bot directory
```

---

## 🔧 Service Configuration

The service is configured in `newscaster-bot.service`:

```ini
[Unit]
Description=Newscaster Bot - News aggregation and analysis bot
After=network-online.target

[Service]
Type=simple
User=cali
WorkingDirectory=/home/cali/newscaster_bot
ExecStart=/home/cali/newscaster_bot/venv/bin/python main.py --mode schedule

# Auto-restart on failure
Restart=on-failure
RestartSec=10

# Logging
StandardOutput=append:/home/cali/newscaster_bot/logs/bot.log
StandardError=append:/home/cali/newscaster_bot/logs/bot-error.log

[Install]
WantedBy=multi-user.target
```

### **Key Features:**
- **User**: Runs as user `cali` (not root)
- **Auto-Restart**: Restarts if crashes (waits 10 seconds)
- **Logging**: Separate logs for output and errors
- **Start on Boot**: Enabled by default

---

## 🔄 Updating the Bot

### **When you update bot code:**

1. **Stop the service:**
   ```bash
   sudo systemctl stop newscaster-bot
   ```

2. **Make your changes** (edit Python files, update .env, etc.)

3. **Restart the service:**
   ```bash
   sudo systemctl start newscaster-bot
   ```

**Or use restart to do both:**
```bash
sudo systemctl restart newscaster-bot
```

### **After updating service file:**

If you edit `newscaster-bot.service`:

```bash
sudo cp newscaster-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart newscaster-bot
```

---

## 🗑️ Uninstalling the Service

To remove the service:

```bash
cd /home/cali/newscaster_bot
sudo ./uninstall-service.sh
```

This will:
- Stop the service
- Disable auto-start
- Remove service file
- Reload systemd

**Note:** Logs in `logs/` directory are kept.

---

## 🧪 Testing the Service

### **Test 1: Start and Check Status**
```bash
sudo systemctl start newscaster-bot
sudo systemctl status newscaster-bot
```

Expected: `Active: active (running)`

### **Test 2: View Live Logs**
```bash
tail -f /home/cali/newscaster_bot/logs/bot.log
```

You should see:
```
🤖 NEWSCASTER BOT INITIALIZING
✅ All components initialized successfully
🎯 Running in SCHEDULED mode
```

### **Test 3: Check Discord**

Within a few minutes, check your Discord channel for news updates!

### **Test 4: Auto-Restart Test**

Kill the bot process:
```bash
# Find process ID
sudo systemctl status newscaster-bot | grep PID

# The service will automatically restart within 10 seconds!
```

Check status again - should be running!

---

## 🐛 Troubleshooting

### **Service won't start**

**Check logs:**
```bash
sudo journalctl -u newscaster-bot -n 50
tail -n 50 /home/cali/newscaster_bot/logs/bot-error.log
```

**Common issues:**
1. **Missing .env file** - Check `/home/cali/newscaster_bot/.env` exists
2. **Wrong permissions** - Run `chmod +x main.py`
3. **Virtual env missing** - Run `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`

### **Service is running but not posting to Discord**

**Check the logs:**
```bash
tail -f /home/cali/newscaster_bot/logs/bot.log
```

**Look for:**
- Discord connection status
- Error messages
- API key issues

**Common fixes:**
1. Check `DISCORD_BOT_TOKEN` in `.env`
2. Check `DISCORD_CHANNEL_ID` in `.env`
3. Verify bot has permissions in Discord channel

### **Service keeps restarting**

**Check error log:**
```bash
tail -f /home/cali/newscaster_bot/logs/bot-error.log
```

**Common causes:**
- Invalid API keys
- Network issues
- Python errors

### **Can't see logs**

**Create logs directory:**
```bash
mkdir -p /home/cali/newscaster_bot/logs
chmod 755 /home/cali/newscaster_bot/logs
```

**Then restart:**
```bash
sudo systemctl restart newscaster-bot
```

---

## 📊 Service Status Explained

### **Active (running)** ✅
```
Active: active (running) since Fri 2025-11-08 19:30:00 UTC; 5min ago
```
**Meaning:** Bot is running normally

### **Failed** ❌
```
Active: failed (Result: exit-code) since Fri 2025-11-08 19:30:00 UTC; 5min ago
```
**Meaning:** Bot crashed or exited with error. Check logs!

### **Inactive (dead)** ⏸️
```
Active: inactive (dead)
```
**Meaning:** Service stopped. Start with `sudo systemctl start newscaster-bot`

---

## 💡 Pro Tips

### **Tip 1: Create Log Rotation**

Prevent logs from growing too large:

```bash
sudo nano /etc/logrotate.d/newscaster-bot
```

Add:
```
/home/cali/newscaster_bot/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### **Tip 2: Create Aliases**

Add to `~/.bashrc`:
```bash
alias nbstart='sudo systemctl start newscaster-bot'
alias nbstop='sudo systemctl stop newscaster-bot'
alias nbstatus='sudo systemctl status newscaster-bot'
alias nblogs='tail -f /home/cali/newscaster_bot/logs/bot.log'
alias nberrors='tail -f /home/cali/newscaster_bot/logs/bot-error.log'
```

Then use:
```bash
nbstart    # Start bot
nbstatus   # Check status
nblogs     # View logs
```

### **Tip 3: Monitor Bot Health**

Create a monitoring script:
```bash
#!/bin/bash
# Check if bot is running and restart if needed
if ! systemctl is-active --quiet newscaster-bot; then
    echo "Bot is down! Restarting..."
    sudo systemctl start newscaster-bot
fi
```

Add to crontab to check every 5 minutes:
```bash
*/5 * * * * /path/to/monitor-bot.sh
```

---

## 🎉 Benefits of Running as Service

### **vs Running in Terminal:**

| Feature | Terminal | Service |
|---------|----------|---------|
| **Survives SSH disconnect** | ❌ No | ✅ Yes |
| **Starts on boot** | ❌ No | ✅ Yes |
| **Auto-restart on crash** | ❌ No | ✅ Yes |
| **Background execution** | ❌ No | ✅ Yes |
| **Centralized logs** | ❌ No | ✅ Yes |
| **System integration** | ❌ No | ✅ Yes |

---

## 📋 Quick Reference

### **Essential Commands:**
```bash
# Service control
sudo systemctl start newscaster-bot      # Start
sudo systemctl stop newscaster-bot       # Stop
sudo systemctl restart newscaster-bot    # Restart
sudo systemctl status newscaster-bot     # Status

# Logs
tail -f logs/bot.log                     # Live output
tail -f logs/bot-error.log               # Live errors
sudo journalctl -u newscaster-bot -f     # Systemd logs

# Service management
sudo systemctl enable newscaster-bot     # Auto-start on boot
sudo systemctl disable newscaster-bot    # Don't auto-start
sudo systemctl daemon-reload             # Reload config
```

---

## 🚀 You're All Set!

Your Newscaster Bot is now running as a professional system service!

- ✅ **Always running** in the background
- ✅ **Survives reboots** and SSH disconnects
- ✅ **Auto-restarts** if it crashes
- ✅ **Easy to manage** with systemctl commands
- ✅ **Logs everything** for debugging

**Enjoy your automated news updates!** 📰🤖

---

*Service Name: `newscaster-bot.service`*
*Service User: `cali`*
*Log Location: `/home/cali/newscaster_bot/logs/`*
