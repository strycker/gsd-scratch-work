---
name: CI SHA refresh
about: Monthly checklist to refresh pinned GitHub Action SHAs
title: "chore(ci): monthly GitHub Action SHA refresh"
labels: ["ci", "maintenance", "security", "ci-sha-refresh"]
assignees: []
---

## Summary

Refresh pinned GitHub Action SHAs to the latest commits for approved major tags/branches.

## Checklist

- [ ] Review `.github/workflows/*.yml` for pinned `uses:` refs.
- [ ] Update `actions/checkout` to latest `v4` commit SHA.
- [ ] Update `actions/setup-python` to latest `v5` commit SHA.
- [ ] Update `actions/upload-artifact` to latest `v4` commit SHA.
- [ ] Update `actions/download-artifact` to latest `v4` commit SHA.
- [ ] Update `pypa/gh-action-pypi-publish` to latest `release/v1` commit SHA.
- [ ] Keep inline comments showing source tag/branch (for readability).
- [ ] Run CI and confirm all workflows pass.
- [ ] Link PR and close this issue.

## Notes

- If an action update causes regressions, pin back to the previous known-good SHA and capture the reason in the PR.
