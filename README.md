# CrewAI 辯論系統

基於 CrewAI 框架的多 Agent 辯論系統。正方與反方 Agent 針對使用者指定的題目進行多回合辯論，最終由裁判 Agent 做出判決。

## 架構

```
正方 (Proponent) ──→ 反方 (Opponent) ──→ ... ──→ 裁判 (Judge)
     第1回合              第1回合           第N回合      總結判決
```

- **正方**：邏輯清晰、立場堅定，主動提出論點
- **反方**：批判性強，針對正方觀點找漏洞並反駁
- **裁判**：絕對中立，分析雙方攻防後給出勝負與理由

## 技術堆疊

- [CrewAI](https://github.com/crewAIInc/crewAI) — 多 Agent 編排框架
- Google Gemini 3 Flash Preview — LLM
- Python 3.10+

## 快速開始

```bash
# 1. 安裝依賴
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. 設定環境變數
cp .env.example .env
# 編輯 .env，填入你的 GOOGLE_API_KEY

# 3. 執行
python src/main.py
```

系統會提示你輸入辯論題目與回合數，然後自動進行辯論。

## 專案結構

```
├── .env.example              # 環境變數範本
├── requirements.txt          # Python 依賴
├── src/
│   ├── main.py               # 核心邏輯 (DebateCrew)
│   └── config/
│       ├── agents.yaml       # Agent 角色定義
│       └── tasks.yaml        # Task 模板
└── openspec/                 # 變更規格文件
```

## 運作方式

1. 使用者輸入辯論題目與回合數 N
2. 系統動態生成 2N+1 個 Task（每回合正方→反方，最後裁判）
3. 每個 Task 透過 context 接收前一個 Task 的輸出，形成連貫對話
4. 裁判接收所有辯論內容，產出完整判決書
