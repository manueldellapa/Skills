"""Validate the canonical skills in ``skills/`` and their agent symlinks.

Each skill lives once in ``skills/<name>/`` and is exposed to coding agents
through relative symlinks in ``.agents/skills/`` (Codex) and
``.claude/skills/`` (Claude Code). Frontmatter rules follow the Agent Skills
specification: https://agentskills.io/specification

Usage: python scripts/validate_skills.py [--root PATH]
"""

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
    from markdown_it import MarkdownIt
except ModuleNotFoundError as exc:  # pragma: no cover - depends on the environment
    sys.exit(
        f"ERROR: missing dependency {exc.name!r}. "
        "Install the dev dependencies with: python -m pip install --group dev"
    )

ROOT_PATH = Path(__file__).resolve().parent.parent

SKILLS_DIR = Path("skills")
AGENT_DIRS = (
    Path(".agents") / "skills",
    Path(".claude") / "skills",
)

SKILLS_PATH = ROOT_PATH / SKILLS_DIR
AGENT_PATHS = tuple(ROOT_PATH / agent_dir for agent_dir in AGENT_DIRS)

# Client-specific rules, applied only to that client's agent directory:
# agent directory -> (client name, skill names the client reserves).
RESERVED_SKILL_NAMES = {
    Path(".claude") / "skills": ("Claude Code", frozenset({"anthropic-skills", "synced"})),
}

SKILL_FILE = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
UTF8_BOM = "﻿"

NAME_MAX_LENGTH = 64
DESCRIPTION_MAX_LENGTH = 1024
COMPATIBILITY_MAX_LENGTH = 500

_NAME_ALLOWED_CHARS = re.compile(r"[a-z0-9-]")
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_MARKDOWN = MarkdownIt("commonmark")

_TYPE_NAMES = {
    bool: "boolean",
    int: "integer",
    float: "number",
    str: "string",
    list: "list",
    dict: "mapping",
    type(None): "null",
}


class _FrontmatterError(Exception):
    """A SKILL.md problem that prevents reading its metadata."""

    def __init__(self, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line


class _DuplicateKeyError(yaml.constructor.ConstructorError):
    def __init__(self, key: object, mark: yaml.Mark) -> None:
        super().__init__(problem=f"found duplicate key {key!r}", problem_mark=mark)
        self.key = key


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate keys instead of keeping the last one.

    It also turns the exceptions that PyYAML's scalar constructors raise on
    malformed input (``2024-13-45``, ``!!int abc``, ``!!timestamp nope``,
    ``!!bool nope``, ``!!int ''``...) into YAML errors with a position.
    Only scalar nodes are wrapped: their constructors run no code of ours,
    so a programming error elsewhere still surfaces as a traceback.
    """

    def construct_object(self, node, deep=False):
        if not isinstance(node, yaml.ScalarNode):
            return super().construct_object(node, deep=deep)

        try:
            return super().construct_object(node, deep=deep)
        except (
            AttributeError,  # !!timestamp nope: the timestamp regex does not match.
            IndexError,  # !!int '': the constructor reads value[0].
            KeyError,  # !!bool nope: unknown boolean literal.
            OverflowError,
            TypeError,
            ValueError,  # 2024-13-45, !!int abc, !!float x.
        ) as exc:
            tag = node.tag.rsplit(":", 1)[-1]
            # Only these messages describe the value; the others are internal.
            detail = f" ({exc})" if isinstance(exc, (ValueError, OverflowError)) else ""
            raise yaml.constructor.ConstructorError(
                problem=f"invalid {tag} value {node.value!r}{detail}",
                problem_mark=node.start_mark,
            ) from exc

    def construct_mapping(self, node, deep=False):
        seen = set()

        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                continue

            key = self.construct_object(key_node, deep=deep)

            try:
                is_duplicate = key in seen
            except TypeError:
                continue  # Unhashable key: reported by the base constructor.

            if is_duplicate:
                raise _DuplicateKeyError(key, key_node.start_mark)

            seen.add(key)

        return super().construct_mapping(node, deep=deep)


def _display(path: Path) -> str:
    """Return ``path`` relative to the working directory when possible."""
    try:
        return str(path.absolute().relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _error(path: Path, message: str, line: int | None = None) -> str:
    location = _display(path) if line is None else f"{_display(path)}:{line}"
    return f"{location}: {message}"


def _type_name(value: object) -> str:
    return _TYPE_NAMES.get(type(value), type(value).__name__)


def validate_skills(skills_path: Path) -> tuple[dict[str, Path], list[str]]:
    """Validate every skill directory and detect duplicate skill names.

    Returns the skill directories keyed by directory name, plus the errors.
    """
    skills: dict[str, Path] = {}
    errors: list[str] = []
    declared_names: dict[str, Path] = {}

    if not skills_path.is_dir():
        return skills, [_error(skills_path, "Missing skills directory")]

    try:
        entries = sorted(skills_path.iterdir())
    except OSError as exc:
        return skills, [_error(skills_path, f"Cannot list skills directory: {exc}")]

    for entry in entries:
        if entry.name.startswith("."):
            continue

        if entry.is_symlink():
            errors.append(_error(
                entry,
                "Invalid skill directory: must be a real directory, not a "
                "symlink (skills/ holds the canonical copy of each skill)",
            ))
            continue

        if not entry.is_dir():
            errors.append(_error(
                entry,
                "Unexpected file in skills directory: only skill directories "
                "are allowed here (hidden files are ignored)",
            ))
            continue

        skills[entry.name] = entry
        skill_file = entry / SKILL_FILE

        if not skill_file.is_file() and not skill_file.is_symlink():
            errors.append(_error(skill_file, "Missing SKILL.md"))
            continue

        name, name_line, skill_errors = _validate_skill_file(entry)
        errors.extend(skill_errors)

        if name is None:
            continue

        if name in declared_names:
            errors.append(_error(
                skill_file,
                f"Duplicate skill name {name!r}: already declared in "
                f"{_display(declared_names[name])}",
                name_line,
            ))
        else:
            declared_names[name] = skill_file

    if not skills:
        errors.append(_error(skills_path, "No skills found"))

    return skills, errors


def validate_symlinks(
    agent_path: Path,
    skills: dict[str, Path],
    reserved: tuple[str, frozenset[str]] | None = None,
) -> list[str]:
    """Check that ``agent_path`` exposes each skill through a portable symlink.

    ``reserved`` is ``(client, names)`` for skill names that the client
    reading ``agent_path`` reserves for itself.
    """
    errors: list[str] = []

    if not agent_path.is_dir():
        return [_error(
            agent_path,
            "Missing agent directory: create it with a relative symlink "
            "to each skill in skills/",
        )]

    for name, skill_dir in skills.items():
        link = agent_path / name
        expected = os.path.relpath(skill_dir.absolute(), agent_path.absolute())

        if reserved is not None and name in reserved[1]:
            errors.append(_error(
                link,
                f"Reserved skill name {name!r}: {reserved[0]} reserves it and "
                f"cannot load a skill with this name; rename skills/{name}",
            ))
            continue

        if not link.is_symlink():
            if not link.exists():
                problem = "Missing symlink"
            elif link.is_dir():
                problem = "Invalid agent entry: found a directory instead of a symlink"
            else:
                problem = (
                    "Invalid agent entry: found a regular file instead of a "
                    "symlink (is git core.symlinks disabled?)"
                )
            errors.append(_error(link, f"{problem}; expected a symlink to {expected!r}"))
            continue

        target = os.readlink(link)

        if os.path.isabs(target):
            errors.append(_error(
                link,
                f"Absolute symlink target {target!r} is not portable; "
                f"use the relative target {expected!r}",
            ))
            continue

        try:
            resolved = link.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            errors.append(_error(
                link,
                f"Broken symlink -> {target!r} ({exc}); expected {expected!r}",
            ))
            continue

        if resolved != skill_dir.resolve():
            errors.append(_error(
                link,
                f"Invalid symlink target {target!r}: resolves to {_display(resolved)}, "
                f"expected {expected!r}",
            ))
        elif os.path.normpath(target) != expected:
            errors.append(_error(
                link,
                f"Non-canonical symlink target {target!r}: it resolves correctly "
                f"here but is not portable; use {expected!r}",
            ))

    try:
        entries = sorted(agent_path.iterdir())
    except OSError as exc:
        return errors + [_error(agent_path, f"Cannot list agent directory: {exc}")]

    for entry in entries:
        if entry.name.startswith("."):
            continue

        if entry.name not in skills:
            errors.append(_error(
                entry,
                "Unexpected agent entry: no matching skill directory in skills/",
            ))

    return errors


def validate_skill_metadata(skill_dir: Path) -> list[str]:
    """Validate ``SKILL.md`` frontmatter, body and local references."""
    return _validate_skill_file(skill_dir)[2]


def _validate_skill_file(skill_dir: Path) -> tuple[str | None, int | None, list[str]]:
    """Return the declared name, its line and the errors for one skill."""
    skill_file = skill_dir / SKILL_FILE

    try:
        metadata, frontmatter_lines, body_lines, body_start = _parse_skill_file(skill_file)
    except _FrontmatterError as exc:
        return None, None, [_error(skill_file, str(exc), exc.line)]

    def line_of(key: str) -> int | None:
        pattern = re.compile(rf"^{re.escape(key)}\s*:")
        for index, line in enumerate(frontmatter_lines, start=2):
            if pattern.match(line):
                return index
        return 1

    errors: list[str] = []
    name = metadata.get("name")
    name_line = line_of("name")

    errors.extend(
        _error(skill_file, problem, name_line)
        for problem in _name_problems(metadata, skill_dir.name)
    )
    errors.extend(
        _error(skill_file, problem, line_of("description"))
        for problem in _description_problems(metadata)
    )
    errors.extend(
        _error(skill_file, problem, line_of(key))
        for key, problem in _optional_field_problems(metadata)
    )

    if not "\n".join(body_lines).strip():
        errors.append(_error(
            skill_file,
            "Missing skill instructions: the Markdown body after the "
            "frontmatter is empty",
        ))

    errors.extend(_reference_errors(skill_dir, skill_file, body_lines, body_start))

    return (name if isinstance(name, str) else None), name_line, errors


def _parse_skill_file(skill_file: Path) -> tuple[dict, list[str], list[str], int]:
    """Split SKILL.md into parsed frontmatter and body.

    Returns ``(metadata, frontmatter_lines, body_lines, body_start_line)``.
    """
    if skill_file.is_symlink():
        raise _FrontmatterError(
            f"SKILL.md must be a regular file, not a symlink (-> "
            f"{os.readlink(skill_file)!r}): the canonical skill must not "
            "depend on other files or on non-portable links",
        )

    try:
        text = skill_file.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _FrontmatterError(f"SKILL.md is not valid UTF-8: {exc}") from exc
    except OSError as exc:
        raise _FrontmatterError(f"Cannot read SKILL.md: {exc}") from exc

    if text.startswith(UTF8_BOM):
        raise _FrontmatterError(
            "SKILL.md starts with a UTF-8 BOM; save it as UTF-8 without BOM "
            "so every agent detects the frontmatter",
            1,
        )

    lines = text.splitlines()

    if not lines or lines[0].rstrip() != FRONTMATTER_DELIMITER:
        raise _FrontmatterError(
            "Missing YAML frontmatter: the first line must be '---'", 1
        )

    end = next(
        (
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.rstrip() == FRONTMATTER_DELIMITER
        ),
        None,
    )

    if end is None:
        raise _FrontmatterError(
            "Unclosed YAML frontmatter: add a closing '---' line at column 1", 1
        )

    frontmatter_lines = lines[1:end]

    try:
        metadata = yaml.load("\n".join(frontmatter_lines), Loader=_UniqueKeySafeLoader)
    except _DuplicateKeyError as exc:
        raise _FrontmatterError(
            f"Duplicate YAML key {exc.key!r} in frontmatter",
            exc.problem_mark.line + 2,
        ) from exc
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        problem = getattr(exc, "problem", None) or str(exc)
        raise _FrontmatterError(
            f"Invalid YAML in frontmatter: {problem}",
            mark.line + 2 if mark is not None else None,
        ) from exc
    except RecursionError as exc:
        raise _FrontmatterError(
            "Invalid YAML in frontmatter: nested too deeply", 1
        ) from exc

    if metadata is None:
        raise _FrontmatterError(
            "Empty YAML frontmatter: required fields 'name' and "
            "'description' are missing",
            1,
        )

    if not isinstance(metadata, dict):
        raise _FrontmatterError(
            f"Frontmatter must be a YAML mapping, got {_type_name(metadata)}", 2
        )

    return metadata, frontmatter_lines, lines[end + 1:], end + 2


def _name_problems(metadata: dict, dir_name: str) -> list[str]:
    if "name" not in metadata:
        return ["Invalid skill name: missing required field 'name'"]

    name = metadata["name"]

    if not isinstance(name, str):
        return [f"Invalid skill name: expected a string, got {_type_name(name)}"]

    prefix = f"Invalid skill name {name!r}"
    problems: list[str] = []

    if not 1 <= len(name) <= NAME_MAX_LENGTH:
        problems.append(
            f"{prefix}: must be 1-{NAME_MAX_LENGTH} characters (got {len(name)})"
        )

    invalid_chars = sorted(set(_NAME_ALLOWED_CHARS.sub("", name)))

    if invalid_chars:
        problems.append(
            f"{prefix}: invalid character(s) "
            f"{', '.join(repr(char) for char in invalid_chars)}; "
            "use only lowercase letters a-z, digits 0-9 and hyphens"
        )

    if name.startswith("-") or name.endswith("-"):
        problems.append(f"{prefix}: must not start or end with a hyphen")

    if "--" in name:
        problems.append(f"{prefix}: must not contain consecutive hyphens")

    if not problems and name != dir_name:
        problems.append(
            f"Skill name {name!r} does not match directory {dir_name!r}; "
            "rename the directory or the 'name' field"
        )

    return problems


def _description_problems(metadata: dict) -> list[str]:
    if "description" not in metadata:
        return ["Invalid skill description: missing required field 'description'"]

    description = metadata["description"]

    if not isinstance(description, str):
        return [
            "Invalid skill description: expected a string, "
            f"got {_type_name(description)}"
        ]

    if not description.strip():
        return ["Invalid skill description: must not be empty"]

    if len(description) > DESCRIPTION_MAX_LENGTH:
        return [
            f"Invalid skill description: must be at most "
            f"{DESCRIPTION_MAX_LENGTH} characters (got {len(description)})"
        ]

    return []


def _optional_field_problems(metadata: dict) -> list[tuple[str, str]]:
    """Check the optional fields defined by the Agent Skills specification.

    Other fields are allowed: agents such as Claude Code define extensions.
    """
    problems: list[tuple[str, str]] = []

    if "license" in metadata:
        value = metadata["license"]
        if not isinstance(value, str):
            problems.append((
                "license",
                f"Invalid 'license': expected a string, got {_type_name(value)}",
            ))
        elif not value.strip():
            problems.append(("license", "Invalid 'license': must not be empty"))

    if "compatibility" in metadata:
        value = metadata["compatibility"]
        if not isinstance(value, str):
            problems.append((
                "compatibility",
                f"Invalid 'compatibility': expected a string, got {_type_name(value)}",
            ))
        elif not value.strip():
            problems.append((
                "compatibility",
                "Invalid 'compatibility': must not be empty (omit the field instead)",
            ))
        elif len(value) > COMPATIBILITY_MAX_LENGTH:
            problems.append((
                "compatibility",
                f"Invalid 'compatibility': must be at most "
                f"{COMPATIBILITY_MAX_LENGTH} characters (got {len(value)})",
            ))

    if "metadata" in metadata:
        value = metadata["metadata"]
        if not isinstance(value, dict):
            problems.append((
                "metadata",
                "Invalid 'metadata': expected a mapping of string keys to "
                f"string values, got {_type_name(value)}",
            ))
        else:
            for key, item in value.items():
                if not isinstance(key, str):
                    problems.append((
                        "metadata",
                        f"Invalid 'metadata' key {key!r}: expected a string, "
                        f"got {_type_name(key)}",
                    ))
                elif not isinstance(item, str):
                    problems.append((
                        "metadata",
                        f"Invalid 'metadata.{key}': expected a string, got "
                        f"{_type_name(item)}; quote the value",
                    ))

    if "allowed-tools" in metadata:
        value = metadata["allowed-tools"]
        if not isinstance(value, str) or not value.strip():
            problems.append((
                "allowed-tools",
                "Invalid 'allowed-tools': expected a non-empty space-separated "
                f"string of tool names, got {_type_name(value)}",
            ))

    return problems


def _iter_links(body_lines: list[str], first_line: int):
    """Yield ``(line_number, href)`` for each link destination in the body.

    The body is parsed as CommonMark, so code blocks (fenced or indented),
    code spans and text that only looks like a link are ignored, while links
    spanning several lines are found. Reference definitions are reported at
    their own line; links that use them are not reported again.
    """
    env: dict = {}
    tokens = _MARKDOWN.parse("\n".join(body_lines), env)
    definitions = env.get("references", {}).values()
    defined_hrefs = {definition["href"] for definition in definitions}

    for definition in definitions:
        yield first_line + definition["map"][0], definition["href"]

    for token in tokens:
        if token.type != "inline" or token.map is None:
            continue

        # Inline tokens carry no position: count the line breaks before each
        # link from the first line of its block.
        line_number = first_line + token.map[0]

        for child in token.children or ():
            if child.type in ("softbreak", "hardbreak"):
                line_number += 1
            elif child.type == "html_inline":
                line_number += child.content.count("\n")
            elif child.type in ("link_open", "image"):
                href = child.attrGet("href" if child.type == "link_open" else "src")
                if isinstance(href, str) and href not in defined_hrefs:
                    yield line_number, href


def _reference_errors(
    skill_dir: Path,
    skill_file: Path,
    body_lines: list[str],
    first_line: int,
) -> list[str]:
    """Check that local Markdown links resolve to files inside the skill."""
    errors: list[str] = []
    skill_root = skill_dir.resolve()

    for line_number, href in _iter_links(body_lines, first_line):
        if (
            not href
            or href.startswith("#")
            or href.startswith("//")
            or _URL_SCHEME.match(href)
        ):
            continue  # Anchor or external URL.

        path_text = unquote(re.split(r"[?#]", href, maxsplit=1)[0])
        target = unquote(href)

        if not path_text:
            continue

        if "\0" in path_text:
            errors.append(_error(
                skill_file,
                f"Invalid local reference {target!r}: contains a null character",
                line_number,
            ))
            continue

        if os.path.isabs(path_text):
            errors.append(_error(
                skill_file,
                f"Invalid local reference {target!r}: absolute paths are not "
                "portable; use a path relative to the skill directory",
                line_number,
            ))
            continue

        candidate = skill_dir / path_text

        try:
            inside = candidate.resolve().is_relative_to(skill_root)
            exists = inside and candidate.exists()
        except (OSError, RuntimeError, ValueError) as exc:
            # Symlink loops, names too long, permission errors...
            errors.append(_error(
                skill_file,
                f"Invalid local reference {target!r}: cannot resolve the path ({exc})",
                line_number,
            ))
            continue

        if not inside:
            errors.append(_error(
                skill_file,
                f"Invalid local reference {target!r}: points outside the skill "
                "directory; skills must be self-contained",
                line_number,
            ))
        elif not exists:
            errors.append(_error(
                skill_file,
                f"Broken local reference {target!r}: file not found",
                line_number,
            ))

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the skills in skills/ and their agent symlinks.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT_PATH,
        help="repository root to validate (default: this repository)",
    )
    args = parser.parse_args(argv)

    skills, errors = validate_skills(args.root / SKILLS_DIR)

    for agent_dir in AGENT_DIRS:
        errors.extend(validate_symlinks(
            args.root / agent_dir, skills, RESERVED_SKILL_NAMES.get(agent_dir)
        ))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)

        print(f"FAILED: {len(errors)} error(s) found.", file=sys.stderr)
        return 1

    print(f"OK: {len(skills)} skill(s) validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
