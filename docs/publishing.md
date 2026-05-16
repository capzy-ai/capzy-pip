# Publishing a release

The repo uploads to PyPI automatically via GitHub Actions + **Trusted
Publisher (OIDC)** — there are no secrets stored anywhere. The
`.github/workflows/publish.yml` workflow fires on every GitHub Release
and uploads the built sdist + wheel.

> Trusted Publisher is configured at
> https://pypi.org/manage/account/publishing/ → project `capzy` → owner
> `capzy-ai`, repo `capzy-pip`, workflow `publish.yml`.

## Cutting a release

1. **Bump the version** in two places (they must match):
   - `pyproject.toml` → `version = "X.Y.Z"`
   - `capzy/_version.py` → `__version__ = "X.Y.Z"`

2. **Add a CHANGELOG entry** in [`CHANGELOG.md`](../CHANGELOG.md) under a
   new `## [X.Y.Z] — YYYY-MM-DD` heading.

3. **Commit + push to `main`:**
   ```bash
   git add pyproject.toml capzy/_version.py CHANGELOG.md
   git commit -m "vX.Y.Z"
   git push origin main
   ```

4. **Tag + push the tag:**
   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin vX.Y.Z
   ```

5. **Draft + publish the release on GitHub:**
   - https://github.com/capzy-ai/capzy-pip/releases/new
   - Pick the tag you just pushed.
   - Title: `vX.Y.Z`.
   - Body: paste the CHANGELOG entry for this version.
   - **Publish release.**

6. **Watch it deploy:**
   https://github.com/capzy-ai/capzy-pip/actions — the
   `Publish to PyPI` workflow runs in ~60 seconds.

7. **Verify:**
   ```bash
   python -m venv /tmp/capzy-smoke
   /tmp/capzy-smoke/bin/pip install --upgrade capzy
   /tmp/capzy-smoke/bin/python -c "import capzy; print(capzy.__version__)"
   ```

## If a release goes wrong

- **Wrong content uploaded:** PyPI does NOT allow re-uploading the same
  version. You can `yank` the bad release (still installable for people
  who pinned it, hidden from `pip install capzy`) at
  https://pypi.org/manage/project/capzy/release/X.Y.Z/ → Yank.
- **Workflow failed mid-upload:** safe to re-run the failed
  `Publish to PyPI` job from the Actions tab — Trusted Publisher mints
  a fresh OIDC token each run.
- **Need to roll back:** bump version and ship a `X.Y.(Z+1)` with the
  desired contents. Yanking does not delete; it just deprioritises.

## Optional: add a manual-approval gate

If you want a human-in-the-loop confirmation before each PyPI upload:

1. GitHub repo → Settings → Environments → **New environment** → name
   `pypi` → enable **Required reviewers** and add yourself.
2. In `.github/workflows/publish.yml`, uncomment the
   `environment: pypi` line under the `publish` job.
3. On the PyPI Trusted Publisher form, set **Environment name** to
   `pypi` to match.

Every release will then wait for your approval click in the Actions UI
before uploading.
