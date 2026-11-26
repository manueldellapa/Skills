# Skills

Reusable software development workflows for OpenAI Codex and Claude Code.

## Skill catalog

| Skill | Use it to | Operating boundaries |
| --- | --- | --- |
| [adr](skills/adr/SKILL.md) | Draft and review Architecture Decision Records, compare alternatives, and preserve decision history. | Defaults to read-only. Stakeholders retain decision and approval authority. |
| [api-contracts](skills/api-contracts/SKILL.md) | Design or review API contracts, including compatibility, migrations, and contract tests. | Defaults to read-only. Contract writes and checks with side effects require authorization. |
| [architecture](skills/architecture/SKILL.md) | Assess software structure, component boundaries, trade-offs, and migration options. | Provides guidance within existing requirements. Implementation belongs to a separate task. |
| [data-model](skills/data-model/SKILL.md) | Design or review schemas, relationships, integrity constraints, and safe schema evolution. | Covers design and review. Schema changes and migration execution are outside its scope. |
| [documentation-audit](skills/documentation-audit/SKILL.md) | Find documentation gaps, stale claims, and duplication using repository evidence. | Defaults to read-only. Edits require an explicit request. |
| [operations-runbook](skills/operations-runbook/SKILL.md) | Draft or review deployment, monitoring, troubleshooting, rollback, and recovery procedures. | Uses passive inspection. Live checks and operational changes require a separately authorized execution task. |
| [prd](skills/prd/SKILL.md) | Define implementation-ready product requirements, milestones, dependencies, and acceptance criteria. | Covers requirements analysis and documentation. Feature implementation is outside its scope. |
| [security-design](skills/security-design/SKILL.md) | Model threats, analyze trust boundaries, and design or review security controls. | Defaults to passive review and design. Scanning, penetration testing, and exploit development are outside its scope. |
| [test-strategy](skills/test-strategy/SKILL.md) | Map risks and acceptance criteria to verification coverage and pass/fail evidence. | Defaults to read-only planning and review. Running checks and changing tests require separate consideration of scope and side effects. |

## Canonical specialist roles

The [runtime-neutral role contracts](roles/README.md) map the nine canonical
skills to independently reusable, read-only specialists. Skills define how
domain work is performed; role contracts define inputs, outputs, semantic
artifact ownership, evidence, escalation, and handoffs.

| Role | Canonical skill |
| --- | --- |
| [Product Analyst](roles/product-analyst.md) | `prd` |
| [Software Architect](roles/software-architect.md) | `architecture` |
| [Decision Analyst](roles/decision-analyst.md) | `adr` |
| [Data Architect](roles/data-architect.md) | `data-model` |
| [API Architect](roles/api-architect.md) | `api-contracts` |
| [Security Architect](roles/security-architect.md) | `security-design` |
| [QA Architect](roles/qa-architect.md) | `test-strategy` |
| [DevOps Engineer](roles/devops-engineer.md) | `operations-runbook` |
| [Documentation Auditor](roles/documentation-auditor.md) | `documentation-audit` |

## Repository layout

Each skill has one canonical directory, `skills/<name>/`, containing `SKILL.md`
and any supporting files. Git tracks one relative directory symlink per skill for
each client.

```text
.agents/skills/<name> -> ../../skills/<name>  (Codex)
.claude/skills/<name> -> ../../skills/<name>  (Claude Code)
roles/<role-id>.md                              (runtime-neutral role contract)
```

Role contracts are not client adapters and do not contain runtime-specific
models, tools, permissions, or orchestration policy.

## Installation

The examples use a POSIX shell, Git, and a filesystem with symlink support, as on
macOS and Linux. Review the skill instructions before installing them.

### Use this repository directly

Use an existing checkout or run the clone setup under
[Install for your user account](#install-for-your-user-account), stopping before
the linking step. Start the client in the checkout. The tracked symlinks already
expose the skills in this project.

```sh
cd "$HOME/src/Skills"
```

### Install for another project

Use a Git submodule to pin the source revision and share the selected skills with
teammates. Run this from the root of the target Git project. The setup reuses the
submodule registered by this example and stops if the path is otherwise occupied.
For a fresh clone of a project that already tracks this submodule, initialize it
with `git submodule update --init -- vendor/Skills`.

```sh
(
  set -e
  skills_url=https://github.com/manueldellapa/Skills.git
  submodule=vendor/Skills
  if [ -L vendor ] || [ -L "$submodule" ]; then
    printf 'Refusing symlink at or above %s\n' "$submodule" >&2
    exit 1
  fi

  if [ "$(git config -f .gitmodules --get submodule.vendor/Skills.path)" = "$submodule" ] &&
     [ "$(git config -f .gitmodules --get submodule.vendor/Skills.url)" = "$skills_url" ] &&
     [ "$(git ls-files --stage -- "$submodule" | cut -d ' ' -f 1)" = 160000 ]; then
    printf 'Using registered submodule %s\n' "$submodule"
  elif [ -e "$submodule" ]; then
    printf 'Destination already exists: %s\n' "$submodule" >&2
    exit 1
  else
    git submodule add "$skills_url" "$submodule"
  fi
)
```

After setup succeeds, set these variables and run [Link the selected skills](#link-the-selected-skills)
from the same project root.

```sh
source_dir=vendor/Skills/skills
link_base=../../vendor/Skills/skills
agent_root=.
```

For team use, review and commit the project's `.gitmodules`, the pinned
submodule entry, and the relative skill links together.

### Install for your user account

User-level links make skills available across local projects for the same user.
Keep the source checkout at a stable path. The example clones it on first use
and accepts an existing checkout with the expected origin. Adjust `skills_repo`
if you already have a clone elsewhere.

```sh
(
  set -e
  skills_url=https://github.com/manueldellapa/Skills.git
  skills_repo="$HOME/src/Skills"
  if [ -e "$skills_repo" ] || [ -L "$skills_repo" ]; then
    if [ ! -e "$skills_repo/.git" ] ||
       [ "$(git -C "$skills_repo" config --local --get remote.origin.url)" != "$skills_url" ]; then
      printf 'Destination is not the expected checkout: %s\n' "$skills_repo" >&2
      exit 1
    fi
  else
    mkdir -p "$HOME/src"
    git clone "$skills_url" "$skills_repo"
  fi
)
```

After setup succeeds, set these variables and run [Link the selected skills](#link-the-selected-skills)
in the same shell. Use the same checkout path in both blocks.

```sh
source_dir="$HOME/src/Skills/skills"
link_base="$source_dir"
agent_root="$HOME"
```

The absolute links depend on this checkout. Update it with `git pull --ff-only`
after checking its branch and working tree. Keep these links out of project commits.

### Link the selected skills

Run this after setting the variables for your chosen scope. The example installs
`architecture` and `prd` for both clients. Edit the `set --` line to select other
skills, or use the commented line to install the full catalog. Use only the
relevant entry in the client loop if you use one client.

```sh
(
  set -eu
  set -- "$source_dir/architecture" "$source_dir/prd"
  # set -- "$source_dir"/*   # Install the full catalog.

  for skill_dir do
    if [ ! -f "$skill_dir/SKILL.md" ]; then
      printf 'Missing skill: %s/SKILL.md\n' "$skill_dir" >&2
      exit 1
    fi
  done

  for client_dir in "$agent_root/.agents" "$agent_root/.claude"; do
    parent="$client_dir/skills"
    if [ -L "$client_dir" ] || [ -L "$parent" ]; then
      printf 'Skipping symlinked client directory: %s\n' "$parent" >&2
      continue
    fi
    mkdir -p "$parent"
    for skill_dir do
      name=${skill_dir##*/}
      destination="$parent/$name"
      if [ -e "$destination" ] || [ -L "$destination" ]; then
        printf 'Keeping existing destination: %s\n' "$destination"
        continue
      fi
      ln -s "$link_base/$name" "$destination"
    done
  done
)
```

Reruns preserve existing files, directories, and symlinks, including dangling
links. Inspect any skipped path before deciding whether to change it.

## Discovery and verification

- **Codex** scans `.agents/skills/` from the working directory up to the Git
  root and reads user skills from `~/.agents/skills/`. Same-name entries can
  both appear, so check which path you select instead of assuming project
  precedence. In the CLI, use `/skills` or request `$architecture` explicitly.
  [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills)
- **Claude Code** uses `.claude/skills/` for project skills and
  `~/.claude/skills/` for personal skills with the default configuration.
  For distinct skills with the same command name at these scopes, enterprise
  takes precedence over personal, then project. Claude Code loads a shared
  symlink target once. Use the slash menu or invoke `/architecture` explicitly.
  [Claude Code skills documentation](https://code.claude.com/docs/en/skills)

Project links apply within that project's discovery scope. User links live on
the machine running your client. On a remote host, install the skills where the
client runs.

Codex Cloud gives each task its own workspace.
[Codex cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)

Do not assume that locally installed skills are available in a cloud workspace.

For this repository's submodule-based installation, check that the remote
checkout includes the project symlinks. Initialize the pinned submodule if
needed, then verify that the symlinks resolve to the expected `SKILL.md` files
in the remote workspace.

Claude Code cloud sessions can discover repository skills where supported and
load skills enabled for your claude.ai account. Your local
`~/.claude/skills/` stays on your machine. [Claude Code cloud skill discovery](https://code.claude.com/docs/en/skills#skills-in-cowork-and-cloud-sessions)

After linking, check that each selected entry resolves to its expected
`SKILL.md` under the source checkout. For example, in the same shell as the
installation, check the two paths for `architecture`.

```sh
test -f "$agent_root/.agents/skills/architecture/SKILL.md" &&
test -f "$agent_root/.claude/skills/architecture/SKILL.md"
```

Open a client session in the intended project and confirm the skill is listed
and can be invoked. Filesystem checks establish that the link resolves. Client
checks establish discovery and invocation.

## Validation and contributions

The [validation workflow](.github/workflows/validate-skills.yml) runs pytest and
the [skill validator](scripts/validate_skills.py) on pull requests targeting
`main` and pushes to `main`. For local commands and review steps, see
[Contributing](CONTRIBUTING.md). The required skill format is defined by the
[Agent Skills specification](https://agentskills.io/specification).
