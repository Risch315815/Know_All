# 全知專案 · Know All

> 知識的重點是**體系化**與**應用**。  
> 學習一門知識的第一步應該是建立體系，了解其脈絡；  
> 細節則應該於實際應用的過程中一步步填充。

---

## 網站

**GitHub Pages：** `https://risch315815.github.io/Know_All/`

---

## 結構說明

```
Know_All/
├── index.html          # 主頁：知識地圖總覽
├── template.html       # 新增領域頁面時複製的模板
├── css/
│   └── style.css       # 全站樣式
├── js/
│   └── main.js         # 互動邏輯（領域卡片管理）
├── domains/
│   └── [領域名]/
│       └── index.html  # 該領域的體系骨架與筆記
└── README.md
```

## 新增一個知識領域

1. 在主頁點擊「新增領域」按鈕（只在本地 localStorage 記錄）
2. 複製 `template.html` 到 `domains/[領域slug]/index.html`
3. 按照 `template.html` 內的 `EDIT:` 標記填入內容
4. `git add . && git commit -m "add: [領域名稱]" && git push`

## 部署（GitHub Pages）

1. 前往 repo 的 **Settings → Pages**
2. Source 選擇 `Deploy from a branch`
3. Branch 選 `main`，資料夾選 `/ (root)`
4. 儲存後約 1 分鐘即可在上方網址存取
