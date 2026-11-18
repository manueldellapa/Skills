---
name: operations-runbook
description: Write or review repository-based runbooks through passive inspection. Use when documenting deployment, validation, monitoring, troubleshooting, rollback, backup, restore, or recovery.
---

# Operations Runbook

## Scope and Operating Limits

Identify the procedure, service, intended operator, target environment, and
repository revision. Read source files, approved references, and existing
results. Inspect scripts as text.

Treat dry runs, plan or diff commands against operational targets, smoke checks,
health probes, live queries (including read-only queries), and running project
scripts for discovery as active checks. During runbook work, describe them for
the operator and cite existing results. Perform active checks or operational
changes only in a separate execution task explicitly authorized for the action,
target, and side effects.

## Repository and Environment Discovery

1. Read applicable repository instructions, existing runbooks, and policies.
   Trace the supported entry points through deployment scripts, manifests,
   runtime configuration, environment overrides, and CI/CD definitions. Check
   which jobs build, validate, publish, or deploy and under which conditions.
2. For the target environment, identify the actual tooling, artifact or release
   version, configuration sources and precedence, required access, approval
   gates, and dependencies. Identify the owner, operator, decision authority,
   and escalation contact or role. Flag gaps and source conflicts. Block affected
   production steps when ownership, escalation, or a required decision remains
   unresolved.
3. Identify steps that depend on network access, such as fetching dependencies
   or artifacts, resolving hosts, or reaching a secrets service. For offline or
   restricted environments, use documented internal endpoints, mirrors, caches,
   or pre-staged artifacts and establish availability from existing evidence.
   Mark affected steps blocked when a dependency or permitted route
   cannot be established.

Ground existing and proposed steps in repository evidence for the target's
tooling, entry points, and constraints. Cite repository sources or official
documentation for the version in use to support syntax and parameters. Verify
applicability to the target from the available evidence. Include the working
directory and how to obtain environment-specific values. If syntax, an entry
point, or compatibility is unknown, describe the gap and evidence needed and
omit the unconfirmed command.

## Procedure Format

- State the objective, target, revision or artifact, owner or operator role,
  prerequisites, and conditions for starting. Include required configuration,
  access, and any applicable change window or approval.
- Order steps by dependency. For each step, give the action, expected outcome,
  observable check, and what to do if the check fails. Identify checkpoints
  before changes that are hard to reverse.
- For deployment, cover applicable preparation, rollout, and post-deploy
  validation. Include existing health or smoke checks and the service or data
  behavior they verify. For monitoring, specify available signals, observation
  windows and thresholds when established, and escalation conditions. Expose
  gaps where those criteria are needed but undefined.
- For troubleshooting, tie observable symptoms to supported diagnostics,
  decisions, and escalation paths.
- End each procedure with success criteria, evidence to retain, unresolved
  prerequisites, and residual risks.

## Failure, Rollback, and Recovery

For each material failure mode, identify the stop condition and establish which
steps took effect before attempting another action. Record how to inspect
partial state, which steps are safe to retry, and when the operator should
escalate. Treat uncertain state or an unconfirmed target as a stop condition.

Identify the last safe rollback point, the compatible prior release or
configuration, and checks for restored service and data integrity. Account for
schema changes and writes that may outlive a release rollback. State who decides
and what evidence favors rollback, a fix-forward, or escalation to recovery.
Where rollback is unavailable or insufficient, describe the supported recovery
path and its checks, or flag the decision needed before proceeding.

## Destructive Operations, Secrets, and Data Protection

- For steps that can delete or overwrite data or interrupt service, identify
  the exact target, impact, prerequisites, recovery options, and required
  authorization before the step. Stop if the target, authorization, or a
  required recovery prerequisite cannot be confirmed.
- Use key names and approved secret-store references. Inspect only necessary
  metadata and use sanitized evidence. Specify an approved way for the operator
  to supply secrets without exposing them through arguments, tracing, debug
  output, or dumps. Escalate suspected exposure privately via the project's
  security process using a safe locator and omitting the value.
- For backup, identify the data scope, approved storage, recovery point, and
  completion and integrity checks. For restore, verify the source copy and
  destination separately and ensure the restore cannot overwrite its source.
  Confirm compatibility and expected data loss or overwrite. Establish a
  technology-appropriate consistency strategy for concurrent writes and a way to
  preserve the prior destination state if it is at risk. Define when writes
  may resume or traffic may switch based on data integrity and service checks.
  Record backup integrity separately from recoverability. Claim verified
  recoverability only with evidence of a successful applicable restore and its
  checks. Propose isolated restore verification where supported when evidence
  is missing.

## Evidence and Output

For each critical step, cite an applicable source by path and line, symbol,
job, or existing runbook section. Record both dimensions of evidence:

- **Origin** — documented by an existing source or proposed for review. Cite the
  source for a documented step. State what a proposal depends on or what evidence
  is missing before it can be used.
- **Execution** — tested with observed evidence or unverified. For tested steps,
  cite the run, log, or report and record the revision, environment, date, and
  actual outcome, including failures. Compare the revision or artifact,
  environment, and conditions with the target. State differences and whether
  they affect the result. Mark steps unverified for the target when evidence is
  stale, materially different, or of uncertain applicability. Limit partial
  results to the steps they cover.

Return the draft or review in the conversation by default. When file edits are
requested, update the applicable canonical runbook if one exists. In a review,
report the affected step, evidence, operational consequence, and correction or
open decision.

Use outputs from `prd`, `architecture`, `adr`, `data-model`, and `api-contracts`
for requirements, topology, decisions, data constraints, and contract
compatibility. Route follow-up work on security controls and sensitive evidence
to `security-design`, verification planning to `test-strategy`, and cross-cutting
documentation audits to `documentation-audit`.
