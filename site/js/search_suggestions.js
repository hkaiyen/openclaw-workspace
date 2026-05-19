// 熱門搜尋關鍵字 suggestions
const popularSearches = [
    { keyword: "股票", emoji: "📈", count: 48 },
    { keyword: "新聞", emoji: "📰", count: 30 },
    { keyword: "創業", emoji: "💡", count: 25 },
    { keyword: "健康", emoji: "🍎", count: 20 },
    { keyword: "財報", emoji: "💹", count: 15 },
    { keyword: "火鍋", emoji: "🍲", count: 5 },
    { keyword: "心理", emoji: "🧠", count: 8 },
    { keyword: "飲食", emoji: "🥗", count: 6 },
    { keyword: "投資", emoji: "📊", count: 12 }
];

// 儲存搜尋歷史到 localStorage
function saveSearchHistory(keyword) {
    let history = JSON.parse(localStorage.getItem('search_history') || '[]');
    history = history.filter(k => k !== keyword);
    history.unshift(keyword);
    history = history.slice(0, 5);
    localStorage.setItem('search_history', JSON.stringify(history));
}

// 取得搜尋歷史
function getSearchHistory() {
    return JSON.parse(localStorage.getItem('search_history') || '[]');
}

// 渲染搜尋建議
function renderSearchSuggestions() {
    const container = document.createElement('div');
    container.className = 'search-suggestions';
    container.style.cssText = 'display:flex;flex-wrap:wrap;gap:8px;padding:10px 0;';
    
    popularSearches.forEach(item => {
        const btn = document.createElement('button');
        btn.textContent = `${item.emoji} ${item.keyword}`;
        btn.style.cssText = 'padding:5px 12px;border-radius:15px;border:1px solid #0078B8;background:#f0f7ff;cursor:pointer;font-size:13px;';
        btn.onclick = () => {
            const searchBox = document.querySelector('.md-search__input');
            if (searchBox) {
                searchBox.value = item.keyword;
                searchBox.dispatchEvent(new Event('input'));
            }
        };
        container.appendChild(btn);
    });
    
    // 把搜尋建議加到搜尋框旁邊
    const searchArea = document.querySelector('.md-search');
    if (searchArea) {
        searchArea.appendChild(container);
    }
}

// 當頁面載入完成後
document.addEventListener('DOMContentLoaded', renderSearchSuggestions);
