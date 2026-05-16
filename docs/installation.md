# Installation

## Requirements

- **Python**: 3.9 or newer. Tested on 3.9 / 3.10 / 3.11 / 3.12 / 3.13.
- **OS**: Linux, macOS, Windows — pure-Python, no native build step.
- **Dependencies**: `requests >= 2.28` (installed automatically).

## Install from PyPI

```bash
pip install capzy
```

> ⏳ The PyPI listing is pending approval. Until it goes live, see **Install from source** below.

To upgrade later:

```bash
pip install --upgrade capzy
```

## Install from source

While the PyPI listing is pending, install straight from GitHub:

```bash
pip install "git+https://github.com/capzy/capzy-pip.git"
```

Pin to a specific tag once releases are cut:

```bash
pip install "git+https://github.com/capzy/capzy-pip.git@v0.0.1"
```

## Verify the install

```bash
python -c "import capzy; print(capzy.__version__)"
# → 0.0.1
```

## Install in a virtual environment (recommended)

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install capzy
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install capzy
```

## Install for development

If you've cloned the repo and want to hack on `capzy` itself:

```bash
git clone https://github.com/capzy/capzy-pip.git
cd capzy-pip
python -m venv .venv
source .venv/bin/activate   # (or .venv\Scripts\Activate.ps1 on Windows)
pip install -e ".[dev]"
pytest
```

## Optional: install for use with `uv` or `poetry`

`uv`:

```bash
uv pip install capzy
```

`poetry`:

```bash
poetry add capzy
```

## Troubleshooting

**`ssl.SSLCertVerificationError`** — your system's CA bundle is outdated. On
macOS run `/Applications/Python\ 3.x/Install\ Certificates.command`. On
Linux update `ca-certificates` (`apt`, `dnf`, etc.). The SDK uses the
standard `requests` TLS path — anything that works for `pip` works here.

**`ModuleNotFoundError: No module named 'capzy'`** — you installed into a
different interpreter than you're running. Confirm with
`python -c "import sys; print(sys.executable)"` matches the `pip` you used.

**Conflicting `requests` version** — `capzy` requires `requests >= 2.28`. Run
`pip install -U requests` if your project pins something older.

---

Next: [Getting started →](./getting-started.md)
