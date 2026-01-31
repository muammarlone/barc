# ARCHITECTURAL RULES (GADOS Governance) - BARC Project

**Status**: Active / Enforced  
**Purpose**: Non-negotiable technical and governance rules for the BARC platform.

## 1. Multi-Agent Separation
- No single agent shall be responsible for both **Analysis** and **Verification**.
- The **Domain Specialist Agent (DSA)** provides the technical analysis.
- The **Thinking Agent** (Critique Node) provides the peer review/verification.
- The **Delivery Governor (VDA)** certifies the result as "Truth".

## 2. Ingestion Protocol
- All evidence must enter the system through the **DMS Connector**, **Email Ingestor**, or **Collab Connect**.
- No ad-hoc file system access for agents is allowed unless brokered by the **Workspace Manager**.
- Every ingested artifact must be assigned a unique **Traceability ID**.

## 3. Communication Gates (CMP)
- Technical artifacts are born as **Internal Only (Review)**.
- No artifact transitions to **External Ready (Distribution)** without PMO clearance.
- The **Communication Specialist Agent (CSA)** must sanitize and translate all external reports.

## 4. UI/UX Principles (KIW Golden UI)
- All interfaces must follow the **KIW Golden UI** standards (Glassmorphism, Dark Mode, Minimalist).
- Every screen must have a clear **Hierarchy of Information** (L1-L3).
- **Trust Gauges** and **SLA Timers** are mandatory for assessment screens.

## 5. Security (Zero Trust)
- All project identities must be verified continuously.
- Least-privilege access is the default for all agents.
- Sensitive vendor data must be logically isolated from other BPO assessments.

## 6. Auditability
- Every decision must be "Fingerprinted" (Owner ID + Timestamp).
- The `log/` directory in `gados-project` is the immutable system of record for all delivery events.
