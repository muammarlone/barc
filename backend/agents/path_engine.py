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
    def determine_optimal_path(complexity: str, urgency: str, historical_fail_rate: float = 0.05) -> PathRecommendation:
        """
        Calculates the most efficient onboarding route based on complexity, urgency, 
        and historical BPO performance patterns (KIW Lens).
        """
        # Complexity mapping
        c_weight = {"LOW": 1, "MEDIUM": 2, "HIGH": 4}.get(complexity.upper(), 2)
        
        base_days = 14
        risk = historical_fail_rate * c_weight
        
        if urgency == "HIGH":
            return PathRecommendation(
                path_name="EXPRESS_ROUTE",
                estimated_days=int(base_days * 0.5 * c_weight),
                risk_score=min(1.0, risk * 2),
                confidence=0.85,
                reasoning=f"Complexity ({complexity}) handled via accelerated gates. High risk due to compressed timelines."
            )
            
        return PathRecommendation(
            path_name="STANDARD_DEEP_DIVE",
            estimated_days=base_days * c_weight,
            risk_score=risk,
            confidence=0.98,
            reasoning=f"Thorough assessment for {complexity} complexity. Historical fail rate ({historical_fail_rate}) factored into risk profile."
        )

    @staticmethod
    def calculate_metrics(findings_count: int, critical_gaps: int, assessment_duration_days: int = 5) -> QualityMetrics:
        """Calculates Quality Scores and Performance Velocity."""
        # KIW Quality Score: Penalizes critical gaps heavily
        qs = max(0, 100 - (critical_gaps * 25) - (findings_count * 2))
        
        # Velocity: Throughput relative to industry baseline
        velocity = 1.0 / (assessment_duration_days / 7.0) # Normalized to 1 week
        
        return QualityMetrics(
            quality_score=qs,
            performance_velocity=round(velocity, 2),
            readiness_forecast="READY" if qs > 85 else "REMEDIATION_REQUIRED"
        )
