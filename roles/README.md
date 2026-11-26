# Canonical specialist role contracts

These runtime-neutral contracts define who owns each specialist result in the
multi-agent blueprint. Canonical skills define how domain work is performed;
these contracts define inputs, outputs, ownership, evidence, escalation, and
handoffs. Runtime adapters and the coordinator must refer to the contracts and
skills rather than copying their instructions.

The contracts implement [ADR 0001](../docs/adr/0001-multi-agent-architecture.md),
especially D-05, D-09–D-12, D-15, D-23–D-30. They do not define runtime tools,
models, permissions, scheduling, retries, or readiness logic.

## Role catalog

| Role ID | Title | Canonical skill | Owned artifact type |
| --- | --- | --- | --- |
| `product-analyst` | Product Analyst | [`prd`](../skills/prd/SKILL.md) | `product-requirements` |
| `software-architect` | Software Architect | [`architecture`](../skills/architecture/SKILL.md) | `software-architecture` |
| `decision-analyst` | Decision Analyst | [`adr`](../skills/adr/SKILL.md) | `architecture-decision` |
| `data-architect` | Data Architect | [`data-model`](../skills/data-model/SKILL.md) | `data-design` |
| `api-architect` | API Architect | [`api-contracts`](../skills/api-contracts/SKILL.md) | `api-contract` |
| `security-architect` | Security Architect | [`security-design`](../skills/security-design/SKILL.md) | `security-design` |
| `qa-architect` | QA Architect | [`test-strategy`](../skills/test-strategy/SKILL.md) | `verification-strategy` |
| `devops-engineer` | DevOps Engineer | [`operations-runbook`](../skills/operations-runbook/SKILL.md) | `operations-runbook` |
| `documentation-auditor` | Documentation Auditor | [`documentation-audit`](../skills/documentation-audit/SKILL.md) | `documentation-audit` |

## Contract format

Each `roles/<role-id>.md` file begins with exactly these identity fields:

```yaml
---
role: product-analyst
title: Product Analyst
skill: prd
---
```

The filename must equal `role`. `skill` identifies exactly one canonical
`skills/<skill>/SKILL.md`. The remaining sections appear in this order:

1. Purpose and canonical skill
2. Required inputs
3. Artifact ownership and outputs
4. Boundaries
5. Evidence requirements
6. Escalation and blocking conditions
7. Handoffs

Role contracts remain concise and link to domain methods in the canonical
skill. They must not carry runtime-specific agent configuration.

## Common operating contract

- Specialists are read-only, do not delegate, and do not coordinate other
  specialists. In blueprint execution they return drafts, findings, and
  evidence only to the coordinator. In standalone execution they return the
  result only to the direct invoker.
- Specialists do not modify documentation, code, tests, schemas,
  configuration, infrastructure, issue trackers, source control, or external
  systems. The separate, explicitly authorized writer described by ADR 0001
  applies an approved candidate.
- A direct invocation of a named specialist uses the same read-only contract.
  Standalone use of a canonical skill remains a separate workflow. A standalone
  specialist result is not blueprint-certified and must not be treated as
  accepted blueprint evidence without current external validation of its
  inputs, exact result revision, native identity, and skill provenance.
- For a role invocation, this common contract and the role-specific boundaries
  take precedence over canonical skill instructions about writes, artifact
  creation, or execution. Those instructions become returned drafts or proposed
  checks. Even an explicit write or execution request does not relax the role;
  it requires the separate writer, a separate execution task, or user action.
  Standalone invocation of the canonical skill outside a specialist role keeps
  the skill's own behavior.
- A role may own an artifact semantically without owning the filesystem path.
  The coordinator assembles contributions, and the authorized writer has only
  temporary write custody of approved target paths.
- A contributing role does not become a co-owner. It reports the proposed
  change or constraint and its intended semantic owner; the coordinator or
  direct invoker performs any routing.
- Material decisions remain proposals until the documented approval process
  supplies an approval reference. Runtime access never grants approval.
- A specialist reports only its task status. It must not claim that the whole
  blueprint run is `ready`.

## Claim and evidence model

Every material claim in a result is classified as a `fact`, `assumption`,
`proposal`, or `decision` and marked `verified` or `unverified`. This is the
producing specialist's first-party evidence assessment, not independent
validation.

- A verified fact cites an inspectable source such as a repository path and
  line, symbol, test, issue URL, decision ID, or sanitized runtime record.
- An assumption is `unverified`; it states the missing evidence and its effect
  on the result. Once supported, restate it as a fact.
- A proposal may be `verified` only in the limited sense that cited evidence
  supports its basis or feasibility. That status never means the proposal is
  approved, implemented, or observed in operation.
- A decision preserves the lifecycle status used by its authoritative source.
  Decision evidence adds `decision_id`, `decision_status`, and `approval_ref`.
  `verified` means the cited record and status were inspected; the specialist
  does not grant approval. An accepted decision requires a nonblank approval
  reference.

The Documentation Auditor's finding status `needs verification` maps to
`verification: unverified`; its `verified` status maps to
`verification: verified`.

Independent verification is performed by an actor other than the specialist
that produced the claim. In blueprint execution, the Documentation Auditor
records its evidence and findings against the integrated, fixed-revision
candidate in the `documentation-audit` artifact. The runtime or coordinator
separately records native role identity and skill provenance in the validation
record; that record does not verify the substantive truth of specialist claims.
In standalone execution, the direct invoker or an independently appointed
reviewer may record verification evidence in a separate, revision-bound review
record, or in the existing `documentation-audit` artifact when that role is
invoked. A standalone result requires no blueprint validation record. Without a
separate independent review, it remains usable as specialist-reported analysis,
but it is neither independently verified nor certified for blueprint use.

For blueprint acceptance, the specialist cannot establish its own native
identity or effective skill usage merely by reporting them. The runtime or
coordinator appends and checks that evidence in the validation record below;
standalone use does not create or require that blueprint record.

## Structured handoff bundle

For blueprint execution, the complete handoff bundle consists of a task
request, a specialist result, and a validation record. A standalone invocation
uses the task request and specialist result, returns them to the direct invoker,
and requires neither a blueprint validation record nor blueprint acceptance.
Any optional independent standalone evidence remains separate from this bundle,
is bound to the result revision, and adds no required schema field.
Implementations may serialize the YAML as another lossless structured
representation, but field names and semantics remain stable.

### Task request

```yaml
task_request:
  task_id: TASK-001
  role_id: product-analyst
  context: blueprint
  objective: Define the requested requirements delta.
  input_revision: git:<commit-or-other-stable-revision>
  inputs:
    - artifact_ref: current-prd
      path: docs/prd/example.md
      revision: sha256:<digest>
      state: existing
      owner_role: product-analyst
  requirement_ids: [FR-001]
  decision_ids: [D-01]
  assumptions:
    - assumption_id: ASM-001
      statement: The referenced PRD is the current product baseline.
      effect: A stale baseline would invalidate the proposed delta.
  known_blockers:
    - blocker_id: BLK-001
      summary: Approval authority for D-01 is not identified.
      resolution_needed: Identify the documented approving authority.
      evidence_ref: null
  expected_outputs:
    - artifact_type: product-requirements
      owner_role: product-analyst
      target_path: docs/prd/example.md
```

`state` distinguishes an `existing`, `proposed`, or `not-created` artifact.
A target path expresses the intended canonical destination; it is not proof
that a file exists or was written.

For a plain-language standalone invocation, the invoked specialist normalizes
the request into this same `task_request` structure before analysis and returns
it with the result. It sets `context: standalone`, derives the role, objective,
scope, identifiers, and expected outputs only from the invocation and
inspectable inputs, and records the most specific stable input revision
available. It does not invent missing values. A missing input that materially
limits the task is recorded in `known_blockers` and in the result's `blockers`,
with the absent evidence identified; the result status then follows the
deterministic rules below. A preformatted request is not required when the
plain-language objective and available evidence can be normalized without
guessing.

### Specialist result

```yaml
specialist_result:
  task_id: TASK-001
  role_id: product-analyst
  context: blueprint
  return_to: coordinator
  status: blocked
  input_revision: git:<commit-or-other-stable-revision>
  output_refs:
    - artifact_type: product-requirements
      owner_role: product-analyst
      target_path: docs/prd/example.md
      state: proposed
      content_ref: result:TASK-001/requirements-delta
      revision: sha256:<digest>
  skill_usage_claim:
    skill_id: prd
    resolved_path: <resolved-canonical-skill-path-or-null>
    content_digest: <sha256-digest-or-null>
    status: unverified_self_report
  evidence:
    - claim_id: CLAIM-001
      classification: fact
      verification: verified
      source_ref: path/to/source:42
  assumptions:
    - assumption_id: ASM-001
      statement: The referenced PRD is the current product baseline.
      effect: A stale baseline would invalidate the proposed delta.
  blockers:
    - blocker_id: BLK-001
      summary: Approval authority for D-01 is not identified.
      resolution_needed: Identify the documented approving authority.
      evidence_ref: null
  approval_requests:
    - approval_id: APR-001
      subject: D-01
      decision_needed: Confirm whether D-01 applies to this scope.
      approving_authority: <documented-authority-or-null>
  handoff_suggestions:
    - role_id: software-architect
      reason: Assess the architecture impact of the requirements delta.
```

`context` is `blueprint` or `standalone`. `return_to` is `coordinator` for
blueprint execution and `direct_invoker` for standalone execution. A handoff
suggestion names an intended downstream role and reason; it does not contact,
delegate to, or coordinate that role.

`skill_usage_claim` records what the specialist reports resolving and reading.
Its status is always `unverified_self_report`, including when a path and digest
are supplied. It never substitutes for the externally corroborated validation
record required for blueprint acceptance by D-23 and D-29.

Assumptions, blockers, and approval requests use the minimal structures shown
above. Use an empty list when none apply; do not replace entries with free-form
strings. `evidence_ref` and `approving_authority` may be `null` only when their
absence is itself reported as a gap.

Select exactly one specialist task status by applying these rules in order:

1. `failed`: execution or contract validation failed without a usable required
   result.
2. `blocked`: an unresolved dependency, capability, or evidence failure
   prevents required progress. This takes precedence over partial outputs and
   pending approvals.
3. `awaiting_approval`: no blocker remains and the next required progress
   depends on a material decision or authorization. This takes precedence over
   `partial` when approval is the only remaining gate.
4. `not_applicable`: the assigned scope does not require the role and no
   substantive output is needed; the result states why.
5. `partial`: usable output exists, no blocker or approval gate remains, and
   required work is incomplete.
6. `complete`: all requested outputs are supplied and no blocker or pending
   approval remains.

The example result is `blocked` because `BLK-001` remains unresolved; its
proposed output and pending approval request do not change that status.

The coordinator alone derives the run states defined by ADR 0001, including
`ready`.

### Validation record

```yaml
validation_record:
  task_id: TASK-001
  role_id: product-analyst
  result_revision: sha256:<exact-specialist-result-digest>
  native_child_id: <runtime-child-id-if-available>
  attempt: 1
  native_role_identity:
    status: verified
    evidence_ref: trace:<event-reference>
  skill_provenance:
    status: verified
    skill_id: prd
    expected_path: skills/prd/SKILL.md
    git_revision: <pinned-revision>
    sha256: <canonical-content-digest>
    source_integrity:
      status: verified
      evidence_ref: manifest:<source-check>
    resolution_integrity:
      status: verified
      evidence_ref: trace:<resolution-check>
    effective_usage:
      status: verified
      evidence_ref: trace:<usage-check>
```

Each validation status is `verified`, `unverified`, or `mismatch`. A missing,
unverified, or mismatched native identity or required provenance check prevents
acceptance of the result and therefore prevents a `ready` run.

The overall `skill_provenance.status` is `verified` only when every required
subcheck is verified, `mismatch` when any subcheck mismatches, and `unverified`
otherwise. The validation record applies only to `result_revision`; changing
the specialist result invalidates the record and requires new external
validation. Evidence from one result must not be reused for another digest.

## Ownership and conflict resolution

The catalog defines the complete initial set of stable artifact type IDs. Each
type has exactly one semantic owner. More specific drafts remain distinguished
by `artifact_ref` or `content_ref`; they do not create new ownership types.
When a document contains several concerns, ownership follows the content being
changed rather than the enclosing file:

- Product requirements belong to the Product Analyst.
- Architecture boundaries belong to the Software Architect.
- Decision status and rationale belong to the Decision Analyst, while
  stakeholders retain approval authority.
- Data, interface, security, verification, and operations artifacts belong to
  their corresponding specialist. Domain-specific requirements, constraints,
  and verification criteria are contributions to the Product Analyst's
  `product-requirements` artifact or QA Architect's `verification-strategy`,
  not competing ownership claims.
- Audit findings belong to the Documentation Auditor. The auditor never owns
  or edits the candidate it reviews.

The coordinator routes conflicting contributions to the semantic owner. A
conflict that changes a material architectural choice goes through the
Decision Analyst and the documented human approval process.

## Result routing and handoffs

During blueprint execution, specialists return results only to the coordinator.
They identify intended downstream roles in `handoff_suggestions`; they do not
contact, invoke, delegate to, or reconcile directly with another specialist.

1. Product analysis establishes the requirements baseline and delta.
2. Software architecture establishes boundaries and identifies material
   decisions. The Decision Analyst prepares or reviews the corresponding
   decision artifacts.
3. Data, API, and security work consume stable requirements, boundaries, and
   approved decisions. Boundary conflicts return to the Software Architect or
   Decision Analyst through the coordinator.
4. QA and operations work consume stable design inputs.
5. The coordinator assembles a candidate tied to accepted handoffs and gives a
   fixed revision to the Documentation Auditor.
6. Blocking audit findings return through the coordinator to the semantic
   owner. The auditor reviews the revised candidate after the bounded
   remediation cycle.
7. Applying the accepted candidate belongs to the separately authorized writer
   session and is not a specialist handoff.

During standalone execution, the specialist returns the result only to the
direct invoker. The direct invoker decides whether and how to use handoff
suggestions. A standalone result is not an integrated candidate, does not pass
the blueprint audit or readiness gates, and cannot be admitted to a blueprint
run until the coordinator revalidates current inputs, the exact result revision,
native role identity, and skill provenance.
