# BEGIN crew.py
# --- patch sqlite3 so Chroma works on Streamlit Cloud ---
import pysqlite3  # noqa: F401
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
# --------------------------------------------------------
import yaml
from pathlib import Path
from typing import Dict, List
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool


CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"


def _load_yaml(filename: str):
    with open(CONFIG_DIR / filename, "r") as f:
        return yaml.safe_load(f)


def create_crew(verbose: bool = True) -> Crew:
    agents_cfg = _load_yaml("agents.yaml")
    tasks_cfg = _load_yaml("tasks.yaml")

    # ---------------- Agents ---------------- #
    agents: Dict[str, Agent] = {}
    for name, cfg in agents_cfg.items():
        tools = []
        if name in ("plant_specialist", "wildlife_mitigator"):
            tools.append(SerperDevTool())  # Example web-search tool

        agents[name] = Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            tools=tools,
            verbose=cfg.get("verbose", False),
        )

    # ---------------- Tasks ---------------- #
    tasks: List[Task] = []
    for tname, tcfg in tasks_cfg.items():
        tasks.append(
            Task(
                description=tcfg["description"],
                agent=agents[tcfg["agent"]],
                output_file=tcfg.get("output_file"),
            )
        )

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose,
    )
    return crew
# END crew.py
