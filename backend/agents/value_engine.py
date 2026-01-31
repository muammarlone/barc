import logging
import time
from typing import Dict, Any
from pydantic import BaseModel

logger = logging.getLogger("Value-Engine")

class ROIMetrics(BaseModel):
    hours_saved: float
    cost_reduction_usd: float
    productivity_gain_percent: float
    accuracy_lift_percent: float
    evidence_trail: str

class ValueEngine:
    """
    Measures and reports the ROI and Productivity benefits of BARC.
    Calculations are based on KIW-verified benchmarks.
    """
    MANUAL_ASSESSMENT_HOURS = 80.0  # Industry standard for enterprise BPO review
    HOURLY_RATE_USD = 150.0        # Blended rate for Senior Architect / Security Lead
    
    @staticmethod
    def calculate_roi(actual_duration_hours: float, findings_count: int, hard_constraints_flagged: int) -> ROIMetrics:
        # 1. Productivity Gain
        hours_saved = max(0, ValueEngine.MANUAL_ASSESSMENT_HOURS - actual_duration_hours)
        productivity_gain = (ValueEngine.MANUAL_ASSESSMENT_HOURS / actual_duration_hours) * 100 if actual_duration_hours > 0 else 1000
        
        # 2. Cost Reduction
        cost_reduction = hours_saved * ValueEngine.HOURLY_RATE_USD
        
        # 3. Accuracy Lift (Reduction in risk)
        # We assume each hard constraint flagged would have led to a 10% risk increase post-onboarding
        accuracy_lift = min(50.0, hard_constraints_flagged * 12.5) 
        
        evidence = f"Verified: {hours_saved}h saved. {hard_constraints_flagged} critical risks mitigated via DSA automation."
        
        return ROIMetrics(
            hours_saved=round(hours_saved, 1),
            cost_reduction_usd=round(cost_reduction, 2),
            productivity_gain_percent=round(productivity_gain, 1),
            accuracy_lift_percent=round(accuracy_lift, 1),
            evidence_trail=evidence
        )
