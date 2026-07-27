"""Version metadata helpers for ai-todo."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ai_todo import __version__

APP_NAME = "ai-todo"
GIT_SHA_ENV_VARS = ("GIT_COMMIT_SHA", "GITHUB_SHA", "CI_COMMIT_SHA", "COMMIT_SHA")


@dataclass(frozen=True)
class VersionInfo:
    """Application version metadata."""

    app_name: str
    version: str
    commit_sha: str | None = None

    def to_dict(self) -> dict[str, str]:
        """Serialize the version metadata for JSON responses."""
        data: dict[str, str] = {"app_name": self.app_name, "version": self.version}
        if self.commit_sha:
            data["commit_sha"] = self.commit_sha
        return data


def _normalize_sha(value: str | None) -> str | None:
    if value is None:
        return None

    candidate = value.strip()
    return candidate or None


def get_commit_sha(project_root: str | Path | None = None) -> str | None:
    """Return the current Git commit SHA if one is available."""
    for env_var in GIT_SHA_ENV_VARS:
        sha = _normalize_sha(os.environ.get(env_var))
        if sha:
            return sha

    root = Path(project_root) if project_root is not None else Path.cwd()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None

    if result.returncode != 0:
        return None

    return _normalize_sha(result.stdout)


def get_version_info(project_root: str | Path | None = None) -> VersionInfo:
    """Return the app name, package version, and optional commit SHA."""
    return VersionInfo(
        app_name=APP_NAME,
        version=__version__,
        commit_sha=get_commit_sha(project_root),
    )
