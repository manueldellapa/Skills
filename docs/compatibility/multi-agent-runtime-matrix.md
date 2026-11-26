# Multi-agent runtime compatibility and PoC evidence

This matrix records the local CLI experiments for [issue #22](https://github.com/manueldellapa/Skills/issues/22). The tests ran on 25 November 2026 on macOS arm64 in disposable projects. The excerpts below retain selected event fields and synthetic fixture values. Session identifiers, absolute paths, account details, and full transcripts are omitted. The reproduction recipes use synthetic inputs.

[ADR 0001](../adr/0001-multi-agent-architecture.md) records the accepted design. Both PoCs reported native named delegation in their tested configurations. Release verification of the implemented blueprint is pending [#28](https://github.com/manueldellapa/Skills/issues/28).

## Evidence and review scope

- **Independently checked.** The Claude Code documentation reviewer compared the Claude claims with the original Claude event streams and checked selected Codex markers and errors in the outer coordinator chat records. The reviewer checked both CLI versions. This was an evidence review of existing runs.
- **Reported by the Codex PoC author.** The initial named-child traces, later sandbox and file-read results, and synthetic catalog and marker checks came from disposable Codex homes and sanitized excerpts. The independent reviewer lacked access to the isolated raw Codex child traces. A corroborated marker in the outer chat does not independently verify an underlying child event.
- **Pending.** The release gate requires fresh, inspectable evidence for the implemented workflow and the effective configuration. A vendor-documented capability or a reproduction recipe alone carries no release verification.

## Capability matrix

| Capability | Codex CLI `0.144.1` | Claude Code `2.1.326` |
| --- | --- | --- |
| Tested model and launch | `gpt-5.6-luna` at the root and explicitly in each role TOML. Non-interactive `codex exec --json`, trusted project, local session state, existing ChatGPT authentication. | `claude-haiku-5-5`, authenticated print-mode runs with `stream-json`. The reviewed streams reported `apiKeySource: none`. |
| Native role format and discovery | **Reported.** Custom TOML roles in `.codex/agents/` appeared in the role inventory. Child metadata carried the requested `agent_role`. | **Review-checked.** The runtime loaded Markdown/YAML agents from `.claude/agents/` and launched a custom main-thread agent with `--agent`. |
| Skill discovery and body loading | **Reported.** A synthetic relative symlink produced a child catalog entry. The clean child result omitted the body-only marker. A root-level invocation read the canonical target and the fresh child still omitted the marker. A separate probe recorded explicit child reads of the canonical file by resolved path. **Pending.** Verify the shipped adapter's effective source, installed path resolution, and application. | **Review-checked.** Native `skills` preload delivered the enabled project symlink sentinel. The disabled sentinel result omitted its marker. Identical personal copies confounded the two domain-skill source checks. **Pending.** Verify the effective canonical source for the coordinator and each specialist, including collisions. |
| Named delegation, concurrency, and completion | **Reported.** Two depth-one children launched before the first wait and the root collected both completed results. Fresh child context was requested. | **Review-checked.** Named children had overlapping execution intervals. Foreground probes collected available replies in one result. A background probe returned an incomplete result followed by a later result. Run B demonstrated three concurrent specialists. The approved cap of two and foreground requirement are workflow policies. |
| Read-only specialist controls | **Reported.** Children inherited `read-only` and `never`. One write attempt hit an OS permission error. The other hit patch syntax validation. | **Review-checked.** A `Read, Grep` specialist reported no write tool. The trace recorded a separate `Write` denial under `dontAsk`. A misspelled `tool` field left write-capable tools available. |
| Supported entry point and positive allowlist | **Reported.** The coordinator stopped before spawning on an absent role. A valid child surfaced a missing skill path. **Pending.** Native positive allowlist and adapter-level failure handling. | **Review-checked.** A custom main-thread root with `Agent(spec-arch, spec-adr)` rejected a registered, unlisted specialist. Skill-only controls delegated through the ordinary root. **Pending.** Verify the blueprint stops before delegating on unsupported launches and direct read-only specialist use still works. |
| Filesystem isolation and writer | **Reported.** Children shared the disposable checkout under the root sandbox. **Pending.** Verify a separate authorized writer's path bounds and no-delegation controls. | **Review-checked.** An isolated fixture wrote to a disposable worktree. V1 excludes worktrees. **Pending.** Verify a separate authorized writer's path bounds and no-delegation controls. |
| Workflow readiness | **Pending.** Named results and native wait events cover part of the completion gate. | **Pending.** Run D identified an incomplete task and emitted a completion marker. A `ready` verdict requires the approved trace, manifest, and audit checks. |

Vendor documentation describes the broader capability surface. Codex documents skill discovery and inherited session controls. Claude Code documents skill preload, scoped permissions, and the `Agent(...)` restriction for custom main-thread agents. The observations above apply to the version, model, and launch mode in the first row. [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Codex skills](https://learn.chatgpt.com/docs/build-skills) · [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) · [Claude Code CLI](https://code.claude.com/docs/en/cli-reference)

## Codex PoC

### Reported results and corroboration

The following results summarize the author’s PoC. The independent reviewer corroborated selected outer-log strings, including `ALL_CHILDREN_COLLECTED_22`, `Operation not permitted`, and `could not resolve the child model`. Child-level and exact-path assertions retain author-reported status.

- The initial successful named-agent run used `gpt-5.6-luna` in both role profiles and kept session state in the disposable Codex home. Two child traces carried depth `1`, returned their private-to-the-fixture role markers and file values, and matched the results in the root's wait events. Without `model` in the role TOML, an earlier Luna run exposed the role selector but failed with `could not resolve the child model for service tier validation`.
- In the targeted follow-up, the recorded roles were `skill-probe-alpha` and `skill-probe-beta`. Both children read the canonical architecture file by its resolved absolute path. Alpha's `touch denied-alpha.txt` returned exit `1` and `Operation not permitted`. Beta submitted a malformed patch, so its `write_denied` self-report shows no sandbox decision. Neither target file appeared. Both children completed before the root emitted `ALL_CHILDREN_COLLECTED_22`.
- In the trusted missing-skill run, the named child checked the specified path, returned `{"skill_loaded":false,"missing_skill":true,"done":true}`, and the root collected it. In the missing-role run, the root emitted `MISSING_ROLE_FAIL_CLOSED_22` after checking the inventory. That run made no spawn call. It verifies coordinator behavior on an absent role and leaves native enforcement of a positive allowlist pending.
- Sol under `--ephemeral` failed in the tested invocation with `no thread with id`. With local session state, the tested Sol path spawned generic children with `agent_role: null`. The account rejected `gpt-5.5` as outside its accessible catalog. The first nested Codex attempt also encountered a DNS restriction before delegation. These outcomes are specific to the tested configurations.

The later synthetic run used the sole discovery link `.agents/skills/skill-probe-auto -> ../../skills/skill-probe-auto`. The named child’s developer context contained the **available-skill catalog entry**, including the description and resolved target path. It lacked the body-only marker. The child located and read `alpha.txt` and returned the following result through native wait.

```json
{"role":"AUTO_ALPHA_22","fixture":"synthetic-alpha-fixture-22"}
```

In the explicit-invocation control, the root ran `sed` on the resolved canonical synthetic `SKILL.md` and its tool output contained `SYNTHETIC_SKILL_AUTO_22`. The fresh child returned the same role and fixture only. The control observed a root file read. The clean child run observed discovery metadata, no skill-file read, and no evidence that the child received or executed the skill body. Earlier synthetic attempts included coordinator-supplied collection markers and are excluded from the skill-body check.

### Reproduce with synthetic inputs

1. In an empty disposable Git repository, create `skills/skill-probe-auto/SKILL.md` with `name: skill-probe-auto`, a description, and an instruction in the body to return `"skill_execution":"SYNTHETIC_SKILL_AUTO_22"`. Keep the marker out of the role profile, root prompt, and delegation message. Create `alpha.txt` containing `synthetic-alpha-fixture-22` and the relative link:

   ```sh
   mkdir -p .agents/skills
   ln -s ../../skills/skill-probe-auto .agents/skills/skill-probe-auto
   ```

2. Define `.codex/agents/auto-skill-alpha.toml` with `name = "auto-skill-alpha"`, a `description`, and `model = "gpt-5.6-luna"`. In `developer_instructions`, tell the child to use the discovered skill, read only `alpha.txt`, and add `role: AUTO_ALPHA_22` and the fixture value to its result. For the automatic-loading check, prohibit explicit skill-file reads by either parent or child. Use a trusted disposable project with an isolated Codex home and native authentication. Keep local session traces enabled and set approval policy to `never` for the read-only probe.
3. From the fixture root, launch the named-role probe and save its event stream outside the fixture. Read the root and child traces. Require the requested `agent_role`, depth `1`, and a successful fixture read. Check the catalog entry, child tool calls, and body-only marker independently.

   ```sh
   codex exec -m gpt-5.6-luna --sandbox read-only --json \
     'Spawn native agent_type auto-skill-alpha with fork_context false. Ask it to
      perform its fixture check using skill-probe-auto. Do not open skill or
      agent files as coordinator. Wait and return the exact child result.' \
     < /dev/null
   ```

4. For the explicit root control, ask the root to invoke `skill-probe-auto` before the same fresh-context delegation. Check whether the tool trace shows a root file read and whether the child shows any independent evidence of applying the body. For the two-child and permission controls, add a beta role with its own marker and `beta.txt`. Launch both before waiting. In each child, use one valid write test such as `touch denied-alpha.txt` or `touch denied-beta.txt`. Check nonzero permission errors and absent files separately. For the missing-skill control, use a trusted project with the named role intact and the specified skill path absent. For the missing-role control, request an undefined role and require an explicit blocked outcome with zero substitute children.

The approved explicit child-loading path requires evidence tying the child's read and execution to the pinned source path, revision, and content hash. In the implementation control, give a competing same-name skill different body-only content and verify that the child used the expected bytes or blocked. Automatic discovery and root-only reads leave the child's effective source unverified. [#24](https://github.com/manueldellapa/Skills/issues/24)

## Claude Code PoC

### Independently checked results

| Probe | Observed evidence |
| --- | --- |
| Named roles and native preload | Foreground `Agent` calls selected `spec-arch` and `spec-adr`. Both had overlapping execution intervals and returned their role lines in a single result. The timing traces showed no skill file reads. `spec-arch` returned `A=SENTINEL-ALPHA-7431`, which is evidence for the enabled project symlink fixture. `spec-adr` returned `A=NONE` for the disabled sentinel. Both returned `B=YES` for matching domain-skill content, but identical personal `architecture` and `adr` directories were visible. The domain-skill source was therefore ambiguous. |
| Skill-only root | Run A invoked `coordinate-specialists` through the ordinary root. Its project deny rule refused `Agent(spec-readonly)` and the other two roles ran. Run B used explicit foreground calls and collected three replies through the ordinary root. These controls show that a discoverable coordinator skill can delegate without the custom root's positive allowlist. In run C the model chose foreground despite the prompt leaving it unspecified, so C does not isolate the default. |
| Read-only and malformed configuration | The `Read, Grep` fixture returned `WRITE=no-tool`. A separate `Write` fixture under `dontAsk` returned `WRITE=denied` and the runtime recorded a `Write` permission denial. The typo fixture used `tool: Read` and reported `Bash`, `Edit`, and `Write` among its available tools. |
| Background return | A custom-root probe without an explicit foreground flag produced a first result indicating the allowed specialist was still running. The specialist's result arrived in a later result event. |
| Custom root plus shared skill | Run D invoked `project-blueprint` through `Skill` from a custom main-thread root with `tools: Agent(spec-arch, spec-adr), Skill, Read`. The two allowlisted children ran in parallel. A third request failed with `not found. Available agents: spec-adr, spec-arch`. The root returned `INCOMPLETE:spec-readonly` followed by `BLUEPRINT-DONE`. This records incomplete work and a completed turn. A production `ready` verdict still requires the separate gate. |

### Reproduce with synthetic inputs

1. In another disposable Git repository, place synthetic `architecture`, `adr`, `sentinel-alpha`, and `sentinel-hidden` skills in `skills/<name>/SKILL.md` and link them from `.claude/skills/<name>` with `../../skills/<name>` targets. Check the visible skill inventory for same-name entries before running the clean preload control. Use distinct body-only values for the two domain skills. Give `sentinel-alpha` the marker `SENTINEL-ALPHA-7431` and `sentinel-hidden` a different body-only marker and `disable-model-invocation: true`.
2. Define `.claude/agents/spec-arch.md` with `skills: [architecture, sentinel-alpha]` and `spec-adr.md` with `skills: [adr, sentinel-hidden]`. Each needs `name` and `description`. Ask each to report its role, its own body-only values, and whether it received the other role's sentinel. Keep the values out of the prompts and exclude skill reads. To reproduce the overlap observation, the original timing fixtures used `tools: Bash` with instructions to run only `date` and `sleep 8`. Use separate permission probes with `tools: Read, Grep` for tool absence and a write-capable fixture under `dontAsk` for runtime denial.
3. Add `.claude/agents/project-blueprint-root.md` with `name: project-blueprint-root`, a `description`, and `tools: Agent(spec-arch, spec-adr), Skill, Read`. Have the root invoke a synthetic shared `project-blueprint` skill that requests both named children in the same turn with `run_in_background: false`, collects their results, and identifies missing required replies. Define an existing `spec-readonly` role outside the allowlist to probe rejection. Run with an authenticated local Claude Code session and retain the stream outside the fixture:

   ```sh
   claude -p --agent project-blueprint-root --model claude-haiku-5-5 \
     --permission-mode dontAsk --allowedTools "Bash(date *)" "Bash(sleep *)" \
     --output-format stream-json --verbose --forward-subagent-text \
     --no-session-persistence \
     'Invoke project-blueprint. Request spec-arch, spec-adr and spec-readonly.
      Return the observed specialist results and identify any missing reply.' \
     < /dev/null
   ```

4. Inspect the actual `Skill` and `Agent` calls, foreground flags, child outputs, tool errors, and result events. Verify role allowlist enforcement with the registered but unlisted role and verify that its child never starts. For the historical comparison, use a normal root with the shared skill and a fixture-local `permissions.deny` containing `Agent(spec-readonly)`. Run a separate background control and compare its first result event with child completion. Use the Bash permissions only for this timing fixture.
5. For the pending shadowing check, add a same-name personal fixture with a different body-only marker in a disposable runtime configuration. Capture the effective selected source and compare its canonical path, pinned revision, and SHA-256 with the expected source. Use the child or root output and runtime evidence to establish which body was actually used. Repeat for the coordinator skill and a specialist preload. A mismatch or unverifiable source must block. This control is a new implementation verification requirement, separate from the historical preload probe.

The PoC root listed `Skill` explicitly and invoked the workflow through that tool. Root-level `skills` preload, the necessity of listing `Skill`, and symlinked root-agent discovery were outside this test.

### Claude Code provenance gate

[Issue #25](https://github.com/manueldellapa/Skills/issues/25) must establish an inspectable evidence method for both the root's skill invocation and specialist preloads. Record source integrity with the pinned canonical path, Git revision, and SHA-256. Check resolution integrity against precedence and all discovery scopes applicable to the tested session, including managed, personal, synced, plugin, and project sources where enabled. A collision-free inventory and hash support source and resolution checks.

Effective usage requires evidence tied to the receiving root or child and its task result. Test whether the supported Claude configuration can expose sufficient evidence for the actual skill invocation or preload. The synthetic sentinel showed usage in its fixture, while the matching domain-skill responses left source selection ambiguous. The reviewed runs established no general provenance method for production skills. If #25 cannot verify effective usage for the approved route, the Claude blueprint route is **no-go** under D-29 and affected runs remain `blocked`. Evaluate any alternative loading mechanism through the architecture approval process before relying on it.

## Pending implementation verification

| Issue | Evidence required |
| --- | --- |
| [#23 — Canonical roles](https://github.com/manueldellapa/Skills/issues/23) | Static contract evidence is defined in the [role catalog](../../roles/README.md) and the nine role files: one-to-one skill mappings, semantic artifact ownership, structured handoffs, native identity and skill-provenance evidence requirements, and independent audit boundaries. Change review must verify those files and references. Runtime proof of native identity and effective skill usage remains with #24–#26. |
| [#24 — Codex adapters](https://github.com/manueldellapa/Skills/issues/24) | Verify native role identity and explicit canonical reads and application for all nine roles. Exercise missing, broken, disabled, and shadowed skills, generic or refused roles, and denied writes. Verify the separate writer's native path and tool boundary or record that writing falls to the user. Characterize native allowlist availability and confirm standalone regression checks. |
| [#25 — Claude Code adapters](https://github.com/manueldellapa/Skills/issues/25) | Verify the custom root and positive allowlist, including rejection of a registered unlisted role. Verify that an ordinary-root blueprint invocation or a wrong or shadowed root starts zero blueprint children. Test direct read-only specialist invocation separately as a supported use. Inspect foreground calls, specialist tool boundaries, absence of child `Agent`, and the [provenance gate](#claude-code-provenance-gate) for the root and all nine specialist preloads, including missing skills and personal or synced collisions. Verify the writer boundary or user handoff and standalone regression. |
| [#26 — Coordinator](https://github.com/manueldellapa/Skills/issues/26) | Verify the supported-root gate before blueprint delegation and the skill-provenance gates before accepting results. Verify greenfield and incremental scheduling, two-worker and one-level bounds, foreground policy, handoffs, approvals, completion, retries, and re-audit against traces and manifest. Exercise the separate writer handoff, missing or stale authorization, unconfined-path fallback, out-of-scope writes, and post-write comparison. Require fail-closed run states. |
| [#27 — Validation and CI](https://github.com/manueldellapa/Skills/issues/27) | Reject unknown and misspelled fields, role and allowlist drift, unsafe tools and permission declarations, broken canonical references, invalid handoffs, and workflow cycles using deterministic fixtures. Preserve current checks. Track runtime evidence of effective controls separately. |
| [#28 — End-to-end release gate](https://github.com/manueldellapa/Skills/issues/28) | Use synthetic projects on both runtime configurations and retain sanitized traces for independent inspection. Verify supported entry points and bypass rejection, skill shadowing and effective bytes, policy compliance, denied writes and authorized writer boundaries, post-write review, incomplete work, failure and restart, non-applicable roles, and independent detection of seeded contradictions. Validate requirements-to-design-to-test traceability. |
| [#29 — Catalog and installation](https://github.com/manueldellapa/Skills/issues/29) | Verify supported entry points and canonical skill resolution in a test checkout and a pinned submodule install. Document unsupported Claude launches, collision troubleshooting, credentials and permission prerequisites, writer limits and user handoff, and supported configurations backed by #28. |
