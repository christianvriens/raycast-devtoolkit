Enabling repository-local git hooks
=================================

This repository includes a `.githooks/` directory with a `pre-commit` hook that runs the test-suite before each commit.

To enable the hooks locally (this updates your local git config only):

```bash
chmod +x scripts/enable-local-githooks.sh
./scripts/enable-local-githooks.sh
```

When you run the script it will print a reminder message and set `core.hooksPath` to `.githooks`.

If you prefer to run tests manually, run:

```bash
./python-tools/run.sh test
```

Note: This change is local to your machine; other contributors must run the script on their machines to enable hooks.
