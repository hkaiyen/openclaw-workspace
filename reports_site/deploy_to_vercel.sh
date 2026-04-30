#!/bin/bash

# ==============================================
# 川寶每日報告 - 自動部署到 Vercel 腳本
# ==============================================
# 用途：將 reports 目錄下的報告自動部署到 Vercel
# 使用方式：./deploy_to_vercel.sh
# ==============================================

set -e

echo "=============================================="
echo "川寶每日報告 - 自動部署腳本"
echo "=============================================="
echo ""

# 進入網站目錄
cd ~/.openclaw/workspace/reports_site

# 檢查目錄是否存在
if [ ! -d "docs" ]; then
    echo "❌ 錯誤：找不到 docs 目錄"
    exit 1
fi

echo "📁 檢查目錄結構..."
echo ""

# 顯示目錄結構
echo "📂 目前目錄結構："
find . -type f -name "*.md" -o -name "*.yml" | sort
echo ""

# 檢查是否有 reports 目錄
if [ ! -d "docs/reports" ]; then
    echo "⚠️  警告：找不到 docs/reports 目錄，將建立..."
    mkdir -p docs/reports
fi

# 建立 MkDocs 靜態網站
echo "🔨 正在建立靜態網站..."
mkdocs build

if [ $? -eq 0 ]; then
    echo "✅ 靜態網站建立成功！"
else
    echo "❌ 錯誤：靜態網站建立失敗"
    exit 1
fi

echo ""
echo "📦 即將部署到 Vercel..."
echo ""

# 檢查 Vercel CLI 是否已安裝
if ! command -g vercel &> /dev/null; then
    echo "⚠️  Vercel CLI 未安裝，正在安裝..."
    npm install -g vercel
fi

# 部署到 Vercel
echo "🚀 正在部署到 Vercel..."
cd site

vercel --prod --yes

echo ""
echo "=============================================="
echo "✅ 部署完成！"
echo "=============================================="
echo ""
echo "📌 注意事項："
echo "   1. 首次部署需要登入 Vercel 帳號"
echo "   2. 部署成功後會提供網址"
echo "   3. 未來只需執行此腳本即可自動更新"
echo ""
echo "💡 如需手動部署，請提供 Google 帳號給小安設定"
echo "=============================================="
