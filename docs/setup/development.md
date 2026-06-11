---
icon: lucide/wrench
hide:
  - path
---



# Development

Development setup instructions for **tenderness**.


## Environment setup

```bash
# Deactivate current env (if active)
deactivate

# Delete old venv (if needed)
rm -rf .venv

# Create new venv
uv venv --python 3.13

# Activate new venv
source .venv/bin/activate

# Install all project deps (including dev group)
uv sync --group dev

# Check installed packages
uv pip list 
```


## [pre-commit](https://github.com/pre-commit/pre-commit)

```bash
# Check pre-commit version
pre-commit --version

# Install pre-commit hooks
pre-commit install

# Run pre-commit hooks on all files
pre-commit run --all-files
```


## [mypy](https://github.com/python/mypy)

```bash
# Run mypy type checks
uv run mypy
```


## [pytest](https://github.com/pytest-dev/pytest)

```bash
# Run all tests
uv run pytest
```

## [pydoclint](https://github.com/jsh9/pydoclint)

```bash
# Run pydoclint on source
uv run pydoclint src
```


## [tox](https://github.com/tox-dev/tox)


```bash
# Install tox globally with uv
uv tool install tox --with tox-uv

# Check tox version
tox --version

# Check available tox environments
tox -l

# Run all environments
tox

# Run all environments in parallel
tox -p auto

# Run a specific environment
tox -e 3.13
```


## Publishing

### 1. Bump the version

```bash
# Bump patch (0.0.0 → 0.0.1)
uv version --bump patch

# Bump minor (0.0.0 → 0.1.0)
uv version --bump minor

# Bump major (0.0.0 → 1.0.0)
uv version --bump major

# Set an exact version
uv version 1.0.0

# Preview without writing
uv version 1.0.0 --dry-run
```

### 2. Commit and tag

```bash
# Stage the version bump
git add pyproject.toml

# Commit with the new version
git commit -m "chore: bump version to 0.1.0"

# Create an annotated tag
git tag -a v0.1.0 -m "v0.1.0"

# Push commit and tag
git push && git push --tags
```

### 3. Build the package

```bash
# Build source dist + wheel into dist/
uv build --no-sources
```

### 4. Publish to PyPI

```bash
export UV_PUBLISH_TOKEN=<your-pypi-token>
uv publish
```

Get a PyPI token at: https://pypi.org/manage/account/token/

### 5. Verify the install

```bash
uv run --with tenderness --no-project -- python -c "import tenderness"
```