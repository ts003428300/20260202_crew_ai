## Why

本專案目前尚無任何程式碼基礎。需要從零初始化一個基於 CrewAI 框架的多 Agent 辯論系統，讓使用者輸入辯論題目與回合數後，由正方、反方兩位 Agent 交替辯論，最終由裁判 Agent 做出判決。選用 Gemini 3.0 Flash 作為 LLM 以兼顧成本與推理能力。

## What Changes

- 建立專案環境設定：`requirements.txt`、`.env.example`
- 建立 Agent 設定檔 `src/config/agents.yaml`：定義正方 (proponent)、反方 (opponent)、裁判 (judge) 三個角色
- 建立 Task 設定檔 `src/config/tasks.yaml`：定義辯論發言與判決的任務模板
- 建立核心邏輯 `src/main.py`：實作 `DebateCrew` 類別，根據回合數動態生成 Task 列表並交由 Crew 執行

## Capabilities

### New Capabilities
- `debate-core`: 核心辯論引擎 — 涵蓋 Agent 定義、Task 模板、動態回合生成、Crew 組裝與執行的完整流程

### Modified Capabilities
<!-- 無既有 spec，本次為全新建立 -->

## Impact

- **新增檔案**: `requirements.txt`, `.env.example`, `src/config/agents.yaml`, `src/config/tasks.yaml`, `src/main.py`
- **依賴**: crewai, crewai-tools, langchain-google-genai, python-dotenv
- **外部服務**: Google Gemini API (需 `GOOGLE_API_KEY`)
- **語言**: 所有 Agent prompt 與輸出皆為繁體中文
