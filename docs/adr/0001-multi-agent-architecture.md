# ADR 0001 — Multi-agent architecture

**Status — Accepted.** D-01–D-30 define the architecture. Implementation and release verification are tracked in the [runtime matrix](../compatibility/multi-agent-runtime-matrix.md).

## Approval record

On 25 November 2026, the user explicitly approved the architecture in the Codex chat *Analyze issue #22 architecture*. The original documentation handoff states:

> The Canonical Core + Native Adapters architecture and consolidated decisions D-01–D-26 for issue #22 are explicitly approved.

The remediation handoff in the same chat at 16:57:09 UTC approves the additions and preserves the original register.

> Preserve approved decisions D-01–D-26 and incorporate approved decisions D-27–D-30:
>
> - Enforce the supported coordinator entry point; prevent unsupported allowlist bypasses.
> - Separate read-only orchestration from the explicitly authorized writer session.
> - Verify effective canonical skill provenance and address skill shadowing.
> - Distinguish native enforcement, workflow policies, and verification gates.

The register below records the architectural interpretation of this wording. The second independent review checked both approval messages against the local chat record. A shared GitHub approval reference remains pending before closing [issue #22](https://github.com/manueldellapa/Skills/issues/22).

## Context

[Epic #21](https://github.com/manueldellapa/Skills/issues/21) calls for one blueprint request to coordinate native specialists in Codex and Claude Code. The workflow supports greenfield and incremental projects, respects existing requirements and decisions, and produces traceable documentation with an independent audit. [Issue #22](https://github.com/manueldellapa/Skills/issues/22) is the architecture decision gate.

The [current catalog](../../README.md#skill-catalog) has nine independently invocable skills. Each has a canonical directory under `skills/` and relative discovery symlinks for both clients. The [existing CI](../../.github/workflows/validate-skills.yml) validates skills and symlinks. The design preserves these entry points and the existing standalone installation flow. The decision drivers are one source for domain methods and workflow rules, verified native delegation, least privilege, explicit approvals, and low maintenance overhead.

## Alternatives and rationale

| Alternative | Trade-off |
| --- | --- |
| Standalone skills with manual coordination | Preserves the simplest execution path. The user manages dependencies, conflicts, handoffs, and audit. Standalone use remains supported. |
| Independent native workflows | Gives each client control over its own workflow. Both implementations would carry the same role, dependency, approval, and readiness rules. |
| Canonical Core + Native Adapters | Shares the contracts and uses native controls at the boundaries. Requires validation of the hand-maintained adapters and a compatibility matrix scoped to tested configurations. **Accepted.** |
| Custom orchestration service or SDK runner | Offers programmatic scheduling and state management. Adds deployment, authentication, and runtime maintenance outside the epic scope. |

Manual thin adapters are proportionate to a catalog of nine roles. A generator could reduce duplication of metadata, with the added cost of templates, a renderer, and another maintenance path. The initial design uses strict static validation and runtime tests to check the manual definitions. On Claude Code, the custom root supplies a positive allowlist while invoking the same canonical workflow as Codex. A skill-only Claude entry point with deny rules would need to track every disallowed agent. [Runtime evidence](../compatibility/multi-agent-runtime-matrix.md#claude-code-poc)

## Accepted decision register

| ID | Decision |
| --- | --- |
| D-01 | Use Canonical Core + Native Adapters. Canonical skills define how work is done, role contracts define who owns it, and the workflow defines dependencies and gates. |
| D-02 | Use native named specialist subagents. Generic agents and root role-play cannot satisfy named delegation. |
| D-03 | The root agent coordinates the run. Codex uses the root session, and Claude Code uses a custom agent launched as the root. |
| D-04 | Share the canonical `project-blueprint` skill. Invoke it in the Codex root session and explicitly from the Claude Code root launched with `claude --agent project-blueprint-root`. |
| D-05 | Put the nine runtime-neutral specialist contracts in `roles/`. |
| D-06 | Maintain thin Codex TOML and Claude Code Markdown/YAML adapters manually. CI rejects unsupported fields, invalid references, and detectable drift. |
| D-07 | Define the workflow as a declarative YAML dependency DAG. |
| D-08 | Limit the initial workflow to two concurrent specialists. |
| D-09 | Delegate one level deep. Specialists have no coordination responsibility and cannot delegate within the workflow. |
| D-10 | Enforce read-only specialist work with native runtime controls. Verify the effective tool and filesystem boundaries. |
| D-11 | Use one authorized writer for canonical documentation. Specialists return drafts and evidence. |
| D-12 | Use structured handoffs and track completion of each required task. |
| D-13 | Allow one retry per transient failure. Surface persistent failures and blocked dependencies. |
| D-14 | Allow one automatic remediation cycle by the responsible role under the existing authorization, then repeat the independent audit. |
| D-15 | Keep the Documentation Auditor independent and read-only. The auditor reviews the integrated candidate and returns findings. |
| D-16 | Exclude worktree isolation from the first version. |
| D-17 | Keep models configurable by runtime within the declared compatibility scope. |
| D-18 | Use native client authentication. The default workflow requires neither a custom runtime nor an external API key. |
| D-19 | Use a positive specialist allowlist where the runtime can enforce it. The Claude root restricts `Agent(...)` to approved specialist types. Codex uses expected-role checks until an equivalent native control is verified. |
| D-20 | Require foreground specialist delegation on Claude Code in the first version. |
| D-21 | Gate the final verdict on explicit collection and validation of required task results. |
| D-22 | Declare support only for verified combinations of client version, model, launch mode, and relevant settings. |
| D-23 | Load skills through runtime-specific adapters. Codex specialists explicitly resolve and read the assigned canonical skill and provide evidence of use. Claude specialists use native `skills` preload. Missing or unusable skills block affected work. |
| D-24 | Keep domain instructions in the canonical `SKILL.md` files. Role contracts and adapters refer to those files and their skill IDs. |
| D-25 | Report explicit run states and fail closed on readiness. |
| D-26 | Separate read-only analysis from authorized writing. A separately authorized single-writer phase may apply the validated documentation changes within its declared scope. |
| D-27 | Enforce the supported coordinator entry point. Claude Code orchestration requires a verified custom main-thread root with the effective positive specialist allowlist. Block delegation when the required launch context is absent or unverified. |
| D-28 | Apply approved documentation changes through a separate, explicitly authorized writer session with technical path limits and no delegation. Hand the write back to the user if the runtime cannot enforce the limits. |
| D-29 | Verify the provenance and integrity of each required canonical skill as used by the root or specialist. Missing, shadowed, mismatched, or unverifiable effective skill content blocks readiness. |
| D-30 | Record native enforcement, workflow policies, verification gates, and human authorization distinctly. Verify compliance with runtime traces and the manifest. |

## Runtime entry points and boundaries

- **Codex.** Enable `project-blueprint` explicitly in the root session. Select native specialists from `.codex/agents/` by agent type and verify the effective role before accepting each result. Inherit a read-only root policy for specialist work. Resolve the pinned canonical skill through the installed project layout and have the child explicitly read and apply it. Ordinary skill availability and root-level reads are insufficient evidence of child execution. [Codex PoC](../compatibility/multi-agent-runtime-matrix.md#codex-poc)
- **Claude Code.** Launch `claude --agent project-blueprint-root` with an explicit `Agent(<approved specialist types>), Skill, Read` tool list. The root invokes the shared `project-blueprint` skill. Launch foreground specialists with explicit read-only tools and no `Agent` capability. The blueprint uses the explicit launch flag and leaves global agent settings and denylists to the user. [Claude Code PoC](../compatibility/multi-agent-runtime-matrix.md#claude-code-poc)

Before the Claude Code `project-blueprint` workflow delegates, verify that the effective main-thread profile is the project-approved `project-blueprint-root` and that it exposes the intended positive allowlist. Running the blueprint from an ordinary session, a specialist, or a shadowed root must stop that workflow before it starts any children. Users can still invoke specialists independently with D-10's read-only controls. Those calls are outside the blueprint allowlist and do not certify a blueprint run. Global agent settings and denylists stay outside the design.

Moving instructions to a readable resource or checking the root in a prompt alone provides no technical entry-point protection. If #25 and #26 cannot verify that the supported entry point is enforced, Claude blueprint orchestration stays blocked. A different structure for exposing the shared workflow would require explicit approval and corresponding amendments to D-04 and the repository layout before adoption. [Claude adapters #25](https://github.com/manueldellapa/Skills/issues/25) · [Coordinator #26](https://github.com/manueldellapa/Skills/issues/26)

### Authorized writer session

On either runtime, the writer is the main agent of a separate, explicitly launched write session. The analysis root and specialists stay read-only. After independent audit and explicit user write authorization, hand the writer the approved candidate, manifest, input revision, and authorized documentation paths. Bind authorization to that candidate and scope. Verify input revision, target state, and resolved paths before writing. Stale inputs or changed targets require reconciliation and renewed authorization where the approved scope changes.

The writer has the minimum read and edit capabilities needed for the handoff, technical write access limited to the approved documentation paths, and no delegation. Its task is to apply the reviewed changes. Requirements interpretation, new decisions, and unresolved findings go back to the read-only workflow. If the runtime cannot enforce the path and tool limits, return the candidate for the user to apply. A read-only post-write check compares the resulting diff with the approved candidate and verifies that only authorized paths changed. No additional specialist adapter is implied. [Codex adapters #24](https://github.com/manueldellapa/Skills/issues/24) · [Claude adapters #25](https://github.com/manueldellapa/Skills/issues/25) · [Coordinator #26](https://github.com/manueldellapa/Skills/issues/26)

The workflow covers documentation and excludes application implementation, deployment, source-control publication, and external system changes. Material architecture decisions require explicit user approval, including during autonomous draft work.

### Effective skill provenance

For each required skill, including the coordinator skill, record the skill ID, evidence for each check below, and its status (`verified`, `unverified`, or `mismatch`).

| Check | Required evidence |
| --- | --- |
| Source integrity | The expected canonical path in the intended checkout or pinned submodule, its Git revision, and the SHA-256 of its contents. |
| Resolution integrity | The effective source selected in the tested runtime and launch context. Inspect applicable discovery scopes and precedence, and resolve same-name collisions. An inventory and hash can support this check when the applicable resolution rules are verified. |
| Effective skill usage | Evidence that the relevant root or child received the expected content through the actual read, preload, or invocation and applied it to the task. Correlate the runtime event with the intended source and the result. |

Source and resolution integrity alone leave effective usage unverified. On Codex, bind the child's explicit read to the pinned canonical file and validate the resulting work. On Claude Code, verify effective usage for both root skill invocation and specialist preload. A synthetic body marker helps isolate a fixture outcome. A catalog entry, matching name, or agent self-report alone cannot establish production usage. Missing, shadowed, mismatched, or unverifiable skill content blocks affected work and prevents `ready`. If #25 cannot establish sufficient evidence for the approved Claude route, that route is a no-go. Any alternative loading design that departs from the approved decisions requires explicit approval. [Existing discovery rules](../../README.md#discovery-and-verification) · [Claude provenance gate](../compatibility/multi-agent-runtime-matrix.md#claude-code-provenance-gate)

### Enforcement and verification

| Control | Classification |
| --- | --- |
| Claude custom-root positive allowlist, specialist tool allowlists, and verified sandbox or path restrictions | Native enforcement within the effective runtime configuration. Apply the same evidence standard to a writer's path limits before enabling writes. |
| Two concurrent specialists, one level of delegation, foreground calls on Claude Code, and bounded retry and remediation | Workflow policies. Claim an additional native bound only when the exact runtime configuration demonstrates it. |
| Supported launch, effective role and skill provenance, trace and manifest checks, completion, independent audit, readiness, and post-write comparison | Verification gates. A policy violation or insufficient evidence blocks the affected gate. |
| Material decision approval and scoped writer authorization | Human authorization. Runtime tool access does not grant approval. |

Use native call and completion events and the run manifest to check foreground flags, overlapping tasks, depth, retry counts, and result coverage. An exit code or a final response cannot establish policy compliance or readiness.

## Workflow and handoffs

1. Discover project guidance, authoritative artifacts, revisions, and applicable roles. For greenfield work, establish the brief and draft requirements. For incremental work, record the existing baseline and proposed delta.
2. Establish requirements, then architecture and any proposed ADRs. Pause dependent work when a material choice requires approval. Record the approval reference before dependent work proceeds.
3. Run data, API, and security design on stable inputs. Schedule independent tasks within the concurrency cap and reconcile shared boundaries before downstream work. Run QA and operations planning when their design inputs are stable.
4. Assemble a candidate tied to the accepted handoffs and give the independent auditor that revision. Route blocking findings to the artifact owner for the bounded remediation cycle and repeat the audit against the revised candidate. Require separate write authorization before applying changes to canonical documentation.

Each handoff carries the task and role IDs, input revision, artifact references, relevant requirement and decision IDs, and expected ownership. Each result carries task status, evidence paths, assumptions, blockers, and a draft or output reference. The root records native child IDs where available, attempts, task status, artifact revisions, effective skill provenance, and unresolved approvals in the run manifest. Reuse a prior result only when its inputs and dependent artifacts still validate. Record why a role is inapplicable.

| Run state | Meaning |
| --- | --- |
| `ready` | Required tasks have validated results, applicable decisions are approved, and the independent audit passed on the integrated candidate. If writes were requested, applicable write and review gates also passed. |
| `blocked` | A required dependency, capability, or unresolved finding blocks further progress. |
| `partial` | Some results are usable and one or more required tasks are incomplete. |
| `failed` | An execution or validation failure prevents completion. |
| `awaiting_approval` | A required user decision or authorization is pending. |

An unsupported launch, missing or mismatched role identity, unverified skill provenance, invalid handoffs, required task failures, and blocking audit findings prevent `ready`. A requested but unauthorized write remains `awaiting_approval`. A write whose technical boundaries cannot be established is `blocked`.

## Repository layout

```text
skills/<domain>/SKILL.md                 # Existing canonical domain skills
skills/project-blueprint/SKILL.md        # Shared coordinator instructions
skills/project-blueprint/workflow.yaml  # Shared dependency DAG
roles/<role-id>.md                      # Nine canonical specialist contracts
.agents/skills/<name>                   # Codex discovery symlinks
.claude/skills/<name>                   # Claude Code discovery symlinks
.codex/agents/<role-id>.toml             # Thin Codex specialist adapters
.claude/agents/<role-id>.md              # Thin Claude specialist adapters
.claude/agents/project-blueprint-root.md
scripts/ and tests/                     # Validation and fixtures
docs/adr/0001-multi-agent-architecture.md
docs/compatibility/multi-agent-runtime-matrix.md
```

## Consequences

Both runtimes share domain methods, contracts, and acceptance criteria while keeping their entry points and permission enforcement native. The single writer serializes integration and limits write contention. The two-worker cap and Claude foreground requirement favor observable completion. Runtime behavior varies with model, launch mode, and permissions, and manually maintained profiles need drift checks. Claude Code's positive root allowlist and Codex's expected-role checks provide different guarantees.

Proofs of concept establish feasibility for the specific configurations tested. The [runtime matrix and verification ownership](../compatibility/multi-agent-runtime-matrix.md#pending-implementation-verification) record what remains before release.
