# Publishing to PyPI

> Internal cheat-sheet for cutting a release once the PyPI listing is
> approved. Pinned to `0.0.1` in the repo until then.

## Pre-flight checklist

- [ ] `pyproject.toml` → bump `version`.
- [ ] `capzy/__init__.py` → bump `__version__` to match.
- [ ] `CHANGELOG.md` → add a dated entry.
- [ ] All examples still run against the live API.
- [ ] `pytest` is green.
- [ ] README rendered preview looks right on GitHub.

## Build

```bash
python -m pip install --upgrade build twine
python -m build
```

This produces `dist/capzy-X.Y.Z.tar.gz` and `dist/capzy-X.Y.Z-py3-none-any.whl`.

## Smoke test the wheel

```bash
python -m venv /tmp/capzy-smoke
/tmp/capzy-smoke/bin/pip install dist/capzy-X.Y.Z-py3-none-any.whl
/tmp/capzy-smoke/bin/python -c "import capzy; print(capzy.__version__)"
```

## Upload to TestPyPI first

```bash
python -m twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --no-deps capzy
```

## Upload to PyPI

```bash
python -m twine upload dist/*
```

Use an API token, not a password. Store it in `~/.pypirc`:

```ini
[pypi]
  username = __token__
  password = pypi-AgEIcHl...
```

## Tag the release

```bash
git tag -a v0.1.0 -m "v0.1.0: first PyPI release"
git push origin v0.1.0
```

## Post-release

- Update the install instructions in the top-level `README.md` (remove
  the "PyPI listing is pending" callout).
- Drop the `git+https://...` install instruction or move it under a
  "Bleeding edge" subsection.
