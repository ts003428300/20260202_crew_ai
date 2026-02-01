## Context

這是一個全新專案，目前沒有任何程式碼。目標是建立一個基於 CrewAI 框架的多 Agent 辯論系統，使用 Google Gemini 3.0 Flash 作為底層 LLM。系統需支援動態回合數，並以繁體中文進行所有對話與輸出。

專案採用 CrewAI 的 YAML-based 設定模式，將 Agent 與 Task 定義分離至設定檔，核心邏輯集中於 `src/main.py`。

## Goals / Non-Goals

**Goals:**
- 建立可執行的辯論系統：正方 vs 反方，多回合交替，裁判總結
- Agent/Task 定義與程式碼分離（YAML 設定檔）
- 支援使用者自訂題目與回合數
- 所有 prompt 與輸出使用繁體中文

**Non-Goals:**
- Web UI 或 API 介面（本次僅 CLI）
- 多模型切換支援（固定使用 Gemini 3.0 Flash）
- 辯論歷史紀錄持久化
- 單元測試（後續 change 處理）

## Decisions

### 1. 專案結構：扁平化單模組

```
├── .env.example
├── requirements.txt
└── src/
    ├── main.py
    └── config/
        ├── agents.yaml
        └── tasks.yaml
```

**理由**: 專案初期功能單一，不需要 package 化或多模組分層。CrewAI 官方範例也採用類似結構。

**替代方案**: 使用 `crewai create crew` scaffolding — 但會產生過多樣板檔案，不符合最小化需求。

### 2. LLM 初始化：使用 CrewAI 內建 LiteLLM 整合

```python
from crewai import LLM
llm = LLM(model="gemini/gemini-3.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
```

**理由**: CrewAI 內建透過 LiteLLM 支援 Gemini，不需額外安裝 `langchain-google-genai`，但 requirements 仍保留以備未來 tool 使用。

**替代方案**: 直接用 `langchain-google-genai` 的 `ChatGoogleGenerativeAI` — 增加不必要的耦合。

### 3. 動態 Task 生成：Python 迴圈組裝 Task 列表

核心邏輯：

```python
tasks = []
for i in range(round_count):
    tasks.append(create_task(proponent, f"第 {i+1} 回合正方發言", context=tasks[-1:]))
    tasks.append(create_task(opponent, f"第 {i+1} 回合反方反駁", context=tasks[-1:]))
tasks.append(create_task(judge, "裁判總結判決", context=tasks))
```

每個 Task 透過 `context` 參數接收前一個 Task 的輸出，形成鏈式對話。裁判 Task 接收所有先前 Task 作為 context。

**理由**: CrewAI 的 `Process.sequential` 僅支援固定順序。動態生成 Task 列表並傳入 Crew 可實現可變回合數。

**替代方案**: 在 YAML 中硬編碼固定回合數 — 失去彈性。

### 4. Crew 執行模式：Sequential Process

```python
crew = Crew(agents=[proponent, opponent, judge], tasks=tasks, process=Process.sequential)
```

**理由**: 辯論是嚴格順序性的（正方 → 反方 → 正方 → ... → 裁判），不需要並行執行。

### 5. YAML Task 模板設計：通用模板 + 動態描述覆蓋

`tasks.yaml` 定義兩個模板 (`debate_task`, `judge_task`)，程式碼在建立 Task 時動態覆蓋 `description` 欄位以注入回合數與角色資訊。

**理由**: 保持 YAML 簡潔，避免為每個回合定義獨立 task。

## Risks / Trade-offs

- **[Context 長度爆炸]** 回合數過多時，裁判 Task 的 context 會包含所有先前輸出 → 限制建議回合數上限（如 5 回合），並在 README 中說明
- **[API 費用]** 每個 Task 都是一次 LLM 呼叫，N 回合 = 2N+1 次呼叫 → Gemini 3.0 Flash 成本低，可接受
- **[繁體中文品質]** Gemini 的中文輸出品質可能不穩定 → 在 Agent backstory 中強調「必須使用繁體中文回應」
