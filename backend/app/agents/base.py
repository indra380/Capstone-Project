from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.services.ai import generate_agent_analysis


class BaseAgent:
    name = "base"

    @property
    def prompts_root(self) -> Path:
        return Path(__file__).resolve().parents[3] / "prompts"

    def load_prompt(self, filename: str) -> str:
        path = self.prompts_root / filename
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def analyze(self, prompt_file: str, payload: dict[str, Any]) -> dict[str, Any]:
        prompt_template = self.load_prompt(prompt_file)
        context = {
            "prompt": prompt_template,
            "payload": payload,
        }
        return generate_agent_analysis(self.name, json.dumps(context, ensure_ascii=True))
