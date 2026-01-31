# STORY-BARC-013: Long-Running Workflow Implementation

**ID**: STORY-BARC-013  
**Epic**: EPIC-BARC-002  
**Status**: TODO  
**Priority**: P0  

## Description
Implement the master `BPO_Onboarding_Workflow` that orchestrates all assessment stages, ensuring durability across service restarts.

## Acceptance Criteria
- [ ] Workflow correctly calls Security, ZTA, DSA, Thinking Agent, and Ethics Manager.
- [ ] Workflow state is queryable (progress, current step).
- [ ] Workflow survives simulated "crash" and restarts from last checkpoint.

## Tasks
- [ ] Map existing agent logic to Temporal Activities.
- [ ] Implement error handling and retry logic in workflow.
