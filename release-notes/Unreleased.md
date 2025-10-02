# Unreleased

This release contains the following changes (from CHANGELOG.md):

- Add `python-tools/run.sh` launcher to create a local virtualenv and run the CLI or tests.
- Split runtime and dev dependencies into `requirements.txt` and `requirements-dev.txt`.
- Add test instructions and require running tests before PRs in `PULL_REQUEST_TEMPLATE.md`.
- Add GitHub Actions workflow to run Python tests on PRs.
- Update README files to document the launcher and running tests locally.

Notes:
- Tests were executed during development: `./python-tools/run.sh test` — 85 passed, 12 warnings.
- Pydantic deprecation warnings are present and should be addressed in a follow-up.
