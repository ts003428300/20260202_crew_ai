## ADDED Requirements

### Requirement: 專案環境設定
系統 SHALL 提供 `requirements.txt` 包含 `crewai`, `crewai-tools`, `langchain-google-genai`, `python-dotenv` 依賴。系統 SHALL 提供 `.env.example` 列出 `GOOGLE_API_KEY` 和 `MODEL=gemini/gemini-3.0-flash` 環境變數範本。

#### Scenario: 安裝依賴
- **WHEN** 使用者執行 `pip install -r requirements.txt`
- **THEN** 所有必要套件（crewai, crewai-tools, langchain-google-genai, python-dotenv）SHALL 被成功安裝

#### Scenario: 環境變數範本
- **WHEN** 使用者查看 `.env.example`
- **THEN** 檔案 SHALL 包含 `GOOGLE_API_KEY` 和 `MODEL=gemini/gemini-3.0-flash` 兩個條目

### Requirement: Agent 定義設定檔
系統 SHALL 在 `src/config/agents.yaml` 中定義三個 Agent：`proponent`（正方）、`opponent`（反方）、`judge`（裁判）。每個 Agent MUST 包含 `role`、`goal`、`backstory` 欄位，且所有內容 MUST 以繁體中文撰寫。

#### Scenario: 正方 Agent 定義
- **WHEN** 系統載入 `src/config/agents.yaml`
- **THEN** SHALL 存在 `proponent` Agent，其 role、goal、backstory 皆為繁體中文，角色定位為邏輯清晰、立場堅定的正方辯手

#### Scenario: 反方 Agent 定義
- **WHEN** 系統載入 `src/config/agents.yaml`
- **THEN** SHALL 存在 `opponent` Agent，其 role、goal、backstory 皆為繁體中文，角色定位為批判性強、專找漏洞的反方辯手

#### Scenario: 裁判 Agent 定義
- **WHEN** 系統載入 `src/config/agents.yaml`
- **THEN** SHALL 存在 `judge` Agent，其 role、goal、backstory 皆為繁體中文，角色定位為絕對中立、分析雙方攻防的裁判

### Requirement: Task 模板設定檔
系統 SHALL 在 `src/config/tasks.yaml` 中定義 `debate_task`（辯論發言）和 `judge_task`（判決）兩個 Task 模板。每個模板 MUST 包含 `description` 和 `expected_output` 欄位。

#### Scenario: 辯論 Task 模板
- **WHEN** 系統載入 `src/config/tasks.yaml`
- **THEN** SHALL 存在 `debate_task` 模板，包含以繁體中文撰寫的 description（含 `{topic}` 和 `{round}` 插值變數）和 expected_output

#### Scenario: 判決 Task 模板
- **WHEN** 系統載入 `src/config/tasks.yaml`
- **THEN** SHALL 存在 `judge_task` 模板，包含以繁體中文撰寫的 description（含 `{topic}` 插值變數）和 expected_output

### Requirement: LLM 配置
系統 MUST 使用 Gemini 3.0 Flash（`gemini/gemini-3.0-flash`）作為所有 Agent 的 LLM。API Key SHALL 從環境變數 `GOOGLE_API_KEY` 讀取。

#### Scenario: LLM 初始化
- **WHEN** `DebateCrew` 類別被實例化
- **THEN** SHALL 建立一個使用 `gemini/gemini-3.0-flash` 模型的 LLM 實例，api_key 來自 `GOOGLE_API_KEY` 環境變數

#### Scenario: 缺少 API Key
- **WHEN** 環境變數 `GOOGLE_API_KEY` 未設定
- **THEN** 系統 SHALL 在啟動時拋出明確錯誤訊息

### Requirement: 動態回合 Task 生成
`DebateCrew` 類別 SHALL 接受 `topic`（辯論題目）與 `round_count`（回合數）作為輸入。系統 MUST 根據 `round_count` 動態生成 Task 列表，順序為：正方發言 → 反方反駁 → （重複 N 次）→ 裁判總結。

#### Scenario: 單回合辯論
- **WHEN** 使用者輸入 topic="AI 是否會取代人類" 且 round_count=1
- **THEN** 系統 SHALL 生成 3 個 Task：[正方第1回合, 反方第1回合, 裁判判決]

#### Scenario: 多回合辯論
- **WHEN** 使用者輸入 topic="核能發電應否廢除" 且 round_count=3
- **THEN** 系統 SHALL 生成 7 個 Task：[正方第1回合, 反方第1回合, 正方第2回合, 反方第2回合, 正方第3回合, 反方第3回合, 裁判判決]

#### Scenario: Task 上下文串接
- **WHEN** 動態生成 Task 列表時
- **THEN** 每個辯論 Task SHALL 接收前一個 Task 的輸出作為 context，裁判 Task SHALL 接收所有先前 Task 作為 context

### Requirement: Crew 組裝與執行
系統 SHALL 將動態生成的 Task 列表與三個 Agent 組裝為一個 Crew，使用 sequential process 模式執行，並回傳完整的辯論結果。

#### Scenario: 正常執行
- **WHEN** 使用者提供有效的 topic 和 round_count 並執行 `DebateCrew`
- **THEN** Crew SHALL 依序執行所有 Task，每個 Agent 的輸出 MUST 為繁體中文，最終回傳包含所有辯論內容與裁判判決的結果

#### Scenario: CLI 入口
- **WHEN** 使用者執行 `python src/main.py`
- **THEN** 系統 SHALL 提示使用者輸入辯論題目與回合數，並啟動辯論流程
