#!/bin/bash
# 記憶維護腳本 - 每週執行（Linux版）
# 整理日常筆記到長期記憶

MEMORY_DIR="$HOME/.openclaw/workspace/memory"
MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"

echo "========================================"
echo "🧠 記憶維護程序"
echo "========================================"
echo ""

# 取得今天的日期
TODAY=$(date '+%Y-%m-%d')
TODAY_FILE="$MEMORY_DIR/$TODAY.md"

echo "📅 今日日期: $TODAY"
echo "📁 記憶檔案: $TODAY_FILE"
echo ""

# 檢查今日記憶檔是否存在
if [ -f "$TODAY_FILE" ]; then
    echo "✅ 今日記憶檔存在"
    echo ""
    echo "📋 今日重要事件："
    grep "^##\|^###" "$TODAY_FILE" | head -10
    echo ""
    echo "📊 今日總結："
    wc -l "$TODAY_FILE"
else
    echo "⚠️ 今日記憶檔不存在: $TODAY_FILE"
fi

# 整理本週記憶
echo ""
echo "📅 本週記憶整理："
ls -lt "$MEMORY_DIR"/2026-04-*.md 2>/dev/null | head -5

# 備份 MEMORY.md
if [ -f "$MEMORY_FILE" ]; then
    BACKUP_DIR="$MEMORY_DIR/backups"
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/MEMORY_$(date '+%Y%m%d').md"
    cp "$MEMORY_FILE" "$BACKUP_FILE"
    echo ""
    echo "✅ MEMORY.md 已備份到: $BACKUP_FILE"
fi

echo ""
echo "========================================"
echo "🧠 記憶維護完成"
echo "========================================"