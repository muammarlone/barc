# KIW Golden UI Specification: BARC Platform

**Standard**: KIW Premium Aesthetics (Glassmorphism + Intel Style)  
**Project**: Agentic BPO Architecture Assessment Platform (BARC)  
**Version**: 1.1  

---

## 1. Universal Design Principles

The BARC UI is governed by the **Intel/PDF "Calm Tech" Philosophy**:
- **Information over Decoration**: Every pixel must serve a data-reporting purpose.
- **Progressive Disclosure**: Hide complexity until the user requests it. Use "Drill-Down" patterns.
- **Micro-Animations**: Use subtle transitions (200ms ease-in-out) for element state changes.
- **Glassmorphic Depth**: Use `backdrop-filter: blur(20px)` for overlays and sidebars to create a premium, layered feel.

---

## 2. Visual Identity & Tokens

| Token | Value | Applied To |
| :--- | :--- | :--- |
| **Primary Base** | `#0F172A` (Slate 900) | Background, Deep Depth |
| **Accent Primary** | `#38BDF8` (Sky 400) | Active states, Primary buttons |
| **Status: Critical** | `#EF4444` (Red 500) | SLA Breach, Security Gap |
| **Status: Compliant** | `#10B981` (Emerald 500) | Approved gates, Passed tests |
| **Surface** | `rgba(255, 255, 255, 0.03)` | Glass cards, Blur panels |
| **Typography** | `Inter`, `Outfit` | UI text and data headers |

---

## 3. High-Fidelity Screen Specifications

### 3.1. The "Observer" Executive Dashboard
- **Component: Global Assessment Heatmap**: A 3D-effect honeycomb grid representing different BPO regions/domains.
- **Component: Agent Activity Pulse**: A real-time, scrolling log of agent reasoning steps (e.g., "Network Agent: Analyzing Redundancy... ✓ Verified").
- **Core Action**: A single, prominent "Certify Compliance" button that only activates when all Trust Gauges are >95%.

### 3.2. The "Domain Sandbox" (Assessor Interface)
- **Left Rail**: "Standards Library". Collapsible categories of IT, Network, and Endpoint rules.
- **Center Canvas**: The Evidence Viewer. Supports PDF pinning, image zooming, and inline agent annotations.
- **Right Rail (KIW Intelligent Sidebar)**: 
    - **Agent Insights**: Cards showing "Thinking" vs "Findings".
    - **Consensus Gauge**: Shows the agreement level between different agents.
    - **Human Override**: A dedicated section for Senior Architects to add "Contextual Corrections".

### 3.3. The "Traceability Graph" (Audit View)
- **Visual Pattern**: A directed acyclic graph (DAG) layout.
- **Nodes**: Standard Node -> Evidence Node -> Finding Node -> Approval Node.
- **Interactive**: Hovering over a link shows the "Reasoning Path" (e.g., "Why this finding was generated").

---

## 4. Interaction Patterns

### 4.1. The "Agent Summon"
When a worker uploads evidence, the corresponding Domain Specialist Agent (DSA) appears as a subtle, pulsing avatar in the corner, indicating it is "investigating". Once done, it slides into the sidebar with a "Sparkle" animation.

### 4.2. The "Gate Transition"
Moving from 'Analyze' to 'Control' (DMAIC) involves a full-screen, blurred transition that shows a checklist of "Acceptance Criteria" being marked off one-by-one with satisfying haptic-like animations.

---

## 5. Accessibility & Responsive Design
- **WCAG 2.1 AA**: Minimum contrast ratios of 4.5:1 on all text.
- **Keyboard Navigation**: Full `Tab` support with high-visibility focus rings.
- **Responsive**: Dashboard transforms into a "Status Feed" for mobile reviewers.

---

**UI Strategy Lead**: Antigravity AI  
**Status**: Design Approved ✅
