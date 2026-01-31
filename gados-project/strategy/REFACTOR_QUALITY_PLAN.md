# BARC Code Review & Quality Optimization Plan

**Status**: **DRAFT**  
**Target**: 140% Quality Goal (KIW Mid-Stream Review)  
**Lead Optimizer**: Antigravity AI  

---

## 1. Backend Refactor (Python/FastAPI)

### 1.1. Structural Modularization
- Move all Pydantic models from `main.py` to `backend/schemas/assessments.py`.
- Consolidate agent instantiation into a `backend/agents/factory.py` or separate module to keep `main.py` lean.

### 1.2. Governance Enforcement
- **ZTA Validation**: Update `/analyze` to require a ZTA Token in the header, not just issue one. Implement a dependency in FastAPI for ZTA verification.
- **Structured Findings**: Ensure all agents return findings using the `Finding` schema from `dsa_framework.py` strictly.

### 1.3. Code Cleanliness
- Remove excessive blank lines in `main.py`.
- Implement standard logging (`import logging`) for better traceability.
- Add Docstrings to all core functions and agents.

---

## 2. Frontend Refactor (React/Vite)

### 2.1. Configuration
- Move the backend URL to a `.env` file and use `import.meta.env.VITE_BACKEND_URL`.

### 2.2. Robust UI Components
- **Error Boundaries**: Implement error boundaries for major dashboard cards.
- **Skeleton Loaders**: Replace simple "Loading..." text with skeleton states for a premium look.

### 2.3. Type Safety
- Centralize interface definitions (Metrics, Findings, etc.) in `barc-app/src/types/`.

---

## 3. Deployment & Regression (Sprint 5 Prep)
- Prepare the repo for **Reprosense Integration**.
- Add a `tests/` directory in the backend for unit tests.

---

**Directive**: Proceeding with these optimizations immediately to exceed the 140% quality bar.
