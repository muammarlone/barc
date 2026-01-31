# STORY-BARC-003: Sensory Layer - Email Ingestor

**Epic**: EPIC-BARC-001  
**Status**: PLANNED  
**Priority**: P1  

## Description
Implement the Email Ingestor Agent to automatically extract and categorize architectural evidence sent via email.

## Acceptance Criteria
- [ ] IMAP/Outlook API connectivity established.
- [ ] Email body & attachment extraction logic implemented.
- [ ] Categorization engine: Technical Evidence vs. Governance/Risk vs. Performance.
- [ ] Automated vaulting of extracted artifacts in the Evidence Layer.

## Implementation Plan
1. Setup Outlook/Exchange API hooks.
2. Build `EmailParser` for attachment handling.
3. Develop categorization LLM prompt (VDA-governed).
4. Integration test with DMS vaulting.
