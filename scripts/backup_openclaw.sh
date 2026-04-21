#!/bin/bash
# 一鍵備份 OpenClaw 所有資料
# 完成後自動發送到 Telegram

BACKUP_DIR="/root/.openclaw/backup"
OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SCRIPTS_DIR="$HOME/.openclaw/workspace/scripts"

# Telegram 設定
TELEGRAM_TOKEN="8704642969:AAERVfjKsxcHExGOfZP9h5412w9Sp1TtABw"
TELEGRAM_CHAT_ID="8779713208"

send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${message}" \
        -d "parse_mode=HTML" > /dev/null 2>&1
}

send_document() {
    local file_path="$1"
    local caption="$2"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendDocument" \
        -F "chat_id=${TELEGRAM_CHAT_ID}" \
        -F "document=@${file_path}" \
        -F "caption=${caption}" > /dev/null 2>&1
}

# 建立備份目錄
mkdir -p "$BACKUP_DIR"

# 時間戳
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="$BACKUP_DIR/openclaw_backup_$TIMESTAMP.tar.gz"

echo "========================================"
echo "📦 OpenClaw 一鍵備份"
echo "========================================"
echo "備份位置: $BACKUP_FILE"
echo ""

# 顯示要備份的內容
echo "📋 備份內容："
echo "  • OpenClaw 主程式設定"
echo "  • 工作區（腳本、日記、記憶）"
echo "  • Google 認證資料"
echo "  • Crontab 排程"
echo "  • Telegram 設定"
echo ""

# 執行備份
echo "🚀 開始備份..."
tar -czf "$BACKUP_FILE" \
    -C "$HOME" \
    .openclaw/workspace/scripts \
    .openclaw/workspace/memory \
    .openclaw/workspace/google_drive \
    .openclaw/workspace/skills \
    .openclaw/workspace/SOUL.md \
    .openclaw/workspace/USER.md \
    .openclaw/workspace/IDENTITY.md \
    .openclaw/workspace/AGENTS.md \
    .openclaw/workspace/MEMORY.md \
    .openclaw/workspace/TOOLS.md \
    .openclaw/openclaw.json \
    2>/dev/null

# 匯出 crontab
crontab -l > "$BACKUP_DIR/openclaw_crontab_$TIMESTAMP.txt" 2>/dev/null

# 顯示完成資訊
SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
BACKUP_TIME=$(date '+%Y年%m月%d日 %H:%M')

echo ""
echo "========================================"
echo "✅ 備份完成！"
echo "========================================"
echo "備份檔: $BACKUP_FILE"
echo "大小: $SIZE"
echo ""

# 發送到 Telegram
echo "📤 發送到 Telegram..."
CAPTION="📦 OpenClaw 備份_${BACKUP_TIME}

💾 大小: $SIZE
📁 包含: 腳本、記憶、Google設定、排程"

if send_document "$BACKUP_FILE" "$CAPTION"; then
    echo "✅ 已發送到 Telegram"
else
    echo "⚠️ Telegram 發送失敗"
fi

echo ""
echo "========================================"
echo "✅ 備份完成！"
echo "========================================"
