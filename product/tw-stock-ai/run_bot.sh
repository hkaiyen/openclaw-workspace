#!/bin/bash
cd /root/.openclaw/workspace/product/tw-stock-ai
exec python3 bot.py >> bot_stdout.log 2>&1
