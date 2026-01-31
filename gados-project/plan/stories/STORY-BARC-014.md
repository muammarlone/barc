# STORY-BARC-014: Human-in-the-Loop Signaling via Temporal

**ID**: STORY-BARC-014  
**Epic**: EPIC-BARC-002  
**Status**: TODO  
**Priority**: P1  

## Description
Implement the "PMO Gate" as a Temporal Signal wait-point, allowing human architects to review and approve findings before final report generation.

## Acceptance Criteria
- [ ] Workflow enters `WAITING` state at PMO Gate.
- [ ] Workflow resumes immediately upon receiving `PMO_GATE_DECISION` signal.
- [ ] Signal data is incorporated into the final audit trail.

## Tasks
- [ ] Implement `wait_for_signal` integration in `workflows.py`.
- [ ] Add signal endpoint to `main.py` for UI interaction.
