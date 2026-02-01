import os
from pathlib import Path

import yaml
from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = Path(__file__).parent / "config"


def load_yaml(filename: str) -> dict:
    with open(CONFIG_DIR / filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class DebateCrew:
    def __init__(self, topic: str, round_count: int):
        self.topic = topic
        self.round_count = round_count

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("環境變數 GOOGLE_API_KEY 未設定，請在 .env 檔案中設定。")

        self.llm = LLM(model="gemini/gemini-3-flash-preview", api_key=api_key)

        agents_config = load_yaml("agents.yaml")
        tasks_config = load_yaml("tasks.yaml")

        self.proponent = Agent(
            role=agents_config["proponent"]["role"],
            goal=agents_config["proponent"]["goal"],
            backstory=agents_config["proponent"]["backstory"],
            llm=self.llm,
            verbose=True,
        )
        self.opponent = Agent(
            role=agents_config["opponent"]["role"],
            goal=agents_config["opponent"]["goal"],
            backstory=agents_config["opponent"]["backstory"],
            llm=self.llm,
            verbose=True,
        )
        self.judge = Agent(
            role=agents_config["judge"]["role"],
            goal=agents_config["judge"]["goal"],
            backstory=agents_config["judge"]["backstory"],
            llm=self.llm,
            verbose=True,
        )

        self.debate_template = tasks_config["debate_task"]
        self.judge_template = tasks_config["judge_task"]

    def _build_tasks(self) -> list[Task]:
        tasks: list[Task] = []

        for i in range(1, self.round_count + 1):
            # 正方發言
            proponent_task = Task(
                description=self.debate_template["description"].format(
                    topic=self.topic, round=i
                ),
                expected_output=self.debate_template["expected_output"],
                agent=self.proponent,
                context=tasks[-1:] if tasks else [],
            )
            tasks.append(proponent_task)

            # 反方反駁
            opponent_task = Task(
                description=self.debate_template["description"].format(
                    topic=self.topic, round=i
                ),
                expected_output=self.debate_template["expected_output"],
                agent=self.opponent,
                context=[proponent_task],
            )
            tasks.append(opponent_task)

        # 裁判總結
        judge_task = Task(
            description=self.judge_template["description"].format(topic=self.topic),
            expected_output=self.judge_template["expected_output"],
            agent=self.judge,
            context=tasks,
        )
        tasks.append(judge_task)

        return tasks

    def run(self):
        tasks = self._build_tasks()
        crew = Crew(
            agents=[self.proponent, self.opponent, self.judge],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        return crew.kickoff()


if __name__ == "__main__":
    topic = input("請輸入辯論題目：").strip()
    rounds = int(input("請輸入辯論回合數：").strip())
    debate = DebateCrew(topic=topic, round_count=rounds)
    result = debate.run()
    print("\n" + "=" * 60)
    print("辯論結果")
    print("=" * 60)
    print(result)
