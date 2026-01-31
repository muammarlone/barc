# TEMPORAL ORCHESTRATION STRATEGY: BARC System Resilience

**Status**: **PROPOSAL**  
**Lead Strategist**: Antigravity AI  
**Target Architecture**: Agentic Workflow Automation (AWA)  

---

## 1. Objective
To transition BARC from a synchronous, request-response execution model to a **Durable, Fault-Tolerant, and Long-Running** orchestration model using **Temporal**.

## 2. Why Temporal for BARC?
In a BPO assessment, workflows can span days (waiting for human approval, multi-agent deep-dives). Temporal provides:
- **Durable Workflows**: Workflows survive process crashes, network failures, and long-wait intervals.
- **Deterministic Retries**: Automatic retries for flaky DSA tools or API integrations (DMS/Email).
- **Visibility**: Real-time tracking of every node in the "Orchestration Canvas" using the Temporal UI.
- **State Sovereignty**: Centralizes the state of the "BPO Onboarding Journey" independent of the backend service.

---

## 3. Proposed Architecture

### 3.1. Temporal Workflows
- `BPO_Onboarding_Workflow`: The master sequence defined in `CONFIGURABLE_WORKFLOWS_SPEC.md`.
- `Domain_Assessment_Workflow`: Sub-workflow for specific DSAs (Network, IT, Desktop).

### 3.2. Temporal Activities
Each agentic action becomes a Temporal Activity:
- `Ingest_Evidence_Activity`: (Sensory Hub)
- `Analyze_Domain_Activity`: (DSA)
- `Peer_Review_Activity`: (Thinking Agent)
- `Ethical_Audit_Activity`: (Ethics Manager)
- `Synthesize_Report_Activity`: (CSA)
- `Gate_Approval_Activity`: (PMO Gate - wait for signal)

---

## 4. Implementation Roadmap
1.  **Phase 1: Proof of Resilience**: Port the `/analyze` endpoint to a Temporal Workflow.
2.  **Phase 2: Long-Wait Gates**: Implement PMO Approval as a Temporal "Wait for Signal".
3.  **Phase 3: Visual Sync**: Connect the Golden UI Reasoning Stream to Temporal History.

---

**Directive for KIW Board**: Seeking validation on the adoption of Temporal as the "Backbone of Truth" for BARC orchestration.
