# Publishing to PyPI

This guide walks you through publishing `drf-choices-mixin` to
[PyPI](https://pypi.org/) (and optionally [TestPyPI](https://test.pypi.org/)
for a dry run).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.
- A [PyPI account](https://pypi.org/account/register/).
- An API token for PyPI (see below).

## Creating an API token

1. Log in to [pypi.org](https://pypi.org/account/login/).
2. Go to **Account Settings → API tokens**
   ([direct link](https://pypi.org/manage/account/token/)).
3. Click **Add API token**.
4. For the first upload, set the scope to **Entire account**. After the
   first successful publish you can create a project-scoped token and
   revoke the broad one.
5. Copy the token — it starts with `pypi-` and is only shown once.

## Configuring the token

`uv publish` picks up credentials in this order:

1. **Environment variable** (recommended for CI and one-off usage):

   ```bash
   export UV_PUBLISH_TOKEN=pypi-xxxx...
   ```

2. **`--token` flag** (inline):

   ```bash
   uv publish --token pypi-xxxx...
   ```

3. **`~/.pypirc` file** (persistent):

   ```ini
   [pypi]
   username = __token__
   password = pypi-xxxx...
   ```

Pick whichever method suits your workflow. The environment variable is the
simplest for a single publish and avoids storing the token on disk.

## Publishing

### 1. Verify the package is ready

```bash
make lint
make test
```

Both must pass with zero errors before publishing.

### 2. Check the version

Open `pyproject.toml` and confirm the `version` field is correct. PyPI does
not allow re-uploading the same version — once `0.1.0` is published, you
cannot overwrite it.

### 3. Build

```bash
make build
```

This removes any previous `dist/` directory and builds both a source
distribution (`.tar.gz`) and a wheel (`.whl`) into `dist/`.

You can inspect the contents of the wheel to make sure everything looks
right:

```bash
unzip -l dist/drf_choices_mixin-*.whl
```

You should see `drf_choices_mixin/__init__.py`,
`drf_choices_mixin/mixins.py`, the `METADATA`, and the `LICENSE` — nothing
else.

### 4. Upload to PyPI

```bash
make publish
```

Or, if you set the token inline:

```bash
UV_PUBLISH_TOKEN=pypi-xxxx... make publish
```

Once complete, verify the package at
[pypi.org/project/drf-choices-mixin](https://pypi.org/project/drf-choices-mixin/).

## Testing with TestPyPI (optional but recommended)

TestPyPI is a separate instance of PyPI meant for experimentation. It is a
good idea to publish there first to make sure everything looks correct.

### 1. Create a TestPyPI account and token

- Register at [test.pypi.org/account/register](https://test.pypi.org/account/register/).
- Create a token at [test.pypi.org/manage/account/token](https://test.pypi.org/manage/account/token/).

### 2. Publish to TestPyPI

```bash
UV_PUBLISH_TOKEN=pypi-xxxx... make publish-test
```

### 3. Verify

Check the package at
`https://test.pypi.org/project/drf-choices-mixin/`.

You can install it from TestPyPI to confirm it works:

```bash
pip install --index-url https://test.pypi.org/simple/ drf-choices-mixin
```

Note: dependencies like Django and DRF are not on TestPyPI, so you may need
to install them separately first.

## Releasing a new version

1. Update the `version` in `pyproject.toml`.
2. Commit the version bump: `git commit -am "Bump version to X.Y.Z"`.
3. Tag the release: `git tag vX.Y.Z`.
4. Push the commit and tag: `git push && git push --tags`.
5. Build and publish: `make publish`.

## Makefile reference

| Command | Description |
|---|---|
| `make build` | Clean `dist/` and build sdist + wheel |
| `make publish` | Build and upload to PyPI |
| `make publish-test` | Build and upload to TestPyPI |
| `make clean` | Remove `dist/` |