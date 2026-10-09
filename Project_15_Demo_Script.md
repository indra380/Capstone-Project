# Project 15 Day 15 Demo Script

## Purpose
This script helps you run a clear, professional final demonstration for Project 15: The AI Project Manager.

## 1. Demo Duration Plan (20-25 minutes)
- 2 minutes: Introduction and problem statement
- 8 minutes: Application walkthrough
- 6 minutes: Code walkthrough
- 4 minutes: Tools and techniques rationale
- 3 minutes: Architecture walkthrough
- 2 minutes: Q and A buffer

## 2. Opening Statement (Use as-is)
Today I am presenting Project 15, The AI Project Manager, from the AI-Forge 2026 capstone assignments. This system converts a high-level project goal into a structured execution plan, allocates resources, tracks progress, identifies risks, and sends stakeholder updates through a supervisor-orchestrated AI workflow.

## 3. Demo Environment Checklist
- Application is running and reachable
- Sample project data loaded
- LLM and integration keys configured
- Notification channel enabled (or sandbox mode enabled)
- Dashboard and logs visible
- Backup screenshots available in case of connectivity issue

## 4. Live Application Walkthrough Script

### Step 1: Goal Intake
- Action: Enter a sample goal.
- Example: Launch a customer support chatbot in 4 weeks with a 4-person team.
- Explain: System captures constraints like deadline, team size, and priorities.

### Step 2: AI Plan Generation
- Action: Click Generate Plan.
- Show: Milestones, tasks, dependencies, estimated durations.
- Explain: Planning Feature breaks down scope and creates executable structure.

### Step 3: Resource Allocation
- Action: Open allocation board.
- Show: Task owner assignments by skill and availability.
- Explain: Resource Allocation Feature optimizes assignment fit and workload balance.

### Step 4: Progress Tracking
- Action: Update one task to delayed and one to completed.
- Show: Timeline shifts and completion percentage updates.
- Explain: Progress Tracking Feature recalculates status and variance from baseline.

### Step 5: Risk Assessment
- Action: Trigger risk refresh.
- Show: New risk entry with severity and mitigation recommendation.
- Explain: Risk Feature detects dependency risk and proposes practical actions.

### Step 6: Communication and Reporting
- Action: Generate status report.
- Show: Executive summary, blockers, milestones at risk, next actions.
- Explain: Communication Feature automates stakeholder reporting with consistent format.

### Step 7: Supervisor Orchestration View
- Action: Open workflow trace or logs.
- Show: Which feature was called and in what sequence.
- Explain: Supervisor Feature orchestrates all feature interactions end to end.

## 5. Code Walkthrough Talking Points
- Repository structure
  - frontend/
  - backend/
  - features/
  - orchestration/
  - data/
  - tests/
- Important modules
  - supervisor coordinator
  - planning service
  - allocation engine
  - risk evaluator
  - reporting service
- Quality controls
  - schema validation
  - logging
  - error handling
  - unit and integration tests

## 6. Frameworks, Tools, and Techniques
- Orchestration: LangGraph or equivalent flow framework
- LLM Integration: provider client with prompt templates and output schema validation
- Data Store: PostgreSQL or Supabase for operational data
- Techniques used:
  - Prompt chaining
  - Structured output parsing
  - Risk scoring heuristics
  - Human override for critical recommendations

## 7. Architecture Walkthrough Script
- Explain layers from UI to backend to Supervisor Feature.
- Show how each specialized feature contributes to a single project state.
- Explain external integrations and notification flow.
- Point out governance controls: RBAC, audit logs, manual override.

## 8. Expected Questions and Short Answers
- Q: How do you prevent unrealistic AI plans?
  - A: Rule constraints plus human approval for critical decisions.
- Q: What happens if a dependency fails?
  - A: Retries, fallback handling, and escalation alerts are triggered.
- Q: Can managers override AI assignments?
  - A: Yes, manual override is mandatory for high-impact decisions.
- Q: How is progress accuracy maintained?
  - A: Through frequent updates, validation checks, and traceable timeline deltas.

## 9. Closing Statement (Use as-is)
This capstone demonstrates a production-oriented AI Project Manager that automates planning, allocation, tracking, risk handling, and communication through an orchestrated multi-feature architecture. The system is designed for transparency, control, and measurable project delivery improvement.
