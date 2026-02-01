## 1. 環境設定

- [x] 1.1 建立 `requirements.txt`，包含 crewai, crewai-tools, langchain-google-genai, python-dotenv
- [x] 1.2 建立 `.env.example`，列出 GOOGLE_API_KEY 和 MODEL=gemini/gemini-3.0-flash

## 2. Agent 設定檔

- [x] 2.1 建立 `src/config/agents.yaml`，定義 proponent（正方）Agent：role、goal、backstory 以繁體中文撰寫
- [x] 2.2 在同一檔案中定義 opponent（反方）Agent：role、goal、backstory 以繁體中文撰寫
- [x] 2.3 在同一檔案中定義 judge（裁判）Agent：role、goal、backstory 以繁體中文撰寫

## 3. Task 設定檔

- [x] 3.1 建立 `src/config/tasks.yaml`，定義 debate_task 模板（含 {topic}、{round} 插值變數、description、expected_output）
- [x] 3.2 在同一檔案中定義 judge_task 模板（含 {topic} 插值變數、description、expected_output）

## 4. 核心邏輯

- [x] 4.1 建立 `src/main.py`，實作 LLM 初始化（gemini/gemini-3.0-flash，從環境變數讀取 API Key）
- [x] 4.2 實作 YAML 設定檔載入函式（讀取 agents.yaml 和 tasks.yaml）
- [x] 4.3 實作 DebateCrew 類別：接受 topic 和 round_count 參數
- [x] 4.4 實作動態 Task 生成迴圈：根據 round_count 建立正方/反方交替 Task 列表，每個 Task 透過 context 串接前一個 Task
- [x] 4.5 實作裁判 Task 生成：接收所有先前 Task 作為 context
- [x] 4.6 實作 Crew 組裝：將 agents 與動態 tasks 組裝為 Crew（sequential process）
- [x] 4.7 實作 CLI 入口（`if __name__ == "__main__"`）：提示使用者輸入辯論題目與回合數，呼叫 DebateCrew 執行
