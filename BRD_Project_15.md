# Business Requirements Document (BRD)

## Project Information
- Project Name: Project 15 - Project Management: The AI Project Manager
- Program: AI-Forge 2026 Capstone
- Document Title: Business Requirements Document (BRD)
- Version: 3.0
- Date: 2026-05-29
- Prepared By: Capstone Delivery Team
- Status: Draft for Review

## 1. Executive Summary
The AI Project Manager is an AI-powered system that oversees a project from initiation to closure. Given a project goal, it generates a plan, allocates resources, tracks progress, identifies risks, and communicates status updates to stakeholders.

The solution uses an orchestrator (Supervisor Feature) to coordinate specialized features and keep project execution on track for scope, timeline, and budget.

## 2. Business Need and Problem Statement
Current project delivery in many teams is affected by:
- Manual planning and re-planning overhead.
- Delayed risk identification and reactive issue handling.
- Inconsistent task assignment based on availability and skills.
- Limited real-time visibility of project status.
- Communication gaps between delivery teams and stakeholders.

The AI Project Manager addresses these gaps by automating planning, coordination, monitoring, and reporting in a single intelligent workflow.

## 3. Business Goals and Objectives
The project objectives are:
- Reduce project planning time by at least 40 percent.
- Improve on-time task completion rate to at least 90 percent.
- Detect and flag high-impact risks at least 7 days before deadline impact, where feasible.
- Reduce manual status reporting effort by at least 50 percent.
- Improve stakeholder visibility and satisfaction to at least 4.2/5.
- Deliver the capstone within the 15-day timeline with production-quality standards.

## 4. Scope
### 4.1 In Scope
- Goal-to-plan conversion with tasks, milestones, deadlines, and dependencies.
- Skill and availability-aware resource allocation suggestions.
- Continuous progress tracking against baseline and updated timelines.
- Risk identification with mitigation recommendations.
- Automated stakeholder communication and periodic reporting.
- Supervisor orchestration across all features.
- Dashboard for project status, risks, milestones, and team workload.

### 4.2 Out of Scope
- Full enterprise PPM replacement.
- Payroll, HRIS, or finance module implementation.
- Legal contract management workflows.
- Physical hardware procurement workflows.
- Autonomous decision execution without human override for critical actions.

## 5. Stakeholders and Responsibilities
- Executive Sponsor: Strategic direction and escalation support.
- Product Owner: Requirement priority and acceptance decisions.
- Project Manager: Governance, timeline control, and delivery accountability.
- Team Leads: Task validation, team capacity inputs, quality oversight.
- Team Members: Task execution updates and blockers.
- PMO/Operations: Reporting standards and governance compliance.
- QA Lead: Test strategy, release quality gate, acceptance validation.
- Security Reviewer: Data, access, and audit compliance checks.

## 6. Business Requirements
All requirements are mandatory unless otherwise noted.

### 6.1 Core Business Requirements
- BR-15-001: The system shall accept a high-level project goal and generate a structured project plan.
- BR-15-002: The plan shall include tasks, durations, dependencies, milestones, and owners.
- BR-15-003: The system shall allocate tasks based on skills, role, and availability inputs.
- BR-15-004: The system shall track task status (not started, in progress, blocked, done) in near real time.
- BR-15-005: The system shall identify schedule and dependency risks and assign severity.
- BR-15-006: The system shall recommend mitigation options for identified risks.
- BR-15-007: The system shall issue automated progress updates to stakeholders at configurable intervals.
- BR-15-008: The system shall support replanning when delays or scope changes occur.
- BR-15-009: The system shall maintain audit logs for key planning, assignment, and status actions.
- BR-15-010: The system shall provide dashboard views for timeline health, risk status, and workload.

### 6.2 Governance and Compliance Requirements
- BR-15-011: The system shall provide decision history and rationale traceability where AI recommendations are applied.
- BR-15-012: The system shall support role-based access for project managers, leads, members, and stakeholders.
- BR-15-013: The system shall preserve report snapshots for review and governance.
- BR-15-014: The system shall support export of plan and progress data in CSV/JSON formats.
- BR-15-015: The system shall provide manual override capability for critical AI recommendations.

## 7. Functional Requirements
- FR-15-001 Planning Feature: Generate initial project plan from goal, constraints, and target timeline.
- FR-15-002 Resource Allocation Feature: Match tasks to best-fit resources.
- FR-15-003 Progress Tracking Feature: Capture progress updates and timeline deltas.
- FR-15-004 Risk Assessment Feature: Predict and score schedule/resource/dependency risks.
- FR-15-005 Communication Feature: Send daily/weekly status summaries and alert updates.
- FR-15-006 Supervisor Feature: Orchestrate all feature interactions and workflow transitions.
- FR-15-007 Dashboard Module: Visualize milestones, risk heatmap, and team utilization.
- FR-15-008 Notification Module: Trigger alerts for blockers, milestone slippage, and unresolved risks.
- FR-15-009 Reporting Module: Generate executive and team-level reports.
- FR-15-010 Admin Module: Configure cadence, severity rules, and access permissions.

## 8. Non-Functional Requirements
- NFR-15-001 Performance: 95 percent of read/write dashboard actions complete within 2 seconds.
- NFR-15-002 Availability: Minimum 99.5 percent monthly uptime.
- NFR-15-003 Scalability: Support concurrent multi-project tracking without major degradation.
- NFR-15-004 Security: Enforce encryption in transit and at rest, with least-privilege access.
- NFR-15-005 Reliability: Scheduled backup and recovery aligned with environment policy.
- NFR-15-006 Usability: Core PM workflows should be operable with minimal onboarding.
- NFR-15-007 Auditability: Critical recommendations and overrides must be traceable.

## 9. Assumptions and Constraints
### 9.1 Assumptions
- Required project data (goals, team profiles, constraints) is available.
- Team members provide timely status updates.
- Stakeholders validate reporting format during UAT.

### 9.2 Constraints
- Capstone duration is fixed at 15 calendar days.
- Project scope must align with assignment brief and no project swapping is allowed.
- Production-quality code and original implementation are mandatory.

## 10. Dependencies
- Access to chosen LLM provider and API credentials.
- Selected orchestration framework (for example LangGraph/LangChain/N8N) readiness.
- Database and storage setup for plans, logs, and reports.
- Notification channel setup (email or collaboration platform API).

## 11. Success Metrics (KPIs)
- Planning time reduction >= 40 percent.
- On-time task completion >= 90 percent.
- Blocker detection to escalation time <= 4 hours.
- Manual reporting effort reduction >= 50 percent.
- Risk mitigation acceptance rate >= 70 percent for high-severity alerts.
- Stakeholder satisfaction >= 4.2/5.

## 12. Risk Register
- R-15-001 Inaccurate Resource Data: Bad capacity inputs may reduce allocation quality.
  - Mitigation: Input validation and periodic sync with source roster.
- R-15-002 Model Hallucination Risk: AI may generate unrealistic schedules.
  - Mitigation: Rule constraints, human approval gates, and override controls.
- R-15-003 Low Adoption: Team may bypass tool updates.
  - Mitigation: Lightweight workflow, reminders, and leadership enforcement.
- R-15-004 Integration Failure: Notification or storage integration may break workflows.
  - Mitigation: Retries, fallback queue, and operational alerts.
- R-15-005 Timeline Risk: Capstone duration may be tight for advanced features.
  - Mitigation: Prioritize MVP, phase non-critical enhancements.

## 13. Milestones and Timeline (15 Days)
- M1 (Day 1-2): Requirement finalization and architecture baseline.
- M2 (Day 3-5): Planning and resource allocation feature implementation.
- M3 (Day 6-8): Progress tracking and risk assessment implementation.
- M4 (Day 9-10): Communication and reporting modules implementation.
- M5 (Day 11-12): End-to-end integration, data model hardening, and QA pass 1.
- M6 (Day 13-14): UAT, defect fixes, and demo preparation.
- M7 (Day 15): Final demonstration and submission.

## 14. Acceptance Criteria
Project 15 will be accepted when:
- All mandatory BR and FR items are implemented and validated.
- Supervisor orchestration is functional end to end.
- No unresolved critical defects remain at submission.
- Demo includes application walkthrough, code walkthrough, techniques/tools explanation, and architecture view.
- Outputs are real and functional, not mock-only.

## 15. Governance and Change Control
- Daily check-in with reporting manager during capstone window.
- Scope changes require explicit approval.
- Critical risks escalated within 24 hours.
- Decision and change logs maintained throughout.

## 16. Communication Plan
- Daily progress snapshot to reporting manager.
- Midpoint review on Day 7 or Day 8.
- Pre-demo readiness review on Day 14.
- Final presentation on Day 15.

## 17. Final Deliverables Mapping
- Deliverable 1: Application Walkthrough -> Covered by end-to-end demo scenario.
- Deliverable 2: Code Walkthrough -> Covered by module-level technical walkthrough.
- Deliverable 3: Frameworks/Tools/Techniques -> Covered by implementation rationale deck.
- Deliverable 4: Architecture Diagram -> Covered by system architecture artifact.

## 18. Sign-Off
| Role | Name | Signature | Date |
|---|---|---|---|
| Reporting Manager |  |  |  |
| Product Owner |  |  |  |
| Project Manager |  |  |  |
| QA Lead |  |  |  |
| Security Reviewer |  |  |  |

## Appendix A: Requirement Traceability Matrix
| Requirement ID | Requirement Summary | Priority | Owner | Test Scenario ID | Status |
|---|---|---|---|---|---|
| BR-15-001 | Goal-to-plan generation | High | Product Owner | TS-001 | Planned |
| BR-15-003 | Skill-based allocation | High | Project Manager | TS-003 | Planned |
| BR-15-005 | Risk identification and severity | High | PMO | TS-005 | Planned |
| BR-15-007 | Automated stakeholder updates | Medium | Operations | TS-007 | Planned |
| BR-15-015 | Manual override for critical actions | High | Governance Lead | TS-015 | Planned |

## Appendix B: Capstone Compliance Notes
- Work must strictly match assigned project scope (Project 15 only).
- Original implementation is mandatory.
- Delivery must be completed within 15 calendar days.
