---
name: documentation-audit
description: Audit repository documentation against code, tests, configuration, and existing decisions. Use to identify evidence-backed documentation gaps, inconsistencies, stale content, duplication, and unnecessary documents before proposing documentation changes.
---

# Documentation Audit

Audit repository documentation for completeness, correctness,
consistency, and relevance.

Identify actionable documentation problems based on repository
evidence rather than generic documentation checklists.

## Operating Principles

- Follow applicable AGENTS.md and CLAUDE.md instructions.
- Identify canonical documentation and existing project conventions.
- Inspect relevant code, tests, configuration, and documentation.
- Evaluate documentation needs against actual project complexity.
- Prefer improving existing documents over creating new ones.
- Do not treat an absent document as a gap without justification.
- Distinguish verified findings from assumptions and uncertainty.
- Do not invent repository facts or claim checks were performed
  when they were not.
- Report when no significant documentation gaps are found.


## Repository Discovery

Establish the actual repository context before evaluating documentation.

1. Read applicable AGENTS.md and CLAUDE.md instructions, including
   relevant nested instructions.
2. Identify the project's purpose, technology stack, architecture,
   maturity, and operational context.
3. Locate existing documentation and identify its canonical sources.
4. Inspect relevant implementation, tests, interfaces, data models,
   configuration, CI/CD, and deployment artifacts.
5. Consult related issues, decisions, or history when available
   and necessary to resolve uncertainty.
6. Map documented claims to their supporting repository evidence.

Discover incrementally. Start with entry points and follow relevant
references rather than scanning every file indiscriminately.

Use actual repository conventions. Do not assume standard directory
names, languages, frameworks, or documentation layouts.

Distinguish authoritative sources from supporting evidence. When
sources disagree, report the conflict instead of silently choosing
one as correct.

Treat inaccessible, generated, or uninspected material as an
explicit limitation when relevant. Never claim exhaustive coverage
after a selective inspection.

## Documentation Applicability

Determine which documentation concerns are relevant to the actual
project before identifying gaps.

Assess the following areas when applicable:

- Product requirements, expected behavior, and acceptance criteria.
- Architecture, significant decisions, and component boundaries.
- Data models, schemas, interfaces, and integration contracts.
- Quality, testing, security, and compatibility constraints.
- Setup, configuration, deployment, operations, and recovery.

Consider project complexity, maintainership, consumers, risk,
deployment model, and existing documentation conventions.

For each relevant area, determine whether its information is:

- Adequately documented.
- Incomplete or potentially inconsistent.
- Not applicable to the project.
- Unverifiable with the available evidence.

Evaluate information coverage rather than document filenames.

A README, existing specification, or code-adjacent documentation
may adequately cover multiple areas without separate documents.

Do not require PRDs, ADRs, runbooks, or other artifacts merely
because they are common in larger projects.

Recommend additional documentation only when a concrete
information gap or maintenance risk justifies it.


## Documentation Gap Detection

Compare relevant documentation against repository evidence.

Identify the following problem categories when supported:

- Missing: Required information is absent or insufficient for
  an identifiable user, developer, integration, or operational need.
- Stale: Documented behavior, commands, interfaces, or procedures
  no longer match the current repository.
- Contradictory: Documentation sources, or documentation and
  implementation, make incompatible claims.
- Duplicated: Multiple independently maintained sources repeat
  information in ways that create ambiguity or maintenance risk.
- Orphaned: Documentation refers to removed components, obsolete
  workflows, or material whose relevance cannot be established.

Do not classify a document as stale based solely on its age.

Do not classify documentation as duplicated merely because
multiple files reference the same canonical information.

Do not classify a document as orphaned solely because no other
document links to it.

Treat missing documentation as actionable only when its absence
creates a concrete knowledge, maintenance, security, integration,
or operational risk.

Distinguish intentional historical documentation from obsolete
content. Preserve useful decision history and superseded ADRs.

Consolidate related observations into distinct root-cause findings.
Avoid reporting the same problem repeatedly across multiple files.

## Evidence and Validation

Ground every verified finding in inspectable repository evidence.

For each finding:

1. Identify the affected documentation or missing information.
2. Locate relevant supporting sources, such as implementation,
   tests, configuration, or canonical specifications.
3. Explain the discrepancy or unmet information need.
4. Describe its practical impact.
5. Propose the smallest justified corrective action.

Reference precise repository paths and line numbers when available.

For discrepancies, cite both sides of the comparison whenever
possible. For missing information, cite the relevant implementation,
configuration, or workflow that establishes the need.

Do not treat an unverified assumption as a confirmed finding.

When evidence is incomplete, explicitly identify what remains
unverified and what additional inspection would resolve it.

Do not claim runtime behavior, test results, or deployment
conditions based solely on documentation or unexecuted code.

Prefer directly inspected evidence over unsupported inferences.
Recognize that code, tests, and documentation can each be outdated
or incorrect; do not automatically treat any one as ground truth.

## Finding Prioritization

Assign priorities according to demonstrated impact.

- Blocking: A documentation defect that demonstrably prevents
  a necessary operation, safe change, integration, or critical
  decision, or creates a significant security or data-loss risk.
- Important: A material inconsistency or gap that increases
  implementation, maintenance, onboarding, or operational risk
  without meeting the blocking threshold.
- Optional: A justified improvement with limited practical impact,
  such as reducing ambiguity or documentation maintenance effort.

Do not assign blocking priority merely because a document
is missing or inconsistent.

Consider affected users, criticality, scope, and available
workarounds when evaluating impact.

Rank findings within each priority by practical consequences.

Keep priority separate from evidence confidence. When the
impact or underlying facts cannot be established, report the
uncertainty rather than inventing severity.

Recommend the least disruptive corrective action:

- Correct inaccurate or outdated content in place.
- Consolidate conflicting or unnecessarily duplicated sources.
- Link existing authoritative information when sufficient.
- Create new documentation only when existing sources cannot
  adequately cover the identified need.
- Preserve historical records when they remain useful.

Do not prescribe broad documentation restructuring when
a localized correction resolves the problem.

## Safety and Scope

Operate read-only by default.

Do not modify repository files, create documentation, change issues,
or perform other write operations unless explicitly requested.

Do not implement features or duplicate the responsibilities
of the PRD skill.


## Audit Report

Produce a concise, evidence-backed report adapted to the repository
and the number of actionable findings.

### Audit Scope

Summarize:

- Repository or project area examined.
- Relevant documentation and implementation sources inspected.
- Documentation concerns considered applicable.
- Significant coverage limitations.

Do not imply that the entire repository was audited when the
inspection was selective.

### Findings

Order findings by priority: blocking, important, then optional.

Assign each finding a report-local identifier (DA-001, DA-002, etc.).

For each finding, provide:

- ID and descriptive title.
- Category: missing, stale, contradictory, duplicated, or orphaned.
- Priority: blocking, important, or optional.
- Status: verified or needs verification.
- Evidence: precise repository paths and relevant line references
  when available.
- Impact: the concrete consequence of the problem.
- Recommendation: the smallest justified corrective action.

Use "verified" only when directly inspected evidence supports
the reported discrepancy or information gap.

Use "needs verification" when relevant evidence is incomplete.
Identify the missing verification explicitly.

Do not present suspected discrepancies as established facts.

Avoid redundant findings, unsupported severity claims, and
recommendations already satisfied by existing documentation.

### Limitations and Uncertainty

Report material limitations that affect confidence or coverage.

Distinguish:

- Verified repository facts.
- Reasonable but unverified interpretations.
- Information unavailable from the inspected sources.

Identify relevant files, environments, external systems, or
runtime behavior that could not be inspected or validated.

Explain what additional evidence would resolve significant
uncertainty when actionable.

Do not hide limitations or imply successful validation of
checks that were not performed.

### Recommended Next Actions

Summarize only justified corrective actions, ordered by impact.

Prefer updating canonical sources and fixing local inconsistencies
before recommending additional documents.

Do not create files, commits, pull requests, or issues as part
of reporting unless explicitly requested.

### No Significant Findings

If no actionable documentation gaps are supported by the evidence,
state that no significant findings were identified within the
inspected scope.

Summarize relevant coverage and limitations without inventing
improvements to populate the report.

Do not equate the absence of findings with proof that all
documentation is complete or correct.
