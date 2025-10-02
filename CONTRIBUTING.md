# Contributing

Please run the test-suite and ensure all tests pass before creating a pull request.

Local pre-commit hooks
- The repository includes local hooks under `.githooks/`.
- To enable them, run:

```bash
chmod +x scripts/enable-local-githooks.sh
./scripts/enable-local-githooks.sh
```

This sets `core.hooksPath` to `.githooks`, enabling the `pre-commit` hook which runs `./python-tools/run.sh test` prior to every commit. If tests fail, the commit will be aborted.

If you prefer not to use local hooks, run the test-suite manually:

```bash
./python-tools/run.sh test
```
