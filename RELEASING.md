# Release process

This project is **not** published to PyPI: the `result` name there belongs to
the upstream rustedpy/result project. A release is a signed git tag plus a
GitHub Release with the wheel and sdist attached. The version is defined only
in `pyproject.toml`; `result.__version__` and the docs read it from the
installed package metadata.

`main` is protected, so the release commit goes through a pull request.

1) Create a release branch and set the version being released:
```
export VERSION={VERSION BEING RELEASED}   # for example '0.19.0'
git switch main && git pull
git switch -c release/${VERSION}
vim pyproject.toml    # version = "${VERSION}"
uv lock
```

2) Update `CHANGELOG.md`:
- Add a `## [${VERSION}] - YYYY-MM-DD` heading above the entries under
  `## [Unreleased]`, so that `[Unreleased]` is empty again. The release
  workflow uses the text under this heading as the release notes and fails if
  it is missing, so keep the `## [${VERSION}]` form.
- Update the link references at the bottom: point `[Unreleased]` at
  `compare/v${VERSION}...HEAD` and add
  `[${VERSION}]: https://github.com/john-parton/result/releases/tag/v${VERSION}`.

3) Update the pinned tag in the README's Installation section (the release
link, the pip and uv commands, the `pyproject.toml` example and the wheel
URL):
```
grep -n "v0\.\|0\.[0-9]*\.[0-9]*-py3" README.md
```

4) Check everything, then open a pull request and merge it (squash):
```
uv run ruff check && uv run ruff format --check
uv run pyrefly check
uv run pytest
uv run --group docs sphinx-build -b html -W docs docs/_build/html
git add pyproject.toml uv.lock CHANGELOG.md README.md
git commit -m "Release v${VERSION}"
git push -u origin HEAD
gh pr create -R john-parton/result
```

5) Tag the merged commit with a signed tag and push it:
```
git switch main && git pull
git tag -s v${VERSION} -m "Release v${VERSION}"
git push origin v${VERSION}
```
Pushing the tag runs the `Release` workflow (`.github/workflows/release.yml`).
It checks that the tag matches the version in `pyproject.toml`, builds the
wheel and sdist with `uv build`, and creates the GitHub Release with the
changelog entry as its notes.

6) Check the release:
- https://github.com/john-parton/result/releases
- the wheel is attached, for example
  `result-${VERSION}-py3-none-any.whl`, and installs with
  `pip install "git+https://github.com/john-parton/result@v${VERSION}"`

7) Start the next development version in a pull request. For example, after
`v0.19.0` set `version = "0.20.0.dev0"` in `pyproject.toml` and run `uv lock`.
