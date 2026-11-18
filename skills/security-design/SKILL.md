---
name: security-design
description: Model threats and design application security controls from repository architecture. Use for feature or system threat models, trust-boundary analysis, and read-only reviews of how existing controls are enforced across application flows.
---

# Security Design

## Mode and Operating Limits

- Use **design** for a proposed feature, change, or control. Use **review**
  to assess existing behavior. For a mixed request, establish a shared
  baseline and report the review and proposal separately.
- Work read-only by default. Return guidance in the conversation unless
  the user requests an artifact. Require explicit authorization for
  implementation or changes to code, tests, configuration, or infrastructure.
- In review mode, use passive inspection and existing results. Describe
  proposed verification checks.
- In both modes, execute checks only with explicit
  authorization outside the read-only scope. Confirm the target, data
  handling, network destinations, and side effects before execution.
  Authorization must cover external calls, data transfers, and writes such
  as caches, artifacts, or database changes. Leave a check proposed if its
  behavior or authorization is unclear.
- Keep vulnerability scanning, diff-level vulnerability hunting, penetration
  testing, exploit development, and unauthorized active testing outside
  this workflow. Existing SAST, Dependabot, and other scanner results may
  be used as evidence within their scope and limitations.

## Sensitive Evidence

- Discover secrets through configuration key names, secret-store references,
  and redacted alerts. For targeted local inspection, use a verified
  metadata-only mode that returns safe locations such as file and line
  without match text. Keep values out of output, errors, and artifacts.
  Skip raw environment dumps and unredacted output from secret-bearing
  files, Git diffs, and logs. Ask for sanitized evidence if needed.
- Report a suspected or observed exposure by type and a safe locator such
  as a sanitized path and line, commit and path, or redacted alert ID.
  Redact the entire value and omit source excerpts that contain it. Keep
  values out of tool inputs, logs, reports, and examples. Never validate or
  use discovered credentials, including attempting authentication. Apply
  the same minimization to sensitive non-secret data such as personal
  records and confidential payloads. Use synthetic data for examples.
- Recommend private escalation to the credential owner. For an exposed
  credential, recommend prompt revocation and rotation through the project's
  incident process, including updating affected consumers. Deleting the
  current copy leaves possible exposure in Git history, clones, forks, logs,
  published artifacts, or backups. Identify confirmed and possible locations
  for authorized follow-up and cleanup.

## Repository Evidence and Threat Model

1. Read applicable repository instructions and identify the feature or
   system, revision, environment, and scope. Consult relevant requirements,
   ADRs, and security policies for intended behavior and constraints.
2. Inventory the assets and sensitive data in scope, their owners, and the
   users, service identities, other actors, and external dependencies that
   can interact with them. Trace relevant data and control flows from entry
   points to privileged actions, storage, logs, and integrations. Mark where
   authentication, privileges, tenancy, or administrative control changes.
3. Trace existing controls through relevant code, configuration,
   infrastructure, CI/CD, and tests. Locate enforcement points and covered
   paths. Assess authentication, authorization, secrets handling, input
   validation, data protection, logging, and deployment exposure where the
   flows warrant it.
4. Describe significant threat scenarios with the actor, prerequisites,
   boundary crossed, asset at risk, and plausible consequence given the
   controls in scope.

Cite safe paths and lines, symbols, test names, or decision IDs for the
evidence that supports the threat model and the review.

## Design Workflow

Start from the observed architecture and show how the proposed change affects
flows, trust boundaries, and control responsibilities. Define the security
requirement at the boundary and choose the component that has the context
and authority to enforce it. Prefer adapting existing controls and respecting
approved policies. Specify allowed behavior and what happens on denial or
control failure where relevant.

Compare viable options where the choice matters. Consider enforcement
coverage, failure behavior, compatibility, and operational cost as relevant.
Explain which trade-off drives the recommendation.

Return a proposal with the baseline and affected flows. For each significant
threat, link its reference and priority to the proposed requirement, control
and enforcement point, verification criterion, and residual risk. Record
material alternatives, assumptions, dependencies, and open decisions.

## Read-Only Review Workflow

Compare expected policy with actual enforcement along the in-scope paths.
Check shared controls and environment overrides before concluding a control
is missing. Name the evidence layer supporting each verified finding, such
as source code, checked-in configuration, a test definition, an observed test
result, or deployment evidence. Explain conflicts between those sources.
Static inspection alone cannot establish runtime effectiveness or security
assurance.

Return a report with the scope, revision and environment, material boundaries
and controls, and coverage limits. Label each entry by its evidence status.

- **Verified finding.** Give the confirmed gap, evidence layer and citation,
  scenario, and priority. Link a proportionate mitigation and verification
  criterion. Limit the claim to the conditions supported by the evidence.
- **Potential threat.** Give the scenario, relevant evidence, priority, and
  conditions affecting reachability or impact. Link related findings and
  mitigations where applicable. State what would confirm or rule out the threat.
- **Unverified assumption.** Name the premise, how it affects the assessment,
  and the evidence needed to resolve it.

Report remaining risks and unresolved verification. If no findings are
verified, state that result within the inspected scope.

## Priority and Verification

Give each significant risk a short reference and use the project's priority
scheme when available. Justify order by plausible impact and likelihood given
asset sensitivity, exposure, actor prerequisites, and existing control
coverage. Flag uncertainty that could change the order.

For each significant mitigation, name an existing or proposed check and its
environment or fixture, and give the observable pass condition. Distinguish
defined checks from observed results. State what risk would remain even if
the mitigation worked and what still needs evidence.

Use sibling skills for requested follow-on work. Pass boundary changes to
`architecture`, decision trade-offs to `adr`, security requirements to `prd`,
data invariants to `data-model`, documentation discrepancies to
`documentation-audit`, and verification planning to `test-strategy`.
