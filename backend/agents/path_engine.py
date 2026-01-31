from pydantic import BaseModel
from typing import List, Dict

class PathRecommendation(BaseModel):
    path_name: str
    estimated_days: int
    risk_score: float
    confidence: float
    reasoning: str

class QualityMetrics(BaseModel):
    quality_score: float
    performance_velocity: float
    readiness_forecast: str

class OPME:
    @staticmethod
    def determine_optimal_path(complexity: str, urgency: str) -> PathRecommendation:
        if urgency == "HIGH":
            return PathRecommendation(
                path_name="EXPRESS_ROUTE",
                estimated_days=7,
                risk_score=0.25,
                confidence=0.88,
                reasoning="Priority given to speed due to mission-critical urgency. Deep-dives deferred to post-onboarding."
            )
        return PathRecommendation(
            path_name="STANDARD_DEEP_DIVE",
            estimated_days=21,
            risk_score=0.05,
            confidence=0.96,
            reasoning="Balanced approach ensuring 100% compliance across all domains."
        )

    @staticmethod
    def calculate_metrics(findings_count: int, critical_gaps: int) -> QualityMetrics:
        # Simple heuristic for metric calculation
        qs = max(0, 100 - (critical_gaps * 15) - (findings_count * 2))
        return QualityMetrics(
            quality_score=qs,
            performance_velocity=0.94,
            readiness_forecast="March 2026"
        )
