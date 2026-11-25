# Contributing

Use the [skill catalog](README.md#skill-catalog) to find related workflows
before adding a skill. Give each workflow a clear trigger, a defined output, and
explicit operational boundaries.

## Naming and frontmatter

Start each `SKILL.md` with a YAML mapping between `---` delimiters, followed
by Markdown instructions. Use unique YAML keys and follow the
[Agent Skills specification](https://agentskills.io/specification) and the
[repository validator](scripts/validate_skills.py).

- `name` is a unique string matching the directory name. Use 1–64 lowercase
  ASCII letters, digits, and hyphens, with no leading, trailing, or consecutive
  hyphens. The validator reserves `synced` and `anthropic-skills` for Claude Code.
- `description` is a nonblank string of at most 1,024 characters. Explain what
  the skill does and when to use it.
- If present, `license` is a nonblank string naming the license or referring to
  a bundled license file. `compatibility` is a nonblank string of at most 500
  characters. `metadata` maps strings to strings. Quote values such as versions
  to preserve their string type. `allowed-tools` is an experimental,
  space-separated tool list written as a nonblank string.
- The validator permits client-specific fields. Check their behavior in the
  intended client when you use them.

## Add a skill

1. Define the trigger, inputs, expected output, and allowed side effects.
2. Create the canonical file and the two relative links using the example
   below. Pick an unused name and use it consistently in the directory and
   frontmatter. Run the commands from the repository root.
3. Replace the sample body with the workflow. Keep supporting files under the
   same skill directory and link to them using paths relative to `SKILL.md`.
4. Add an alphabetical entry to the [catalog](README.md#skill-catalog) and run
   the checks below.

```sh
(
  set -e
  skill_name=release-note-review
  for parent in .agents/skills .claude/skills; do
    destination="$parent/$skill_name"
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      printf 'Destination already exists: %s\n' "$destination" >&2
      exit 1
    fi
  done

  mkdir "skills/$skill_name"
  cat > "skills/$skill_name/SKILL.md" <<'SKILL'
---
name: release-note-review
description: Review draft release notes against the changes included in the release.
---

# Release Note Review

Compare the draft with the changes in the release. Report omissions and
unsupported claims with references to the relevant changes.
SKILL

  ln -s "../../skills/$skill_name" ".agents/skills/$skill_name"
  ln -s "../../skills/$skill_name" ".claude/skills/$skill_name"
)
```

The two links expose the canonical instructions. See the
[repository layout](README.md#repository-layout) for the expected paths.

## Validate and review

From the repository root, with Python 3.12 in an active virtual environment,
install the development dependencies and run the same checks as
[CI](.github/workflows/validate-skills.yml).

```sh
python -m pip install --upgrade pip
python -m pip install --group dev
python -m pytest
python scripts/validate_skills.py
git status --short
git diff --check HEAD
```

Pytest exercises validator behavior. The validator checks canonical structure,
frontmatter, unique and reserved names, local references in skill bodies, and
agent symlinks. Review new files separately because `git diff` excludes
untracked files.

- Follow links in the catalog and guide and check any linked resources.
- Review the instructions against a representative request and one outside the
  intended scope. Check trigger wording, output expectations, permissions,
  and command side effects.
- In each intended client, check discovery and explicit invocation in a
  test checkout. Try the representative prompts to assess implicit selection
  and scope. Record the client and version, observed behavior, and any checks
  you could not run.

## Open a pull request

Explain the purpose, affected skills, and any changes to triggers, permissions,
or side effects. Include test results and manual verification, with any
remaining limitations. Include the canonical skill, both relative links, and
the catalog entry when adding a skill. Keep the diff focused on the change.
