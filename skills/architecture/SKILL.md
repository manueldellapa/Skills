---
name: architecture
description: Analyze, design, review, and evolve software architecture based on repository evidence, existing requirements, and architectural decisions. Use for architecture assessments, component boundaries, system design, technical trade-offs, architectural refactoring, and migration planning.
---

# Software Architecture

Analyze, design, document, and evolve software architecture
based on actual repository context, requirements, and
existing architectural decisions.

Produce actionable, evidence-based architectural guidance.
Prefer solutions proportional to project complexity.

Do not implement architecture changes or redefine requirements.

## Operating Principles

Read-only execution includes avoiding filesystem side effects.

Before running tests, linters, generators, or diagnostic commands,
consider whether they create caches, artifacts, database changes,
or other persistent state.

Prefer non-mutating inspection. When execution is necessary,
use a verified side-effect-free mode or request authorization
before creating persistent files.

- Follow applicable AGENTS.md and CLAUDE.md instructions.
- Inspect relevant repository evidence before proposing designs.
- Respect existing requirements, ADRs, and architectural constraints.
- Distinguish verified current-state observations from assumptions
  and proposed changes.
- Prefer incremental evolution over unnecessary rewrites.
- Evaluate alternatives using explicit technical trade-offs.
- Avoid imposing architectural patterns without demonstrated need.
- Preserve compatibility or document the required migration path.
- Identify significant decisions requiring an ADR.
- Do not invent components, dependencies, behavior, or constraints.
- Operate read-only by default. Do not modify repository files,
  requirements, or decisions unless explicitly requested.

## Repository Discovery

Establish the actual project context before evaluating or
proposing architecture.

1. Read applicable repository and agent instructions.
2. Identify the project's purpose, scope, maturity, and technology stack.
3. Locate canonical requirements, architecture documents, and ADRs.
4. Inspect relevant modules, interfaces, data models, and integrations.
5. Review applicable tests, configuration, CI/CD, and deployment artifacts.
6. Identify operational constraints and relevant non-functional requirements.
7. Consult related issues or implementation history when needed.

Explore incrementally, following relevant entry points and dependencies.
Avoid exhaustive repository scans when focused inspection is sufficient.

Identify authoritative documentation and preserve existing conventions.

When sources conflict, report the discrepancy rather than silently
selecting one as authoritative.

Classify sources according to their authority and purpose:
canonical requirements, approved decisions, implementation
evidence, and unapproved proposals.

Decision registers and closed questions may contain binding
architectural decisions without being formal ADRs.

Preserve their actual status and format. Do not relabel them
as ADRs or recommend duplicate decision records.

Do not infer deployed behavior solely from source code or documentation.
Report material gaps in the available evidence.

## Current-State Architecture Analysis

Describe the existing architecture before evaluating changes.

Examine relevant aspects of:

- System boundaries and external dependencies.
- Components, modules, layers, and their responsibilities.
- Interfaces, contracts, and integration mechanisms.
- Data ownership, persistence, and information flows.
- Dependency direction and component coupling.
- Deployment topology and operational dependencies.
- Security and trust boundaries.
- Reliability, performance, scalability, and maintainability.
- Testing boundaries and architectural testability.

Identify existing architectural strengths, constraints, and
evidence-backed risks.

Do not assume every concern requires a dedicated component,
layer, pattern, or document.

Separate:
- Verified observations supported by repository evidence.
- Reasonable interpretations requiring confirmation.
- Unknown or uninspected architectural areas.

Reference relevant repository paths and precise evidence where
available.

Describe only the architecture actually supported by the
inspected sources. Do not present intended or proposed behavior
as already implemented.

Distinguish implemented defects, documentation inconsistencies,
and risks associated with planned or unimplemented architecture.

Do not present future implementation risks as defects in
existing code.

Before claiming that a component, configuration, or safeguard
is absent, inspect the relevant sources sufficiently.

When inspection is incomplete, report that the item was not
observed within the inspected scope rather than asserting
its absence.

## Architecture Design

Design architecture proposals based on verified project context,
requirements, constraints, and existing decisions.

Before proposing changes:

1. Identify the architectural problem and desired outcome.
2. Reference relevant requirements and acceptance criteria.
3. Establish affected components, interfaces, and dependencies.
4. Identify applicable ADRs and existing architectural constraints.
5. Determine relevant non-functional requirements.
6. Assess whether the existing architecture can accommodate the change.

Define proposed responsibilities, boundaries, interactions,
and data flows at the level of detail justified by the problem.

Consider when relevant:

- Component cohesion and separation of concerns.
- Dependency direction and coupling.
- Data ownership, consistency, and transaction boundaries.
- API contracts and integration compatibility.
- Security, authorization, and trust boundaries.
- Reliability, observability, and failure handling.
- Performance, scalability, and resource constraints.
- Deployment, operations, and testability.

Prefer the simplest architecture that satisfies demonstrated
requirements and constraints.

Do not introduce new services, layers, frameworks, infrastructure,
or abstraction boundaries without clear justification.

Distinguish proposed architecture from verified current-state
behavior. Do not present recommendations as approved decisions.

## Architecture Evolution

Plan architectural changes with explicit consideration for
existing behavior, compatibility, and operational risk.

For each significant proposed change:

1. Identify affected components, interfaces, data, and consumers.
2. Describe the difference between current and target architecture.
3. Evaluate compatibility with existing requirements and ADRs.
4. Identify migration prerequisites and dependencies.
5. Assess data migration, deployment, and rollback implications.
6. Define incremental transition steps when justified.
7. Identify verification needs and unresolved risks.

Prefer changes that can be independently validated and
introduced without unnecessary disruption.

Account for temporary coexistence of old and new components
when a staged migration requires it.

Avoid prescribing migrations or abstractions when a localized
change adequately solves the problem.

Do not silently override existing architectural decisions.
Flag conflicts and decisions requiring explicit approval.

Describe implementation sequencing without implementing changes
or converting architectural guidance into an unsolicited task backlog.

## Technical Trade-offs

Evaluate meaningful alternatives before recommending significant
architectural changes.

Include the existing architecture as an option when retaining it
could reasonably satisfy the requirements.

Compare relevant alternatives using criteria such as:

- Requirements coverage and functional suitability.
- Complexity and maintainability.
- Compatibility and migration effort.
- Security and data integrity.
- Reliability and operational burden.
- Performance and scalability.
- Testability and observability.
- Team capabilities and existing technology investments.

Consider only criteria relevant to the actual decision.

Explain the benefits, costs, limitations, and risks of each
credible alternative.

Prefer evidence from repository constraints, existing
implementation, and documented requirements.

Avoid speculative performance or scalability claims without
supporting evidence.

Recommend a preferred option only when the available evidence
justifies it.

If material uncertainty prevents a reliable recommendation,
identify the missing evidence and explain how to resolve it.

Document the consequences of the recommendation, including
important trade-offs that remain unresolved.

## Architecture Decisions and ADRs

Respect existing architectural decisions and their documented
rationale.

Before recommending significant changes:

- Identify applicable ADRs and their current status.
- Determine whether the proposal is compatible with those decisions.
- Explain any conflicts or consequences of superseding a decision.
- Preserve historical decision context and existing identifiers.

Flag decisions that may require an ADR when they introduce
significant or difficult-to-reverse consequences.

Examples include:

- Major changes to system or component boundaries.
- Changes to data ownership or consistency models.
- New foundational technologies or infrastructure dependencies.
- Breaking changes to integration or public API contracts.
- Significant security, deployment, or operational trade-offs.

For decisions requiring an ADR, summarize:

- Context and architectural problem.
- Relevant constraints and requirements.
- Credible alternatives and their trade-offs.
- Recommended option and rationale, when justified.
- Expected consequences and unresolved questions.

Do not create an ADR for every implementation detail.

Follow existing ADR conventions and decision processes.

Do not silently approve, replace, or supersede architectural
decisions. Treat proposed decisions as pending until explicitly
accepted through the project's established process.

If requirements are missing or contradictory, identify the issue
and recommend clarification through the canonical requirements
process rather than rewriting the PRD.

## Architecture Documentation

Produce focused Markdown documentation appropriate to the
project's architecture, complexity, and existing conventions.

Before creating or updating documentation:

1. Identify existing architecture documentation and its canonical location.
2. Determine whether an existing document can accommodate the change.
3. Follow established naming, organization, and linking conventions.
4. Preserve valid architectural decisions and historical context.
5. Avoid duplicating requirements, ADRs, or implementation details.

Prefer updating existing canonical documentation over creating
parallel architecture specifications.

When no architecture documentation convention exists, propose
a minimal location under `docs/`, such as `docs/architecture/`,
without assuming that a dedicated directory is necessary.

Keep documents focused and navigable.

Use explicit references to relevant requirements, ADRs,
components, interfaces, and repository evidence.

Prefer relative Markdown links for repository-local documents.

Use repository-relative links or verified canonical URLs.
Do not construct guessed external URLs for local documents.

Ensure architectural comparisons include credible alternatives,
not artificial options introduced merely to justify a recommendation.

Use diagrams only when they materially improve understanding
of component relationships, data flows, deployment topology,
or architectural boundaries.

Prefer text-based diagrams, such as Mermaid, when compatible
with the target repository.

Do not introduce diagrams or documents solely for completeness.

When the request is an architecture review, report findings
without modifying documentation unless explicitly requested.

## Architecture Output

Adapt the response to the requested architecture task and
the complexity of the inspected system.

For architecture reviews, provide:

- Scope and inspected repository evidence.
- Verified current-state architecture.
- Architectural strengths, constraints, and relevant risks.
- Actionable findings with supporting evidence.
- Recommended improvements and their trade-offs.
- Material uncertainties and verification needs.

For architecture design or evolution proposals, provide:

- Problem, objectives, and relevant requirements.
- Verified current-state context and affected components.
- Proposed architecture, responsibilities, and data flows.
- Considered alternatives and technical trade-offs.
- Compatibility, migration, and operational implications.
- Relevant risks, mitigations, and verification approach.
- Decisions requiring an ADR or explicit approval.

Keep current-state observations clearly separate from proposed
architecture and unapproved decisions.

Include only sections justified by the requested task.

Prioritize findings by demonstrated impact, confidence,
and relevance to the requested architecture task.

Consolidate overlapping findings and avoid speculative
inventories of potential problems.

Prefer a small set of actionable, well-supported findings
over exhaustive generic recommendations.

Avoid repeating the full report in the closing summary.

Reference concrete repository paths, requirements, and ADRs
where available. Never fabricate identifiers or evidence.

Clearly distinguish recommendations from established decisions.

Report material gaps in inspection or validation.

Summarize the preferred approach and justified next actions.

Do not modify source code, requirements, documentation, ADRs,
issues, or repository history without explicit authorization.
