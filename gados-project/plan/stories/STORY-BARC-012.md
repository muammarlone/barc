# STORY-BARC-012: Temporal Infrastructure Setup & Base Worker

**ID**: STORY-BARC-012  
**Epic**: EPIC-BARC-002  
**Status**: IN_PROGRESS  
**Priority**: P0  

## Description
Establish the core Temporal (simulated or real) orchestration layer to support long-running, fault-tolerant BPO assessment workflows.

## Acceptance Criteria
- [x] Simulation layer supports workflow execution and activity tracking.
- [x] History and Query support implemented.
- [x] Base Worker capable of polling and executing registered tasks.

## Tasks
- [x] Implement `TemporalSimulation` class.
- [x] Register base activities.
- [ ] Implement persistent history store (SQLite/JSON).
