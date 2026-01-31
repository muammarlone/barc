# STORY-BARC-015: Master Dashboard Scaling (Multi-Tenant Support)

**ID**: STORY-BARC-015  
**Epic**: EPIC-BARC-002  
**Status**: TODO  
**Priority**: P1  

## Description
Evolve the backend and UI to support multiple simultaneous BPO projects across different tenants/business units.

## Acceptance Criteria
- [ ] Backend isolates data and workflows by `tenant_id`.
- [ ] Dashboard displays project metrics for selected tenant.
- [ ] Resource contention is handled (simulated scaling).

## Tasks
- [ ] Implement multi-tenant filtering in `TemporalSimulation`.
- [ ] Add `tenant_id` to all agent and workflow contexts.
