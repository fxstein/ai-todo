# Release Process (PR-driven)

DEC-0098 migrates releases from bash scripts to a Python + GitHub Actions flow.

## Overview

1. Open a PR with release-ready changes.
2. Run the release preparation script locally:

```bash
python release/prepare_release.py [--beta] [--summary "optional summary"]
```

This script will:
- Read git history since the last `v*` tag
- Infer semver bump from conventional commits
- Optionally create a beta version (`bN`)
- Inject `release/AI_RELEASE_SUMMARY.md` (if present)
- Write `release/RELEASE_NOTES.md`
- Update versions in:
  - `pyproject.toml`
  - `ai_todo/__init__.py`
  - `legacy/todo.ai`

1. Commit the generated changes with a release commit message format:

```text
chore: Release vX.Y.Z
```

(or `chore: Release vX.Y.ZbN` for beta)

1. Merge PR to `main`.

## GitHub Actions Behavior

When a commit lands on `main` with message starting with `chore: Release v`:

- `create-release-tag` job runs
- It extracts the tag from commit message
- Pushes tag (if missing)
- Creates GitHub release via `gh release create`
- Exposes tag/version outputs for downstream release jobs

The existing PyPI publish pipeline continues to run using the created tag.

## Notes

- Conventional commits drive release bumping:
  - `major`: breaking changes (`!:` or `BREAKING CHANGE`)
  - `minor`: `feat:` commits
  - `patch`: all others
- Keep `release/RELEASE_NOTES.md` committed as part of the release PR.
