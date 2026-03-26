"""Contract test: secret paths stay listed in .gitignore (INSTALL-20 / EMAIL-10)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_gitignore_lists_env_and_email_local() -> None:
    lines = (_repo_root() / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in lines, "root .env should be gitignored"
    assert any("email.local.yaml" in line for line in lines), (
        "email.local.yaml pattern should be gitignored"
    )
