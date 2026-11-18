---
name: test-strategy
description: Plan and review risk-based verification for repository changes. Use when mapping requirements and acceptance criteria to existing or proposed checks, identifying test gaps, and defining pass/fail evidence in the project's test and CI environments.
---

# Test Strategy

Produce a verification plan ordered by risk. Show how each critical
requirement will be checked and what evidence is needed to judge the result.

## Purpose and Operating Limits

- Inspect the repository and available results in read-only mode by default.
  Return the plan in the conversation unless the user requests another format.
- Create or modify tests only when explicitly requested. Treat executing
  checks and changing repository files or CI configuration as distinct actions.
- Before executing a check, confirm it is within the requested scope and
  inspect its target and side effects. Use an isolated test environment for
  checks that write data or artifacts, and get authorization for side effects
  outside the granted scope. This includes caches, snapshots, test databases,
  remote CI jobs, and calls to external services. If execution is out of scope
  or the target is uncertain, describe the check in the plan.
- Use the project's canonical sources for requirements and acceptance criteria,
  including PRDs, issues, specifications, or contracts as applicable.
  Use architecture decisions for component boundaries and `data-model`
  artifacts for data invariants and migration constraints. Link to these
  inputs and surface conflicts or ambiguities for resolution at the source.

## Repository Discovery

1. Read applicable repository instructions. Identify the change or behavior
   under review, its baseline or revision when available, and the requirements,
   acceptance criteria, or contracts that define the expected behavior.
2. Follow affected entry points, interfaces, and dependencies to locate the
   relevant implementation, tests, fixtures, runner configuration, and CI
   jobs. Check which suites are selected, skipped, or conditional when this
   affects confidence. Inspect existing reports or run logs if available.
3. Note the project's actual framework, test levels, commands or manual
   procedures, and environment constraints. Cite the specific sources used,
   such as a requirement ID, path and line, test name, or CI job.

Scope discovery to the affected behavior. Record inaccessible or uninspected
areas when they limit a conclusion. Where sources disagree, identify the
conflict and its effect on the plan.

## Risk Prioritization

Describe concrete failure modes and their consequences. Prioritize them by
impact and plausibility using evidence from the change, existing behavior,
dependency boundaries, or known regressions. Flag uncertainty that could
change the order.

Consider critical paths, boundary and failure cases, regressions, and
nonfunctional risks relevant to the change. Include concerns such as
compatibility, performance, data integrity, or recovery when the requirements
or repository evidence justify them. Use the team's existing priority scheme
if it fits. A short rationale is sufficient when no scheme exists.

## Verification Design

For each prioritized failure mode, choose the lowest-cost verification level
that can reliably expose it under representative conditions. Consider setup,
execution time, maintenance, and the risk that substitutes hide the failure.
Explain when more than one level adds distinct evidence.

- Use unit checks for isolated rules or boundary values when dependencies
  are irrelevant to the failure.
- Use integration checks when persistence, transactions, or component
  interactions determine the result. Use contract checks when compatibility
  between a producer and a consumer is the behavior under test.
- Use end-to-end checks when the critical risk depends on a full workflow.
  Use operational checks when deployment, load, observability, or recovery
  behavior needs evidence from a representative environment.

Reuse existing cases and tooling when their assertions and setup exercise the
risk. Where a check needs capabilities the repository has yet to establish,
state the prerequisite and mark the check as proposed. Derive the mix of test
levels from risk, architecture, and cost. Use coverage metrics only where
they help answer a project-specific verification question.

## Requirements-to-Test Traceability

Map each critical requirement or acceptance criterion to a concrete existing
or proposed check, or to a documented gap. Reuse stable IDs or cite the source
and location. Reference the existing acceptance criterion and describe the
observable result for the particular scenario. If the requirement has no
clear expected outcome, record the decision needed to define pass/fail.

Use individual mappings for critical requirements and distinct failure
modes. Group lower-risk checks where they exercise the same behavior and
references remain clear. Reuse a case across requirements only when its
assertions support each mapping.

Record these conditions independently when applicable:

- **Missing test.** The relevant tests were inspected and no case was found
  that exercises the behavior with a suitable assertion. State the search
  scope and propose a check when feasible.
- **Not inspected.** A relevant suite, job, or other source was unavailable
  or outside the inspection scope. Identify what remains to inspect.
- **Execution evidence absent.** A case is defined, but its execution or
  outcome for the relevant revision and environment is unverified. Cite any
  older or partial results with their limitations.

## Verification Evidence and Output

Start with scope, sources, and material inspection limits. Present a table or
list ordered by risk. For each priority check, include:

- Requirement reference, failure mode, and reason for the priority.
- Existing case and its repository reference, proposed case and its intended
  scenario, or a gap and what would resolve it.
- Verification level, environment, and relevant prerequisites and test data.
  Use an established command, CI job, or manual procedure when known. State
  what must be established for a proposed check to be executable.
- Observable pass and fail conditions and the evidence to collect, such as
  an assertion result, test report, measured value, or run log.

Report observed outcomes only when supported by execution evidence. Cite the
case or job, relevant revision and environment, and result where available.
Check that the evidence shows the relevant case ran and evaluated the expected
condition. Flag skipped cases, incomplete results, and results for a different
revision or environment when they affect confidence.

Close with unresolved gaps, blocked checks, and residual risks. Check that
each critical requirement has a verifiable case or an explicit gap, that
priority and test level have a rationale, and that observed outcomes can be
traced to their execution evidence.
