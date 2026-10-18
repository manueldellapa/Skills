---
name: prd
description: Create or refine repository-aware, implementation-ready Product Requirements Documents (PRDs). Use when defining software requirements, planning features, analyzing impact, organizing milestones, user stories, dependencies, or acceptance criteria.
---

# PRD Generator

Create concise, modular, traceable, and implementation-ready Product
Requirements Documents suitable for Claude Code, Codex, and other coding agents.

Analyze and document requirements. Do not implement features.

## 1. Repository Discovery

Before defining requirements:

- Follow applicable AGENTS.md and CLAUDE.md instructions.
- Identify canonical specifications, architecture, and conventions.
- Inspect relevant source code, interfaces, data models, and tests.
- Review related PRDs, ADRs, and available GitHub/GitLab Issues.
- Reuse existing project knowledge instead of rediscovering it.
- Inspect selectively to minimize unnecessary context consumption.

Distinguish verified facts, assumptions, and unresolved questions.

Do not invent repository structures, APIs, dependencies, or behavior.

## 2. Impact Analysis

Assess how the proposed feature affects the existing repository.

Identify relevant:

- Components, modules, and interfaces.
- Data models, schemas, and migrations.
- APIs, integrations, and external dependencies.
- Security, performance, and compatibility constraints.
- Existing tests and documentation.

Identify conflicts with existing behavior or canonical specifications.

Do not introduce incompatible requirements without documenting
the necessary changes or migration strategy.

Describe expected impact without prescribing unnecessary
implementation details.

## 3. Requirements Definition

Define:

- Problem and expected outcomes.
- Target users or affected systems.
- Functional and non-functional requirements.
- Scope and explicit exclusions.
- Constraints and dependencies.
- Measurable success criteria.

Use stable requirement identifiers: FR-001, FR-002, etc.

Avoid ambiguous, duplicated, or unverifiable requirements.

Prefer existing architectural decisions over speculative designs.

## 4. Requirements Traceability

Maintain explicit relationships between:

- Functional requirements.
- Milestones.
- User stories.
- Acceptance criteria.
- Implementation tasks.
- Related GitHub/GitLab Issues.

Use stable identifiers:

- Requirements: FR-001
- Milestones: M0, M1
- User stories: US-001
- Acceptance criteria: AC-US-001-01
- Tasks: TASK-001

Preserve existing identifiers when updating documentation.

Each user story must reference its requirements.
Each acceptance criterion must belong to a user story.
Each implementation task must reference its parent story.

Avoid duplicating requirements across documents.

## 5. Milestones and Dependencies

Organize complex features into logical milestones.

- Identify prerequisites and implementation dependencies.
- Order stories according to their dependencies.
- Prioritize foundational changes when required.
- Prefer independently deliverable vertical slices.
- Avoid circular dependencies.
- Identify tasks that can execute independently.

Do not assume a fixed database-to-backend-to-frontend sequence
when repository architecture suggests a better approach.

Preserve existing milestone conventions when available.

## 6. User Stories and Atomic Tasks

Create focused user stories with:

- Stable identifier and descriptive title.
- Expected outcome.
- Related requirements.
- Dependencies.
- Verifiable acceptance criteria.
- Verification approach.
- Definition of Ready status.

Break implementation work into atomic tasks when useful.

Each task should:

- Represent one focused change.
- Have a clear expected outcome.
- Be independently verifiable where practical.
- Reference its parent story.
- Avoid unnecessary coupling with unrelated changes.

Prefer tasks suitable for one focused Claude Code or Codex session.

Do not fragment trivial changes into unnecessary tasks.

## 7. Definition of Ready

Evaluate each user story before marking it implementation-ready.

A story is READY when:

- Its objective and scope are clear.
- Related requirements are identifiable.
- Acceptance criteria are observable and testable.
- Relevant dependencies and constraints are known.
- Expected repository impact is sufficiently understood.
- No unresolved blocking decision prevents implementation.

Otherwise, mark it BLOCKED and document the missing information.

Do not fabricate answers to satisfy readiness criteria.

## 8. Technical Risks

Identify relevant risks before implementation.

Consider:

- Architectural incompatibilities.
- Breaking changes and migrations.
- Security and data integrity.
- External service dependencies.
- Performance and scalability.
- Operational and deployment constraints.
- Insufficient testability.

Record significant risks with their impact and possible mitigation.

Avoid speculative risk lists without supporting evidence.

## 9. GitHub and GitLab Integration

When issue tracking is available:

- Identify existing related issues.
- Reference issues using canonical URLs.
- Preserve issue identifiers and relationships.
- Link relevant PRDs, milestones, stories, and tasks.
- Avoid duplicating work already described in existing issues.
- Identify missing issue coverage when relevant.

Never invent issue identifiers or URLs.

Do not create, edit, or close issues unless explicitly requested.

## 10. Incremental Documentation

Treat PRDs as evolving project documentation.

When updating an existing PRD:

- Reuse its canonical documents and identifiers.
- Modify affected sections instead of rewriting everything.
- Preserve valid decisions and requirements.
- Update affected dependencies and references.
- Identify obsolete, contradictory, or superseded content.
- Avoid creating duplicate or competing specifications.

Keep documentation aligned with current repository knowledge.

Do not silently discard unresolved decisions or historical context.

## 11. Documentation Organization

Store generated PRD documentation under `docs/`.

Follow existing repository conventions when compatible.
Otherwise, use `docs/prd/`.

For simple features:

docs/prd/<feature-name>.md

For complex features:

docs/prd/<feature-name>/
├── README.md
├── milestones/
│   └── M0-foundation.md
└── stories/
    └── US-001-description.md

The README provides the overview, scope, requirements,
milestone sequence, and navigation.

Milestone documents describe outcomes, dependencies,
and related stories.

Story documents contain acceptance criteria, atomic tasks,
verification requirements, and readiness status.

Keep tasks within their parent stories unless separate
documents provide clear value.

Create only the files justified by feature complexity.

Never use the root `tasks/` directory for PRD documentation.

## 12. Graphify-Friendly Documentation

Write documentation that is easy to navigate and analyze.

- Keep Markdown documents focused and reasonably sized.
- Split large documents along meaningful boundaries.
- Avoid excessive fragmentation and arbitrary size limits.
- Use descriptive headings and consistent terminology.
- Maintain stable identifiers and filenames.
- Express dependencies and relationships explicitly.
- Link related documents using relative Markdown links.
- Maintain one canonical source for each requirement.
- Avoid duplicated content and ambiguous references.
- Keep indexes and navigation links synchronized.

Prefer standard Markdown over tool-specific metadata.

Do not require Graphify to be installed or available.

## 13. Acceptance Criteria and Verification

Write measurable and verifiable acceptance criteria.

Include relevant:

- Expected behavior.
- Boundary conditions.
- Failure scenarios.
- Security and compatibility requirements.
- Regression considerations.

Use the repository's actual testing conventions.

Include appropriate validation for UI changes when relevant.

Never assume a specific language, framework, or testing tool.

Do not confuse implementation tasks with acceptance criteria.

## 14. PRD Self-Validation

Before delivering documentation, verify:

- Consistency with canonical repository specifications.
- Completeness and clarity of requirements.
- Unique and stable identifiers.
- Traceability between requirements, stories, criteria, and tasks.
- Logical dependency ordering without circular dependencies.
- Testable acceptance criteria.
- Definition of Ready status for each story.
- Consistency of related GitHub/GitLab references.
- Absence of contradictory or duplicated requirements.
- Valid internal documentation links.
- Absence of unnecessary or obsolete documents.

Report unresolved inconsistencies instead of hiding them.

Do not claim validation succeeded without performing it.

## 15. Output

Save or update PRD documentation under `docs/`.

Return a concise summary containing:

- Created or updated documentation paths.
- Milestones and implementation order.
- Stories that are READY or BLOCKED.
- Significant technical risks.
- Unresolved decisions requiring attention.

Do not implement code, create commits, or modify issue trackers
unless explicitly requested.