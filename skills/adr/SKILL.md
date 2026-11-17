---
name: adr
description: Create, review, and maintain repository-aware Architecture Decision Records (ADRs). Use when documenting architectural decisions, evaluating alternatives, tracking decision status, identifying conflicting or superseded decisions, and preserving architectural decision history.
---

# Architecture Decision Records

Prepare, review, and maintain concise, traceable
Architecture Decision Records based on repository evidence.

Respect existing decision conventions and approval processes.

Do not make architectural decisions on behalf of stakeholders.
Do not implement code or approve proposed decisions.

## Operating Principles

- Follow applicable AGENTS.md and CLAUDE.md instructions.
- Inspect relevant repository evidence before preparing ADRs.
- Identify canonical requirements, architecture documentation,
  existing decisions, and established ADR conventions.
- Respect existing decisions and their documented approval status.
- Distinguish verified facts, assumptions, proposals, and
  accepted architectural decisions.
- Evaluate meaningful alternatives and their trade-offs.
- Preserve existing ADR identifiers and decision history.
- Identify contradictions, dependencies, and superseded decisions.
- Do not invent decisions, approvals, requirements, or evidence.
- Do not present a proposal as accepted without clear evidence
  of approval through the project's decision process.
- Operate read-only by default, including avoiding filesystem
  side effects from diagnostic commands.
- Do not modify repository files, implement code, or change
  issue trackers unless explicitly requested.

## Repository Discovery

Establish the repository's decision-making context before
creating, reviewing, or updating Architecture Decision Records.

1. Read applicable repository and agent instructions.
2. Identify canonical requirements and architecture documentation.
3. Locate existing ADRs, decision registers, and other
   authoritative records of architectural decisions.
4. Determine established ADR locations, filename patterns,
   identifiers, numbering, templates, and status conventions.
5. Inspect relevant existing decisions, including their rationale,
   relationships, approval evidence, and supersession history.
6. Examine related implementation, tests, configuration, issues,
   and repository history when needed to establish context.
7. Identify the project's documented decision owners,
   approval process, and lifecycle rules when available.

Explore incrementally. Follow relevant references rather than
performing exhaustive repository scans without justification.

Distinguish formal ADRs from decisions recorded in other
authoritative documents. Do not assume every architectural
decision must be converted into an ADR.

Preserve existing conventions and canonical sources.
Do not introduce duplicate records for decisions already
adequately documented elsewhere.

When conventions are absent, propose a minimal ADR format,
location, and numbering scheme rather than silently imposing one.

Do not allocate an identifier without checking existing records
for collisions. If uniqueness cannot be established, report
the uncertainty before creating the record.

Treat missing, conflicting, or inaccessible evidence as an
explicit limitation. Do not infer approval, implementation,
or decision status from filenames, code, or issue closure alone.

When authoritative sources disagree, identify the conflict
and request clarification rather than selecting one silently.

Do not claim complete decision-history coverage when
repository inspection was selective or incomplete.

## ADR Applicability and Decision Context

Determine whether a formal ADR provides lasting value before
proposing a new decision record.

An ADR is appropriate when a decision has meaningful architectural
consequences, involves important trade-offs, or is difficult
or costly to reverse.

Examples include:

- Foundational technology or infrastructure choices.
- System boundaries and component responsibilities.
- Data ownership, persistence, and consistency models.
- Significant API, integration, or compatibility decisions.
- Security architecture and trust boundaries.
- Deployment architecture and operational constraints.
- Major architectural migrations or technology replacements.

Do not create ADRs for routine implementation details,
minor refactoring, or decisions already adequately captured
in authoritative records.

Before drafting an ADR:

1. Define the architectural question and desired outcome.
2. Identify relevant requirements and architectural constraints.
3. Establish the current architecture using repository evidence.
4. Identify existing decisions that constrain the available options.
5. Determine the decision drivers and evaluation criteria.
6. Identify credible alternatives, including retaining the
   current approach when appropriate.
7. Establish relevant stakeholders and approval requirements
   when documented.
8. Record missing evidence and unresolved questions.

Distinguish the architectural problem from the proposed solution.

Do not present assumptions, preferences, or recommendations
as established project requirements.

When an existing ADR covers the same decision, determine
whether clarification, amendment, or explicit supersession
is appropriate instead of creating a duplicate.

When the evidence is insufficient to evaluate alternatives
or justify a decision, identify the missing information
rather than inventing a rationale.

If a formal ADR is not justified, explain why and recommend
the smallest appropriate form of documentation.

## ADR Drafting

Prepare concise, self-contained ADRs that explain the
architectural problem, considered alternatives, rationale,
and expected consequences.

Follow the target repository's established ADR template,
terminology, structure, and metadata conventions.

When no convention exists, propose a minimal structure
covering the following information:

- Title: A concise description of the architectural decision.
- Status: The decision's documented lifecycle state.
- Context: The problem, current situation, and relevant constraints.
- Decision Drivers: Requirements and criteria influencing the choice.
- Considered Options: Credible alternatives and their trade-offs.
- Proposed Decision: The preferred option and supporting rationale.
- Consequences: Expected benefits, costs, risks, and limitations.
- References: Related requirements, architecture documents,
  issues, and architectural decisions.

Include only sections and metadata justified by the decision
and the repository's conventions.

### Alternatives and Rationale

Evaluate meaningful alternatives against relevant decision drivers.

Include the existing approach when retaining it is a credible option.

Describe relevant advantages, disadvantages, risks, and constraints.

Avoid artificial alternatives introduced solely to justify
a predetermined recommendation.

Base the rationale on documented requirements, technical evidence,
and explicit trade-offs.

Do not invent benchmarks, performance claims, approval history,
or operational constraints.

When evidence does not justify a preferred option, document
the uncertainty and outstanding evaluation needs.

### Decision and Consequences

Clearly distinguish a recommended option from an accepted decision.

Use the repository's proposed or pending status when available.
Do not mark a new decision accepted without verified approval.

Describe significant positive and negative consequences,
including relevant compatibility, migration, security,
maintenance, and operational implications.

Identify unresolved risks, assumptions, and follow-up decisions.

Do not present expected future behavior as already implemented.

### Document Quality

Keep each ADR focused on one coherent architectural decision.

Use precise language and avoid unnecessary implementation detail.

Preserve established identifiers, naming conventions,
and document structure.

Link supporting evidence and related decisions where available.

Use valid relative Markdown links for repository-local documents.

Do not invent identifiers, dates, stakeholders, or references.

Explicitly identify material missing information rather than
silently filling gaps with assumptions.

Do not create or modify ADR files without explicit authorization.

## Decision Lifecycle and Supersession

Respect the repository's established decision lifecycle,
status terminology, and approval process.

Do not impose a universal ADR state machine.

Distinguish, when supported by project conventions:

- Proposed: A decision awaiting evaluation or approval.
- Accepted: A decision approved through the established process.
- Rejected: A proposal explicitly declined.
- Superseded: A decision replaced by a subsequent decision.
- Deprecated: A decision being phased out, when this status
  is explicitly defined by the repository.

Do not infer acceptance from implementation, issue closure,
document existence, or the absence of objections.

### Approval and Status Transitions

Before changing an ADR's status:

1. Identify the current documented status.
2. Determine the applicable approval process.
3. Verify explicit evidence authorizing the transition.
4. Identify the approving authority when documented.
5. Preserve relevant approval references and decision history.

Do not change decision status based solely on a recommendation
or an instruction to draft or update documentation.

When approval evidence is missing or ambiguous, preserve
the existing status and report the unresolved approval question.

Do not invent approval dates, decision owners, or reviewers.

### Superseding Existing Decisions

When a new decision conflicts with an existing accepted ADR,
evaluate whether explicit supersession is required.

Before proposing supersession:

1. Identify the affected ADR and its current status.
2. Explain why the existing decision is no longer suitable.
3. Describe the architectural changes and relevant trade-offs.
4. Identify compatibility, migration, and operational impacts.
5. Reference the original decision in the proposed replacement.
6. Determine which historical references require updating.

Preserve superseded ADRs and their original rationale.

Use explicit relationships between the replacing and replaced
decisions, following repository conventions.

Do not mark an existing ADR superseded merely because a
replacement has been proposed.

Only record supersession as effective when the replacement
has been approved through the established decision process.

Update historical status and cross-references only when
explicitly authorized and supported by approval evidence.

If approval or write authorization is missing, report the
required changes without applying them.

### Conflicts and Historical Consistency

Identify contradictory decisions using their actual scope,
status, applicability, and documented chronology.

Distinguish genuine contradictions from decisions that apply
to different components, environments, or time periods.

Identify stale references to superseded decisions when
relevant to the requested task.

Do not silently reconcile contradictory accepted decisions.

Report conflicts with references to the affected records,
their documented status, and the evidence supporting the finding.

When the authoritative decision cannot be established,
surface the ambiguity rather than inventing a resolution.

## Traceability and Cross-References

Maintain explicit, verifiable relationships between architectural
decisions and their supporting project documentation.

Identify and reference relevant:

- Product requirements and acceptance criteria.
- Architecture specifications and design documents.
- Related ADRs and authoritative decision registers.
- GitHub or GitLab issues and review discussions.
- Implementation evidence and migration plans when applicable.

Preserve existing document identifiers and reference conventions.

Use relative Markdown links for repository-local documents
and verified canonical URLs for external references.

Do not invent identifiers, issue numbers, document paths,
approval references, or external URLs.

### Decision Relationships

Distinguish relationships such as:

- Depends on: A decision relies on another established decision.
- Related to: Decisions address connected architectural concerns.
- Conflicts with: Decisions contain incompatible constraints
  or outcomes within an overlapping scope.
- Supersedes: An approved decision explicitly replaces an
  earlier decision.
- Superseded by: A historical decision references its
  approved replacement.

Follow established repository terminology when available.

Do not infer a supersession relationship solely from
chronology, similarity, or overlapping subject matter.

### Reference Maintenance

When creating or updating an ADR:

1. Identify relevant existing documents and decisions.
2. Verify referenced identifiers, paths, and relationships.
3. Include links necessary to understand the decision context.
4. Identify references affected by the proposed change.
5. Check for contradictory or outdated references.
6. Report additional documentation updates when justified.

Preserve historical references that explain why past
architectural decisions were made.

Avoid duplicating requirements, architectural specifications,
or decision rationale across multiple documents.

Prefer linking canonical sources over copying their contents.

Update related documents or decision indexes only when
explicitly requested and within the authorized scope.

Do not interpret a linked issue, merged pull request,
or implemented feature as evidence of decision approval
unless the established approval process confirms it.

Report broken, ambiguous, or unverifiable references
rather than silently replacing them with guessed targets.

## ADR Review and Validation

Review ADRs for clarity, completeness, consistency,
traceability, and compliance with repository conventions.

Evaluate the following aspects when applicable:

- The architectural problem and decision scope are clear.
- Decision drivers reflect documented requirements and constraints.
- Considered alternatives are credible and meaningfully compared.
- The rationale supports the proposed or accepted decision.
- Positive and negative consequences are documented.
- Assumptions, uncertainties, and unresolved risks are explicit.
- Identifiers, filenames, and metadata follow established conventions.
- Decision status is supported by appropriate evidence.
- Related requirements, decisions, and references are consistent.
- Supersession relationships preserve decision history.

### Evidence-Based Findings

Ground review findings in inspectable repository evidence.

For each actionable finding:

1. Identify the affected ADR and relevant location.
2. Describe the specific problem or inconsistency.
3. Reference supporting evidence when available.
4. Explain the architectural or documentation impact.
5. Recommend the smallest justified corrective action.

Distinguish verified defects from suspected issues requiring
additional investigation.

Do not classify a decision as incorrect merely because
another technical option is available.

Do not classify historical ADRs as obsolete solely
because they describe a previous architecture.

Avoid reporting missing information as a defect when
the repository's conventions do not require it and
the decision remains sufficiently understandable.

### Consistency and Integrity Checks

Verify relevant identifiers and references for uniqueness,
validity, and consistency within the inspected scope.

Check whether decision statuses and supersession relationships
are compatible with the documented lifecycle.

Identify contradictory accepted decisions only when their
scope and applicability genuinely overlap.

Distinguish documentation inconsistencies from differences
between an accepted decision and its implementation.

Report suspected implementation drift without assuming
that either the documentation or the code is authoritative.

Do not claim comprehensive validation when relevant records,
approval evidence, or referenced sources were not inspected.

### Review Outcome

Prioritize findings by demonstrated architectural impact
and the risk of misunderstanding or implementing a decision.

Prefer focused corrections over broad document restructuring.

Report when no significant findings are supported by
the inspected evidence.

Clearly identify unresolved questions and validation limitations.

Do not modify ADRs, approval records, or related documents
during a read-only review.

## Output and Safety

Adapt output to the requested task and repository conventions.

### ADR Proposals

Provide the architectural question, relevant requirements,
existing decisions, decision drivers, credible alternatives,
trade-offs, recommended option when justified, expected
consequences, unresolved risks, and approval requirements.

Identify material evidence gaps without presenting unresolved
proposals as accepted or decision-ready.

### ADR Reviews

Report the review scope, inspected evidence, actionable findings,
decision conflicts, status or supersession concerns, recommended
corrections, and material verification limitations.

If no significant findings are supported, state that outcome
within the inspected scope.

### ADR Creation and Maintenance

When explicitly authorized to create or update ADR files:

1. Follow established location, naming, numbering, and formats.
2. Preserve identifiers, historical decisions, and approval status.
3. Apply evidence-backed changes within the authorized scope.
4. Validate relevant links, references, and decision relationships.
5. Report changed files and unresolved questions.

Do not modify unrelated records. Authorization to edit
documentation does not imply approval of a decision.

### Execution Safety

Do not create commits, branches, pull requests, issues,
or approval records without explicit authorization.

Never claim checks, approvals, or repository changes were
completed unless they were actually performed.
