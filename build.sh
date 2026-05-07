#!/bin/bash
set -e
mkdir -p site
cp /root/.openclaw/reports/daily/全方位新聞快報_20260507_1507.html site/index.html
echo "Build complete"
