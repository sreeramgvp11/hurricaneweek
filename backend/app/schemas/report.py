from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.simulation import ScoreState


class FinancialSummary(BaseModel):
    starting_cash: int = Field(ge=0)
    ending_cash: int = Field(ge=0)
    damage: int = Field(ge=0)


class FinalReportExplanation(BaseModel):
    what_you_did_well: str
    what_exposed_you: str
    top_preparedness_gaps: list[str]
    preparedness_plan_48h: list[str]


class FinalReport(BaseModel):
    simulation_id: UUID
    outcome: str
    scores: ScoreState
    financial_summary: FinancialSummary
    strengths: list[str]
    preparedness_gaps: list[str]
    action_identifiers: list[str]
    decision_history: list[dict[str, str]]
    explanation: FinalReportExplanation | None = None
