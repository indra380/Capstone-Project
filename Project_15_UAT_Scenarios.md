# Project 15 UAT Scenarios (Phase 13)

Date: 2026-06-29
Objective: Prepare UAT scenarios mapped to BRD requirements and confirm UAT-ready quality baseline.

## UAT Entry Criteria
- Backend tests are green.
- JWT auth is enabled.
- RBAC and audit controls are active.
- Seed project can be created through API/UI flow.

## UAT Scenario Matrix

| Scenario ID | BR/FR Mapping | Scenario | Steps | Expected Result | Priority |
|---|---|---|---|---|---|
| UAT-001 | BR-15-001, BR-15-002, FR-15-001 | Goal to plan generation | Create project with goal, run planning | Tasks with milestones/dependencies are created | High |
| UAT-002 | BR-15-003, FR-15-002 | Skill-aware allocation | Invoke allocation action for project | Tasks receive owner assignments by role/skills | High |
| UAT-003 | BR-15-004, FR-15-003 | Progress status tracking | Update tasks to in_progress/blocked/done | Completion and blocked metrics recalculate correctly | High |
| UAT-004 | BR-15-005, BR-15-006, FR-15-004 | Risk detection and mitigation | Trigger risk assessment after blocker update | Risk entries are generated with severity and mitigation | High |
| UAT-005 | BR-15-007, FR-15-005, FR-15-009 | Automated communication/reporting | Generate status report (daily/weekly) | Report snapshot created with project metrics and narrative | Medium |
| UAT-006 | BR-15-008, FR-15-006 | Replanning through orchestration | Run supervisor after project/task updates | Workflow returns stable orchestration with status and errors fields | High |
| UAT-007 | BR-15-009, BR-15-011, NFR-15-007 | Audit and rationale traceability | Execute planning/allocation/risk/override actions, then fetch project audit | Audit stream includes key actions with actor role and rationale | High |
| UAT-008 | BR-15-012, FR-15-010 | Role-based access control | Attempt manager-only endpoints with stakeholder token | Unauthorized calls are blocked with 403 | High |
| UAT-009 | BR-15-013, FR-15-009 | Report snapshot preservation | Generate report and fetch history | Report appears in history with persisted content/snapshot | Medium |
| UAT-010 | BR-15-014 | Data export | Export project as JSON and CSV | Export endpoints return valid JSON and downloadable CSV | High |
| UAT-011 | BR-15-015 | Manual override capability | Perform task owner override | Override succeeds for authorized roles and is audited | High |
| UAT-012 | FR-15-007, FR-15-008 | Dashboard and alerts | Open dashboard analytics after updates | Metrics reflect latest tasks/risks and support stakeholder visibility | Medium |

## UAT Execution Notes
- Preferred execution order: UAT-001 -> UAT-002 -> UAT-003 -> UAT-004 -> UAT-005 -> UAT-006 -> UAT-007 -> UAT-008 -> UAT-009 -> UAT-010 -> UAT-011 -> UAT-012
- Defect severity guide:
  - Critical: blocks core flow or data integrity
  - High: major requirement behavior incorrect
  - Medium: partial behavior mismatch with workaround
  - Low: cosmetic/non-blocking issue

## Phase 13 Fix Pass (Completed)
1. Replaced deprecated UTC-naive datetime usage with timezone-aware UTC timestamps in:
- backend/app/models/entities.py
- backend/app/services/admin.py
- backend/app/services/communication.py
- backend/app/db/sqlalchemy/models.py
2. Goal of fix pass: remove warning-prone time handling before UAT and improve future runtime compatibility.

## UAT Exit Criteria
- All high-priority UAT scenarios pass.
- No open critical defects.
- No open high defects in core BR mandatory scope.
- Test baseline remains green after fix pass.
