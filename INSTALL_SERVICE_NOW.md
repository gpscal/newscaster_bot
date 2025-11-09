# 🚀 Install Service - Quick Guide

## Run Your Bot 24/7 in Background!

Follow these 3 simple steps to run your bot as a system service:

---

## 📋 Step-by-Step Installation

### **Step 1: Install the Service**

```bash
cd /home/cali/newscaster_bot
sudo ./install-service.sh
```

**What this does:**
- Creates logs directory
- Installs systemd service file
- Enables auto-start on boot

### **Step 2: Start the Service**

```bash
sudo systemctl start newscaster-bot
```

### **Step 3: Verify It's Running**

```bash
sudo systemctl status newscaster-bot
```

**Expected output:**
```
● newscaster-bot.service - Newscaster Bot
     Loaded: loaded
     Active: active (running) since...
```

**Check the logs:**
```bash
tail -f /home/cali/newscaster_bot/logs/bot.log
```

You should see:
```
🤖 NEWSCASTER BOT INITIALIZING
✅ All components initialized successfully
🎯 Running in SCHEDULED mode
```

---

## ✅ That's It!

Your bot is now:
- ✅ Running in the background
- ✅ Will survive SSH disconnects
- ✅ Will start automatically on reboot
- ✅ Will restart automatically if it crashes
- ✅ Logs everything to `logs/bot.log`

---

## 🎛️ Quick Commands

### **View Live Logs:**
```bash
tail -f /home/cali/newscaster_bot/logs/bot.log
```

### **Stop the Bot:**
```bash
sudo systemctl stop newscaster-bot
```

### **Restart the Bot:**
```bash
sudo systemctl restart newscaster-bot
```

### **Check Health:**
```bash
./check-service.sh
```

---

## 📖 Full Documentation

For detailed information, see: **`SERVICE_GUIDE.md`**

---

## 🐛 Troubleshooting

### **If service won't start:**

1. Check error logs:
   ```bash
   tail -f /home/cali/newscaster_bot/logs/bot-error.log
   ```

2. Check systemd logs:
   ```bash
   sudo journalctl -u newscaster-bot -n 50
   ```

3. Verify .env file exists:
   ```bash
   cat .env
   ```

4. Check virtual environment:
   ```bash
   ls -la venv/
   ```

### **Common fixes:**

**Missing dependencies:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Permission issues:**
```bash
chmod +x main.py
chmod -R 755 /home/cali/newscaster_bot
```

**Service file issues:**
```bash
sudo systemctl daemon-reload
sudo systemctl restart newscaster-bot
```

---

## 🗑️ Uninstall

To remove the service:

```bash
sudo ./uninstall-service.sh
```

---

## 🎉 Enjoy Your 24/7 News Bot!

Your bot will now:
- Fetch news every 6 hours automatically
- Send updates to Discord
- Run forever in the background
- Never stop (even if SSH disconnects)

**Check your Discord channel for news updates!** 📰🤖

---

*For more details, see `SERVICE_GUIDE.md`*
