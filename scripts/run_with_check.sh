#!/bin/bash
# 任務管理器包裝腳本
# 用法: run_with_check.sh <task_key> <script_path>

SCRIPTS_DIR="/Users/hsuehkaiyen/.openclaw/workspace/scripts"
LOGS_DIR="/Users/hsuehkaiyen/.openclaw/workspace/logs"

TASK_KEY="$1"
SCRIPT="$2"
TODAY=$(date '+%Y-%m-%d')

# 任務定義（按執行順序）
case "$TASK_KEY" in
    "morning")
        # 04:45 - 股市早盤，前面無任務
        ;;
    "news")
        # 06:00 - 新聞，前面檢查股市
        if ! grep -q "$TODAY" "$LOGS_DIR/daily_market_report.log" 2>/dev/null; then
            echo "⚠️ 發現股市早盤未執行，先執行..."
            python3 "$SCRIPTS_DIR/daily_market_report.py"
        fi
        ;;
    "briefing")
        # 07:30 - 簡報，檢查新聞和股市
        if ! grep -q "$TODAY" "$LOGS_DIR/daily_news_report.log" 2>/dev/null; then
            echo "⚠️ 發現新聞快報未執行，先執行..."
            python3 "$SCRIPTS_DIR/daily_news_report.py"
        fi
        if ! grep -q "$TODAY" "$LOGS_DIR/daily_market_report.log" 2>/dev/null; then
            echo "⚠️ 發現股市早盤未執行，先執行..."
            python3 "$SCRIPTS_DIR/daily_market_report.py"
        fi
        ;;
    "briefing_google")
        # 08:00 - Google簡報，檢查前面所有
        if ! grep -q "$TODAY" "$LOGS_DIR/daily_briefing_apple.log" 2>/dev/null; then
            echo "⚠️ 發現Apple簡報未執行，先執行..."
            python3 "$SCRIPTS_DIR/daily_briefing_apple.py"
        fi
        ;;
    "afternoon")
        # 13:40 - 股市午盤
        ;;
    "middle_east")
        # 中東局勢，追蹤12/18/00
        ;;
esac

# 執行主要任務
python3 "$SCRIPT"
