"""
scaffold.py — Generate a CrewAI project skeleton for the Garden‑Planner app

Usage:
    python scaffold.py [project_name]

Creates the following structure (default project_name = "garden_planner"):

project_name/
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── crew.py
│       └── main.py
└── README.md
"""
import os
import sys
import textwrap
from pathlib import Path
