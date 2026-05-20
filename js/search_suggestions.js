// 搜尋歷史記錄功能（已停用熱門搜尋按鈕）
const popularSearches = [];

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
    
    const searchArea = document.querySelector('.md-search');
    if (searchArea) {
        searchArea.appendChild(container);
    }
}

document.addEventListener('DOMContentLoaded', renderSearchSuggestions);