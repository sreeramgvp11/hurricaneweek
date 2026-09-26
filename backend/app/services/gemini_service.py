import json
import os
from uuid import UUID

from pydantic import ValidationError

from app.schemas.report import FinalReport, FinalReportExplanation

try:
    from google import genai
except ModuleNotFoundError:  # pragma: no cover
    genai = None


class GeminiService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        self.enabled = bool(self.api_key and genai is not None)

        self._client = None
        if self.enabled:
            self._client = genai.Client(api_key=self.api_key)

    def explain_decision(
        self,
        simulation_id: UUID,
        event_id: str,
        choice_id: str,
        state: dict,
        scores: dict[str, int],
        consequence: str,
    ) -> str | None:
        if not self._client:
            return None

        prompt = (
            "You are a hurricane preparedness explainer. "
            "Use only the provided deterministic simulation data. "
            "Do not change any numbers. Do not invent consequences. "
            "Do not provide policy-specific insurance advice. "
            "Explain what changed and why it matters. "
            "Give exactly one practical preparedness action. "
            "Keep it concise (max 90 words).\n\n"
            f"simulation_id: {simulation_id}\n"
            f"event_id: {event_id}\n"
            f"choice_id: {choice_id}\n"
            f"consequence: {consequence}\n"
            f"stage: {state['stage']}\n"
            f"cash: {state['cash']}\n"
            f"preparedness_points: {state['preparedness_points']}\n"
            f"timing_points: {state['timing_points']}\n"
            f"financial_loss: {state['financial_loss']}\n"
            f"safety_score: {scores['safety']}\n"
            f"financial_score: {scores['financial']}\n"
            f"preparedness_score: {scores['preparedness']}\n"
            f"timing_score: {scores['timing']}\n"
            f"overall_score: {scores['overall']}"
        )

        try:
            response = self._client.models.generate_content(model=self.model, contents=prompt)
        except Exception:
            return None

        text = getattr(response, "text", None)
        return text.strip() if text else None

    def explain_current_state(self, simulation_id: UUID, state: dict, scores: dict[str, int]) -> str | None:
        if not self._client:
            return None

        prompt = (
            "You are a hurricane preparedness explainer. "
            "Use only this deterministic simulation state. "
            "Do not change any numbers. Do not invent consequences. "
            "Do not provide policy-specific insurance advice. "
            "Explain what changed and why it matters. "
            "Give one practical preparedness action. "
            "Keep it concise (max 90 words).\n\n"
            f"simulation_id: {simulation_id}\n"
            f"stage: {state['stage']}\n"
            f"status: {state['status']}\n"
            f"cash: {state['cash']}\n"
            f"food_days: {state['food_days']}\n"
            f"water_days: {state['water_days']}\n"
            f"evacuated: {state['evacuated']}\n"
            f"financial_loss: {state['financial_loss']}\n"
            f"completed_events: {len(state['completed_events'])}\n"
            f"scores: {scores}"
        )

        try:
            response = self._client.models.generate_content(model=self.model, contents=prompt)
        except Exception:
            return None

        text = getattr(response, "text", None)
        return text.strip() if text else None

    def explain_final_report(self, report: FinalReport) -> FinalReportExplanation | None:
        if not self._client:
            return None

        payload = report.model_dump(mode="json")
        prompt = (
            "You are a hurricane-readiness explainer. "
            "Use only the deterministic report data provided. "
            "Do not change any numbers. Do not invent consequences. "
            "Do not provide policy-specific insurance advice. "
            "Return strict JSON with keys: what_you_did_well, what_exposed_you, "
            "top_preparedness_gaps, preparedness_plan_48h. "
            "top_preparedness_gaps and preparedness_plan_48h must be arrays of short strings.\n\n"
            f"report_json: {json.dumps(payload)}"
        )

        try:
            response = self._client.models.generate_content(model=self.model, contents=prompt)
            text = getattr(response, "text", None)
            if not text:
                return None
            data = json.loads(text)
            return FinalReportExplanation.model_validate(data)
        except (json.JSONDecodeError, ValidationError, Exception):
            return None
