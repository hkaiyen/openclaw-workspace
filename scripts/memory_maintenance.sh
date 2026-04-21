#!/bin/bash
# 記憶維護腳本 - 每週執行
# 整理日常筆記到長期記憶

MEMORY_DIR="$HOME/.openclaw/workspace/memory"
MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"

echo "========================================"
echo "🧠 記憶維護程序"
echo "========================================"
echo ""

# 取得上週的日期
LAST_WEEK_DATE=$(date -v-7d '+%Y-%m-%d')
echo "📅 整理上週筆記: $LAST_WEEK_DATE"

# 讀取上週的記憶檔
WEEKLY_FILE="$MEMORY_DIR/$LAST_WEEK_DATE.md"
if [ -f "$WEEKLY_FILE" ]; then
    echo "✅ 找到上週檔案"
    echo ""
    echo "📋 重要事件摘要："
    grep "^##\|^###" "$WEEKLY_FILE" | head -10
    echo ""
    echo "📝 完整內容："
    cat "$WEEKLY_FILE" | head -50
else
    echo "⚠️ 未找到上週檔案: $WEEKLY_FILE"
fi

echo ""
echo "========================================"
echo "🧠 記憶維護完成"
echo "========================================"