import os
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.validate_skills import (
    AGENT_DIRS,
    ROOT_PATH,
    main,
    validate_skill_metadata,
    validate_skills,
    validate_symlinks,
)

VALID_FRONTMATTER = "name: example\ndescription: Example skill for tests."


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def write_skill(
    skills_path: Path,
    dirname: str,
    frontmatter: str | None = None,
    body: str = "# Instructions\n",
) -> Path:
    """Create ``skills_path/dirname/SKILL.md`` and return the skill directory."""
    if frontmatter is None:
        frontmatter = f"name: {dirname}\ndescription: Example skill for tests."

    skill_dir = skills_path / dirname
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8"
    )
    return skill_dir


def link_skill(root: Path, agent_dir: Path, name: str) -> Path:
    """Create the canonical relative symlink ``agent_dir/name``."""
    agent_path = root / agent_dir
    agent_path.mkdir(parents=True, exist_ok=True)
    link = agent_path / name
    link.symlink_to(
        os.path.relpath(root / "skills" / name, agent_path),
        target_is_directory=True,
    )
    return link


def make_repo(root: Path, *names: str) -> Path:
    """Create a valid repository layout with the given skills."""
    for name in names:
        write_skill(root / "skills", name)
        for agent_dir in AGENT_DIRS:
            link_skill(root, agent_dir, name)
    return root


def write_skill_md(tmp_path: Path, content: str | bytes) -> Path:
    skill_dir = tmp_path / "example"
    skill_dir.mkdir(exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    if isinstance(content, bytes):
        skill_file.write_bytes(content)
    else:
        skill_file.write_text(content, encoding="utf-8", newline="")
    return skill_dir


def metadata_errors(tmp_path: Path, frontmatter: str, body: str = "# Instructions\n"):
    return validate_skill_metadata(
        write_skill_md(tmp_path, f"---\n{frontmatter}\n---\n\n{body}")
    )


def assert_error(errors: list[str], *fragments: str) -> None:
    assert any(all(fragment in error for fragment in fragments) for error in errors), errors


# --------------------------------------------------------------------------
# main() and command line
# --------------------------------------------------------------------------


def test_current_repository_is_valid(capsys):
    assert main(["--root", str(ROOT_PATH)]) == 0
    assert "OK:" in capsys.readouterr().out


def test_main_valid_layout(tmp_path, capsys):
    make_repo(tmp_path, "alpha", "beta")

    assert main(["--root", str(tmp_path)]) == 0
    assert "OK: 2 skill(s)" in capsys.readouterr().out


def test_main_reports_file_and_reason(tmp_path, capsys):
    make_repo(tmp_path, "alpha")
    write_skill(tmp_path / "skills", "alpha", "name: alpha\ndescription: ''")

    assert main(["--root", str(tmp_path)]) == 1

    stderr = capsys.readouterr().err
    assert "alpha/SKILL.md:3: Invalid skill description: must not be empty" in stderr
    assert "FAILED: 1 error(s) found." in stderr


def test_main_missing_skills_directory(tmp_path, capsys):
    assert main(["--root", str(tmp_path)]) == 1

    stderr = capsys.readouterr().err
    assert "Missing skills directory" in stderr
    assert "Missing agent directory" in stderr


def test_main_detects_broken_agent_symlink(tmp_path, capsys):
    make_repo(tmp_path, "alpha")
    link = tmp_path / ".claude" / "skills" / "alpha"
    link.unlink()
    link.symlink_to("../../skills/missing", target_is_directory=True)

    assert main(["--root", str(tmp_path)]) == 1
    assert "Broken symlink" in capsys.readouterr().err


def test_main_rejects_unknown_argument():
    with pytest.raises(SystemExit) as exc_info:
        main(["--unknown"])

    assert exc_info.value.code == 2


@pytest.mark.parametrize(("valid", "expected_code"), [(True, 0), (False, 1)])
def test_cli_exit_code(tmp_path, valid, expected_code):
    make_repo(tmp_path, "alpha")
    if not valid:
        (tmp_path / "skills" / "alpha" / "SKILL.md").unlink()

    result = subprocess.run(
        [sys.executable, str(ROOT_PATH / "scripts" / "validate_skills.py"),
         "--root", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == expected_code, result.stderr
    if not valid:
        assert "Missing SKILL.md" in result.stderr


# --------------------------------------------------------------------------
# skills/ directory
# --------------------------------------------------------------------------


def test_valid_skill(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")

    skills, errors = validate_skills(tmp_path / "skills")

    assert errors == []
    assert skills == {"prd": skill_dir}


def test_missing_skill_file(tmp_path):
    (tmp_path / "skills" / "invalid-skill").mkdir(parents=True)

    skills, errors = validate_skills(tmp_path / "skills")

    assert "invalid-skill" in skills
    assert_error(errors, "invalid-skill/SKILL.md", "Missing SKILL.md")


def test_missing_skills_directory(tmp_path):
    skills, errors = validate_skills(tmp_path / "skills")

    assert skills == {}
    assert_error(errors, "Missing skills directory")


def test_empty_skills_directory(tmp_path):
    (tmp_path / "skills").mkdir()

    _, errors = validate_skills(tmp_path / "skills")

    assert_error(errors, "No skills found")


def test_hidden_entries_are_ignored(tmp_path):
    write_skill(tmp_path / "skills", "alpha")
    (tmp_path / "skills" / ".DS_Store").write_text("", encoding="utf-8")
    (tmp_path / "skills" / ".draft").mkdir()

    skills, errors = validate_skills(tmp_path / "skills")

    assert errors == []
    assert list(skills) == ["alpha"]


def test_unexpected_file_in_skills_directory(tmp_path):
    write_skill(tmp_path / "skills", "alpha")
    (tmp_path / "skills" / "README.md").write_text("notes", encoding="utf-8")

    _, errors = validate_skills(tmp_path / "skills")

    assert_error(errors, "README.md", "Unexpected file in skills directory")


def test_symlinked_skill_directory_is_rejected(tmp_path):
    write_skill(tmp_path / "skills", "alpha")
    (tmp_path / "skills" / "beta").symlink_to("alpha", target_is_directory=True)

    skills, errors = validate_skills(tmp_path / "skills")

    assert "beta" not in skills
    assert_error(errors, "beta", "must be a real directory, not a symlink")


def test_duplicate_skill_names(tmp_path):
    write_skill(tmp_path / "skills", "alpha")
    write_skill(
        tmp_path / "skills",
        "beta",
        "name: alpha\ndescription: Same name as another skill.",
    )

    _, errors = validate_skills(tmp_path / "skills")

    assert_error(errors, "beta/SKILL.md:2", "Duplicate skill name 'alpha'", "alpha/SKILL.md")
    assert_error(errors, "Skill name 'alpha' does not match directory 'beta'")


def test_skills_without_string_names_are_not_duplicates(tmp_path):
    write_skill(tmp_path / "skills", "alpha", "description: No name.")
    write_skill(tmp_path / "skills", "beta", "description: No name either.")

    _, errors = validate_skills(tmp_path / "skills")

    assert len(errors) == 2
    assert all("missing required field 'name'" in error for error in errors)


# --------------------------------------------------------------------------
# Frontmatter parsing
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("content", "expected_error"),
    [
        ("# Instructions\n", "1: Missing YAML frontmatter"),
        ("", "1: Missing YAML frontmatter"),
        ("  ---\nname: example\n---\n# Body\n", "1: Missing YAML frontmatter"),
        ("---\nname: example\n", "1: Unclosed YAML frontmatter"),
        (
            "---\nname: example\ndescription: x\n  ---\n# Body\n",
            "1: Unclosed YAML frontmatter",
        ),
        ("---\n---\n# Body\n", "1: Empty YAML frontmatter"),
        ("---\n- name\n- description\n---\n# Body\n", "2: Frontmatter must be a YAML mapping, got list"),
        (
            "---\nname: example\ndescription: [invalid\n---\n# Body\n",
            "Invalid YAML in frontmatter",
        ),
        (
            "---\nname: example\ndescription: One\ndescription: Two\n---\n# Body\n",
            "4: Duplicate YAML key 'description' in frontmatter",
        ),
        (
            "---\nname: example\ndescription: Example\n---\n",
            "Missing skill instructions",
        ),
        (
            "---\nname: example\ndescription: Example\n---\n   \n\n",
            "Missing skill instructions",
        ),
    ],
)
def test_invalid_skill_content(tmp_path, content, expected_error):
    errors = validate_skill_metadata(write_skill_md(tmp_path, content))

    assert_error(errors, expected_error)


def test_utf8_bom_is_reported(tmp_path):
    content = f"---\n{VALID_FRONTMATTER}\n---\n# Body\n".encode()

    errors = validate_skill_metadata(write_skill_md(tmp_path, b"\xef\xbb\xbf" + content))

    assert_error(errors, "SKILL.md:1", "UTF-8 BOM")


def test_invalid_utf8_is_reported(tmp_path):
    errors = validate_skill_metadata(write_skill_md(tmp_path, b"---\nname: \xff\n---\n"))

    assert_error(errors, "not valid UTF-8")


@pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="needs POSIX permissions and a non-root user",
)
def test_unreadable_skill_file(tmp_path):
    skill_dir = write_skill_md(tmp_path, f"---\n{VALID_FRONTMATTER}\n---\n# Body\n")
    skill_file = skill_dir / "SKILL.md"
    skill_file.chmod(0)

    try:
        errors = validate_skill_metadata(skill_dir)
    finally:
        skill_file.chmod(0o644)

    assert_error(errors, "Cannot read SKILL.md")


def test_invalid_yaml_reports_file_line(tmp_path):
    errors = metadata_errors(
        tmp_path, "name: example\n  bad: indent: here\ndescription: Example"
    )

    assert_error(errors, "SKILL.md:3", "Invalid YAML in frontmatter")


def test_indented_delimiter_inside_block_scalar_is_content(tmp_path):
    errors = metadata_errors(
        tmp_path,
        "name: example\ndescription: |\n  First line\n  ---\n  Still description",
    )

    assert errors == []


def test_crlf_line_endings_are_accepted(tmp_path):
    content = f"---\r\n{VALID_FRONTMATTER}\r\n---\r\n# Body\r\n".replace(
        "\ndescription", "\r\ndescription"
    )

    assert validate_skill_metadata(write_skill_md(tmp_path, content)) == []


def test_delimiter_trailing_whitespace_is_accepted(tmp_path):
    content = f"---  \n{VALID_FRONTMATTER}\n--- \n# Body\n"

    assert validate_skill_metadata(write_skill_md(tmp_path, content)) == []


def test_unhashable_yaml_key_is_reported(tmp_path):
    errors = metadata_errors(tmp_path, f"{VALID_FRONTMATTER}\n? [a, b]\n: value")

    assert_error(errors, "Invalid YAML in frontmatter", "unhashable key")


def test_yaml_merge_keys_are_not_duplicates(tmp_path):
    errors = metadata_errors(
        tmp_path,
        "name: example\ndescription: Example\n"
        "base: &base {a: '1'}\nmetadata:\n  <<: *base\n  a: '2'",
    )

    assert errors == []


# --------------------------------------------------------------------------
# Frontmatter fields
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("frontmatter", "expected_error"),
    [
        ("description: Example", "missing required field 'name'"),
        ("name: 123\ndescription: Example", "expected a string, got integer"),
        ("name:\ndescription: Example", "expected a string, got null"),
        ("name: ''\ndescription: Example", "must be 1-64 characters (got 0)"),
        (f"name: {'a' * 65}\ndescription: Example", "must be 1-64 characters (got 65)"),
        ("name: Example\ndescription: Example", "invalid character(s) 'E'"),
        ("name: my_skill\ndescription: Example", "invalid character(s) '_'"),
        ("name: -example\ndescription: Example", "must not start or end with a hyphen"),
        ("name: example-\ndescription: Example", "must not start or end with a hyphen"),
        ("name: invalid--name\ndescription: Example", "must not contain consecutive hyphens"),
        ("name: other\ndescription: Example", "does not match directory 'example'"),
    ],
)
def test_invalid_name(tmp_path, frontmatter, expected_error):
    errors = metadata_errors(tmp_path, frontmatter)

    assert_error(errors, "SKILL.md:", expected_error)


def test_name_error_reports_line(tmp_path):
    errors = metadata_errors(tmp_path, "description: Example\nname: Bad")

    assert_error(errors, "SKILL.md:3", "Invalid skill name 'Bad'")


def test_maximum_name_length_is_valid(tmp_path):
    name = "a" * 64
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Example\n---\n# Body\n", encoding="utf-8"
    )

    assert validate_skill_metadata(skill_dir) == []


@pytest.mark.parametrize(
    ("description", "expected_error"),
    [
        (None, "missing required field 'description'"),
        ("42", "expected a string, got integer"),
        ("''", "must not be empty"),
        ("'   '", "must not be empty"),
        ("x" * 1025, "must be at most 1024 characters (got 1025)"),
    ],
)
def test_invalid_description(tmp_path, description, expected_error):
    frontmatter = "name: example"
    if description is not None:
        frontmatter += f"\ndescription: {description}"

    errors = metadata_errors(tmp_path, frontmatter)

    assert_error(errors, "Invalid skill description", expected_error)


def test_maximum_description_length_is_valid(tmp_path):
    assert metadata_errors(tmp_path, f"name: example\ndescription: {'x' * 1024}") == []


def test_valid_optional_fields(tmp_path):
    errors = metadata_errors(
        tmp_path,
        VALID_FRONTMATTER + "\n"
        "license: Apache-2.0\n"
        f"compatibility: {'c' * 500}\n"
        "metadata:\n  author: example\n  version: '1.0'\n"
        "allowed-tools: Bash(git:*) Read\n"
        "argument-hint: '[topic]'",  # Agent-specific extension fields are allowed.
    )

    assert errors == []


@pytest.mark.parametrize(
    ("extra", "expected_error"),
    [
        ("license: ''", "Invalid 'license': must not be empty"),
        ("license: [MIT]", "Invalid 'license': expected a string, got list"),
        ("compatibility: ''", "Invalid 'compatibility': must not be empty"),
        ("compatibility: 3", "Invalid 'compatibility': expected a string, got integer"),
        (f"compatibility: {'c' * 501}", "must be at most 500 characters (got 501)"),
        ("metadata: notamap", "Invalid 'metadata': expected a mapping"),
        ("metadata:\n  version: 1.0", "Invalid 'metadata.version': expected a string, got number"),
        ("metadata:\n  1: one", "Invalid 'metadata' key 1"),
        ("allowed-tools: [Read, Bash]", "Invalid 'allowed-tools'"),
        ("allowed-tools: ''", "Invalid 'allowed-tools'"),
    ],
)
def test_invalid_optional_fields(tmp_path, extra, expected_error):
    errors = metadata_errors(tmp_path, f"{VALID_FRONTMATTER}\n{extra}")

    assert_error(errors, expected_error)


# --------------------------------------------------------------------------
# Local references
# --------------------------------------------------------------------------


def test_valid_local_references(tmp_path):
    skill_dir = write_skill_md(tmp_path, "")
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "guide.md").write_text("guide", encoding="utf-8")
    (skill_dir / "references" / "my file.md").write_text("spaces", encoding="utf-8")
    (skill_dir / "assets").mkdir()
    (skill_dir / "assets" / "logo.png").write_bytes(b"")

    body = (
        "See [the guide](references/guide.md) and [section](references/guide.md#usage).\n"
        "Also [titled](references/guide.md \"Guide\") and [spaces](references/my%20file.md).\n"
        "Angle [link](<references/my file.md>) and ![logo](assets/logo.png).\n"
        "Self [link](./SKILL.md) and [ref][guide].\n"
        "\n"
        "[guide]: references/guide.md\n"
        "External [site](https://example.com/x.md), [mail](mailto:a@b.c), "
        "[anchor](#top), [query](?tab=1) and [proto](//cdn.example.com/a.js).\n"
    )
    (skill_dir / "SKILL.md").write_text(
        f"---\n{VALID_FRONTMATTER}\n---\n\n{body}", encoding="utf-8"
    )

    assert validate_skill_metadata(skill_dir) == []


def test_broken_local_reference(tmp_path):
    errors = metadata_errors(
        tmp_path, VALID_FRONTMATTER, "# Body\n\nSee [missing](references/missing.md).\n"
    )

    assert_error(errors, "SKILL.md:8", "Broken local reference 'references/missing.md'")


def test_broken_reference_definition(tmp_path):
    errors = metadata_errors(
        tmp_path, VALID_FRONTMATTER, "# Body\n\n[guide]: references/missing.md\n"
    )

    assert_error(errors, "Broken local reference 'references/missing.md'")


@pytest.mark.parametrize(
    ("target", "expected_error"),
    [
        ("../other/SKILL.md", "points outside the skill directory"),
        ("references/../../outside.md", "points outside the skill directory"),
        ("/etc/hosts", "absolute paths are not portable"),
    ],
)
def test_reference_outside_skill(tmp_path, target, expected_error):
    (tmp_path / "other").mkdir()
    (tmp_path / "other" / "SKILL.md").write_text("x", encoding="utf-8")
    (tmp_path / "outside.md").write_text("x", encoding="utf-8")

    errors = metadata_errors(tmp_path, VALID_FRONTMATTER, f"# Body\n\n[x]({target})\n")

    assert_error(errors, "Invalid local reference", expected_error)


def test_reference_escaping_through_symlink(tmp_path):
    (tmp_path / "secret.md").write_text("x", encoding="utf-8")
    skill_dir = write_skill_md(tmp_path, "")
    (skill_dir / "link.md").symlink_to("../secret.md")
    (skill_dir / "SKILL.md").write_text(
        f"---\n{VALID_FRONTMATTER}\n---\n\n[x](link.md)\n", encoding="utf-8"
    )

    errors = validate_skill_metadata(skill_dir)

    assert_error(errors, "points outside the skill directory")


def test_links_in_code_are_ignored(tmp_path):
    body = (
        "# Body\n\n"
        "Inline `[x](missing-inline.md)` code.\n\n"
        "```markdown\n"
        "[x](missing-fenced.md)\n"
        "```\n\n"
        "~~~~\n"
        "```\n"
        "[x](missing-nested.md)\n"
        "~~~~\n"
    )

    assert metadata_errors(tmp_path, VALID_FRONTMATTER, body) == []


def test_link_after_closed_fence_is_checked(tmp_path):
    body = "# Body\n\n```\ncode\n```\n\n[x](missing.md)\n"

    errors = metadata_errors(tmp_path, VALID_FRONTMATTER, body)

    assert_error(errors, "Broken local reference 'missing.md'")


# --------------------------------------------------------------------------
# Agent symlinks
# --------------------------------------------------------------------------


def test_valid_symlink(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    link_skill(tmp_path, Path(".agents/skills"), "prd")

    errors = validate_symlinks(tmp_path / ".agents" / "skills", {"prd": skill_dir})

    assert errors == []


def test_missing_agent_directory(tmp_path):
    errors = validate_symlinks(tmp_path / ".agents" / "skills", {})

    assert_error(errors, "Missing agent directory")


def test_missing_symlink(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    (tmp_path / ".agents" / "skills").mkdir(parents=True)

    errors = validate_symlinks(tmp_path / ".agents" / "skills", {"prd": skill_dir})

    assert_error(errors, "Missing symlink", "'../../skills/prd'")


def test_directory_copy_instead_of_symlink(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    write_skill(tmp_path / ".agents" / "skills", "prd")

    errors = validate_symlinks(tmp_path / ".agents" / "skills", {"prd": skill_dir})

    assert_error(errors, "found a directory instead of a symlink")


def test_regular_file_instead_of_symlink(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    agent_path = tmp_path / ".agents" / "skills"
    agent_path.mkdir(parents=True)
    (agent_path / "prd").write_text("../../skills/prd", encoding="utf-8")

    errors = validate_symlinks(agent_path, {"prd": skill_dir})

    assert_error(errors, "found a regular file", "core.symlinks")


def test_broken_symlink(tmp_path):
    agent_path = tmp_path / ".agents" / "skills"
    agent_path.mkdir(parents=True)
    (agent_path / "prd").symlink_to("../../skills/prd", target_is_directory=True)

    errors = validate_symlinks(agent_path, {"prd": tmp_path / "skills" / "prd"})

    assert_error(errors, "Broken symlink")


def test_absolute_symlink_is_rejected(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    agent_path = tmp_path / ".agents" / "skills"
    agent_path.mkdir(parents=True)
    (agent_path / "prd").symlink_to(skill_dir.absolute(), target_is_directory=True)

    errors = validate_symlinks(agent_path, {"prd": skill_dir})

    assert_error(errors, "Absolute symlink target", "use the relative target '../../skills/prd'")


def test_wrong_symlink_target(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    write_skill(tmp_path / "skills", "other")
    agent_path = tmp_path / ".agents" / "skills"
    agent_path.mkdir(parents=True)
    (agent_path / "prd").symlink_to("../../skills/other", target_is_directory=True)

    errors = validate_symlinks(agent_path, {"prd": skill_dir})

    assert_error(errors, "Invalid symlink target", "expected '../../skills/prd'")


@pytest.mark.parametrize(
    "target",
    [
        "../../.agents/skills/prd",  # Chained through another agent directory.
        "../../../{root}/skills/prd",  # Depends on the clone directory name.
    ],
)
def test_non_canonical_symlink_is_rejected(tmp_path, target):
    make_repo(tmp_path, "prd")
    link = tmp_path / ".claude" / "skills" / "prd"
    link.unlink()
    link.symlink_to(target.format(root=tmp_path.name), target_is_directory=True)

    errors = validate_symlinks(
        tmp_path / ".claude" / "skills", {"prd": tmp_path / "skills" / "prd"}
    )

    assert_error(errors, "Non-canonical symlink target")


def test_unexpected_agent_entry(tmp_path):
    skill_dir = write_skill(tmp_path / "skills", "prd")
    link_skill(tmp_path, Path(".agents/skills"), "prd")
    agent_path = tmp_path / ".agents" / "skills"
    (agent_path / "stale").symlink_to("../../skills/stale", target_is_directory=True)
    (agent_path / ".DS_Store").write_text("", encoding="utf-8")

    errors = validate_symlinks(agent_path, {"prd": skill_dir})

    assert len(errors) == 1
    assert_error(errors, "stale", "Unexpected agent entry")


# --------------------------------------------------------------------------
# Regression: CommonMark link extraction
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("body", "expected_line"),
    [
        ("See [the\nguide](missing.md).\n", 6),  # Link text over two lines.
        ("See [guide](missing.md\n  \"Title\").\n", 6),  # Title on next line.
        ("First line\nsecond [x](missing.md)\n", 7),  # Link on a later line.
        ("- item\n\n  > quoted [x](missing.md)\n", 8),  # List and blockquote.
        ("Text <span\nclass=\"x\"> [x](missing.md)\n", 7),  # Inline HTML.
    ],
)
def test_links_spanning_lines_are_checked(tmp_path, body, expected_line):
    errors = metadata_errors(tmp_path, VALID_FRONTMATTER, body)

    assert_error(errors, f"SKILL.md:{expected_line}:", "Broken local reference 'missing.md'")


def test_multiline_reference_definition_is_checked(tmp_path):
    body = "Use [the guide][g].\n\n[g]:\n  missing.md\n  'Title'\n"

    errors = metadata_errors(tmp_path, VALID_FRONTMATTER, body)

    assert_error(errors, "SKILL.md:8:", "Broken local reference 'missing.md'")


def test_reference_used_several_times_is_reported_once(tmp_path):
    body = "[a][g], [b][g] and [g].\n\n[g]: missing.md\n"

    errors = metadata_errors(tmp_path, VALID_FRONTMATTER, body)

    assert len(errors) == 1
    assert_error(errors, "SKILL.md:8:", "Broken local reference 'missing.md'")


def test_unused_reference_definition_is_checked(tmp_path):
    errors = metadata_errors(tmp_path, VALID_FRONTMATTER, "# Body\n\n[unused]: missing.md\n")

    assert_error(errors, "SKILL.md:8:", "Broken local reference 'missing.md'")


@pytest.mark.parametrize(
    "body",
    [
        "Text\n\n    [x](missing.md)\n    [y]: missing-def.md\n",  # Indented code block.
        "- item\n\n        [x](missing.md)\n",  # Indented code inside a list.
        "A paragraph\n[y]: missing.md\n",  # Not a definition: paragraph continuation.
        "Not a link: [x] (missing.md) and \\[x](missing.md).\n",
        "`code\nspan [x](missing.md)` spanning lines.\n",
        "<!--\n[x](missing.md)\n-->\n",  # HTML block.
    ],
)
def test_text_that_is_not_a_link_is_ignored(tmp_path, body):
    assert metadata_errors(tmp_path, VALID_FRONTMATTER, body) == []


# --------------------------------------------------------------------------
# Regression: SKILL.md must not be a symlink
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "target",
    ["../../outside.md", "docs/main.md", "../../missing.md"],
)
def test_symlinked_skill_file_is_rejected(tmp_path, target):
    (tmp_path / "outside.md").write_text(f"---\n{VALID_FRONTMATTER}\n---\n# B\n", encoding="utf-8")
    skill_dir = tmp_path / "skills" / "example"
    (skill_dir / "docs").mkdir(parents=True)
    (skill_dir / "docs" / "main.md").write_text(
        f"---\n{VALID_FRONTMATTER}\n---\n# B\n", encoding="utf-8"
    )
    (skill_dir / "SKILL.md").symlink_to(target)

    _, errors = validate_skills(tmp_path / "skills")

    assert len(errors) == 1
    assert_error(errors, "example/SKILL.md", "must be a regular file, not a symlink", target)


# --------------------------------------------------------------------------
# Regression: YAML construction errors
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("extra", "expected_error"),
    [
        ("created: 2024-13-45", "SKILL.md:4: Invalid YAML in frontmatter: invalid timestamp value '2024-13-45'"),
        ("count: !!int abc", "SKILL.md:4: Invalid YAML in frontmatter: invalid int value 'abc'"),
        ("ratio: !!float x", "SKILL.md:4: Invalid YAML in frontmatter: invalid float value 'x'"),
        ("metadata:\n  when: 2024-02-30", "SKILL.md:5: Invalid YAML in frontmatter: invalid timestamp value"),
        ("deep: " + "[" * 5000 + "]" * 5000, "SKILL.md:1: Invalid YAML in frontmatter: nested too deeply"),
    ],
)
def test_yaml_construction_errors_are_reported(tmp_path, extra, expected_error):
    errors = metadata_errors(tmp_path, f"{VALID_FRONTMATTER}\n{extra}")

    assert_error(errors, expected_error)


def test_yaml_construction_error_does_not_stop_the_scan(tmp_path, capsys):
    make_repo(tmp_path, "alpha", "beta")
    write_skill(tmp_path / "skills", "alpha", "name: alpha\ndescription: !!int abc")
    write_skill(tmp_path / "skills", "beta", "name: beta\ndescription: ''")

    assert main(["--root", str(tmp_path)]) == 1

    stderr = capsys.readouterr().err
    assert "alpha/SKILL.md:3: Invalid YAML in frontmatter: invalid int value 'abc'" in stderr
    assert "beta/SKILL.md:3: Invalid skill description: must not be empty" in stderr


# --------------------------------------------------------------------------
# Regression: path resolution errors
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("setup", "link", "expected_error"),
    [
        (
            lambda d: (d / "loop.md").symlink_to("loop.md"),
            "loop.md",
            "Invalid local reference 'loop.md': cannot resolve the path",
        ),
        (
            lambda d: ((d / "a.md").symlink_to("b.md"), (d / "b.md").symlink_to("a.md")),
            "a.md",
            "Invalid local reference 'a.md': cannot resolve the path",
        ),
        (None, "bad%00.md", "contains a null character"),
        (None, "a" * 300 + ".md", "cannot resolve the path"),
    ],
)
def test_path_resolution_errors_do_not_stop_validation(tmp_path, setup, link, expected_error):
    skill_dir = write_skill_md(tmp_path, "")
    if setup is not None:
        setup(skill_dir)
    (skill_dir / "SKILL.md").write_text(
        f"---\n{VALID_FRONTMATTER}\n---\n\n[bad]({link})\n\n[next](missing.md)\n",
        encoding="utf-8",
    )

    errors = validate_skill_metadata(skill_dir)

    assert len(errors) == 2
    assert_error(errors, "SKILL.md:6:", expected_error)
    assert_error(errors, "SKILL.md:8:", "Broken local reference 'missing.md'")


# --------------------------------------------------------------------------
# Regression: names reserved by Claude Code
# --------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["synced", "anthropic-skills"])
def test_claude_code_reserved_names_are_rejected(tmp_path, capsys, name):
    make_repo(tmp_path, name)

    assert main(["--root", str(tmp_path)]) == 1

    errors = capsys.readouterr().err.splitlines()
    assert len(errors) == 2  # The reserved-name error and the summary line.
    assert f".claude/skills/{name}: Reserved skill name {name!r}: Claude Code" in errors[0]
    assert ".agents/skills" not in "\n".join(errors)


@pytest.mark.parametrize("name", ["synced", "anthropic-skills"])
def test_reserved_names_are_client_specific(tmp_path, name):
    make_repo(tmp_path, name)
    skills = {name: tmp_path / "skills" / name}

    assert validate_symlinks(tmp_path / ".agents" / "skills", skills) == []
    assert_error(
        validate_symlinks(
            tmp_path / ".claude" / "skills",
            skills,
            ("Claude Code", frozenset({"anthropic-skills", "synced"})),
        ),
        "Reserved skill name",
    )


def test_names_similar_to_reserved_ones_are_allowed(tmp_path, capsys):
    make_repo(tmp_path, "synced-notes", "anthropic-skills-guide")

    assert main(["--root", str(tmp_path)]) == 0


# --------------------------------------------------------------------------
# Regression: PyYAML scalar constructor exceptions through the CLI
# --------------------------------------------------------------------------


def run_cli(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT_PATH / "scripts" / "validate_skills.py"), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    ("value", "expected_error"),
    [
        ("!!timestamp nope", "invalid timestamp value 'nope'"),
        ("!!bool nope", "invalid bool value 'nope'"),
        ("!!int ''", "invalid int value ''"),
    ],
)
def test_cli_reports_scalar_constructor_errors(tmp_path, value, expected_error):
    make_repo(tmp_path, "alpha")
    write_skill(tmp_path / "skills", "alpha", f"name: alpha\ndescription: Example\nextra: {value}")

    result = run_cli(tmp_path)

    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert f"alpha/SKILL.md:4: Invalid YAML in frontmatter: {expected_error}" in result.stderr
    assert "FAILED: 1 error(s) found." in result.stderr


def test_cli_continues_after_scalar_constructor_errors(tmp_path):
    make_repo(tmp_path, "alpha", "beta", "gamma", "delta", "omega")
    skills_path = tmp_path / "skills"
    write_skill(skills_path, "alpha", "name: alpha\ndescription: !!timestamp nope")
    write_skill(skills_path, "beta", "name: beta\ndescription: Example\nflag: !!bool nope")
    write_skill(skills_path, "gamma", "name: gamma\ndescription: Example\ncount: !!int ''")
    write_skill(skills_path, "delta", "name: delta\ndescription: ''")

    result = run_cli(tmp_path)

    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "alpha/SKILL.md:3: Invalid YAML in frontmatter: invalid timestamp value 'nope'" in result.stderr
    assert "beta/SKILL.md:4: Invalid YAML in frontmatter: invalid bool value 'nope'" in result.stderr
    assert "gamma/SKILL.md:4: Invalid YAML in frontmatter: invalid int value ''" in result.stderr
    assert "delta/SKILL.md:3: Invalid skill description: must not be empty" in result.stderr
    assert "omega" not in result.stderr  # The valid skill after the failures is still scanned.
    assert "FAILED: 4 error(s) found." in result.stderr
