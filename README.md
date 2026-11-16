# Skills

A personal collection of reusable skills for Claude Code and OpenAI Codex, designed to improve development workflows, automate repetitive tasks, and maintain consistency across projects.

## Layout

Each skill lives once in `skills/<name>/SKILL.md`, following the
[Agent Skills specification](https://agentskills.io/specification).
Codex and Claude Code load it through relative symlinks:

```text
.agents/skills/<name> -> ../../skills/<name>
.claude/skills/<name> -> ../../skills/<name>
```

## Validation

`scripts/validate_skills.py` checks the frontmatter (`name`, `description` and
the optional specification fields), duplicate names, local Markdown links and
the agent symlinks. It runs in GitHub Actions on pull requests and pushes to
`main`. To run it locally (Python 3.12):

```bash
python -m pip install --group dev
python -m pytest
python scripts/validate_skills.py
```
