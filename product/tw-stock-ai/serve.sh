#!/bin/bash
# Simple HTTP server for landing page
cd /root/.openclaw/workspace/product/tw-stock-ai
python3 -m http.server 8080 >> /root/.openclaw/workspace/product/tw-stock-ai/www.log 2>&1
