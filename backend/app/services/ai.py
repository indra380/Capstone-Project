from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import get_settings


SYSTEM_PROMPT = (
    "You are an AI project manager assistant. Return compact JSON only with keys: "
    "summary, risks, recommendations."
)


def _extract_text_from_gemini(data: dict[str, Any]) -> str:
    candidates = data.get("candidates", [])
    if not candidates:
        return "{}"
    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    if not parts:
        return "{}"
    return str(parts[0].get("text", "{}"))


def _heuristic_payload(goal: str) -> dict[str, Any]:
    lower = goal.lower()
    risks: list[str] = []
    if "launch" in lower or "release" in lower:
        risks.append("Release readiness risk due to integration and QA dependencies")
    if "4 week" in lower or "4-week" in lower or "month" in lower:
        risks.append("Schedule compression risk due to short timeline")
    if "team" in lower and any(ch.isdigit() for ch in lower):
        risks.append("Capacity risk if team members are unavailable")

    return {
        "summary": "AI fallback analysis generated from deterministic heuristics.",
        "risks": risks or ["No immediate critical risk inferred from goal text"],
        "recommendations": [
            "Prioritize dependency-critical tasks first",
            "Enforce daily blocker escalation",
            "Review scope weekly with stakeholders",
        ],
    }


def generate_goal_analysis(goal: str) -> dict[str, Any]:
    settings = get_settings()
    if settings.openai_api_key.strip() == "":
        return _heuristic_payload(goal)

    endpoint = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.openai_model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Analyze this project goal and return JSON with summary, risks, recommendations: "
                    f"{goal}"
                ),
            },
        ],
    }

    try:
        with httpx.Client(timeout=settings.ai_timeout_seconds) as client:
            response = client.post(endpoint, headers=headers, json=body)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return _heuristic_payload(goal)
        return {
            "summary": str(parsed.get("summary", "")) or "AI analysis generated.",
            "risks": list(parsed.get("risks", [])) if isinstance(parsed.get("risks", []), list) else [],
            "recommendations": (
                list(parsed.get("recommendations", []))
                if isinstance(parsed.get("recommendations", []), list)
                else []
            ),
        }
    except Exception:
        return _heuristic_payload(goal)


def generate_agent_analysis(agent_name: str, context: str) -> dict[str, Any]:
    settings = get_settings()
    prompt = (
        f"Agent: {agent_name}. Return JSON with keys summary, risks, recommendations. "
        f"Context: {context}"
    )

    if settings.ai_provider.lower() == "gemini" and settings.gemini_api_key.strip():
        endpoint = (
            f"{settings.gemini_base_url.rstrip('/')}/models/{settings.gemini_model}:generateContent"
            f"?key={settings.gemini_api_key}"
        )
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        try:
            with httpx.Client(timeout=settings.ai_timeout_seconds) as client:
                response = client.post(endpoint, json=body)
                response.raise_for_status()
                text = _extract_text_from_gemini(response.json())
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return {
                    "summary": str(parsed.get("summary", "")),
                    "risks": list(parsed.get("risks", [])) if isinstance(parsed.get("risks", []), list) else [],
                    "recommendations": (
                        list(parsed.get("recommendations", []))
                        if isinstance(parsed.get("recommendations", []), list)
                        else []
                    ),
                }
        except Exception:
            pass

    if settings.openai_api_key.strip() == "":
        return _heuristic_payload(context)

    endpoint = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.openai_model,
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        with httpx.Client(timeout=settings.ai_timeout_seconds) as client:
            response = client.post(endpoint, headers=headers, json=body)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return _heuristic_payload(context)
        return {
            "summary": str(parsed.get("summary", "")) or "AI analysis generated.",
            "risks": list(parsed.get("risks", [])) if isinstance(parsed.get("risks", []), list) else [],
            "recommendations": (
                list(parsed.get("recommendations", []))
                if isinstance(parsed.get("recommendations", []), list)
                else []
            ),
        }
    except Exception:
        return _heuristic_payload(context)
