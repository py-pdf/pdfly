# Releases

`pdfly` is published to [PyPI](https://pypi.org/project/pdfly/) via
[trusted publishing](https://docs.pypi.org/trusted-publishers/). No API tokens
are stored in GitHub. PyPI trusts the workflow `publish-to-pypi.yaml` running
in the `pypi` GitHub environment of `py-pdf/pdfly`.

Every change to `main` goes through a pull request, including releases. Never
push or force-push to `main` directly.

## Where the version lives

The version is defined in one place only: `version` in `pyproject.toml`.
`uv.lock` records it too and is updated by `uv version`. At runtime, `pdfly`
reads it from the installed package metadata, so users get it with any of:

```bash
pdfly --version
python -c "import pdfly; print(pdfly.__version__)"
pip show pdfly
```

The package is built with the `uv_build` backend; `uv build` and `uv publish`
are the front end.

## Normal path: via GitHub

1. On an up-to-date `main`, run `make prepare-release`. It
    * suggests the next version (patch bump) and asks you to confirm it,
    * sets it in `pyproject.toml` and `uv.lock` (via `uv version`),
    * adds a new section to `CHANGELOG.md` based on the commits since the last
      tag (it queries the GitHub API for author names), and
    * writes the commit message to `RELEASE_COMMIT_MSG.md` (git-ignored).
2. Review the diff. Then create a branch, commit and push it, as printed by
   the script.
3. Open a pull request:
    * Title: `REL: X.Y.Z`
    * Description: the body of `RELEASE_COMMIT_MSG.md` (everything after the
      first line)
4. Squash-merge the PR. Make sure the squash commit message is the PR title
   and the PR description, because it becomes the tag message and the text of
   the GitHub release. A regular merge commit does not start with `REL: ` and
   would not trigger anything.
5. GitHub Actions does the rest:

    | Workflow                     | Trigger                              | Result                                                    |
    | ---------------------------- | ------------------------------------ | --------------------------------------------------------- |
    | `release.yaml`               | push to `main` of a `REL: ` commit   | creates the git tag `X.Y.Z` with the commit body as message |
    | `create-github-release.yaml` | `release.yaml` finished              | creates the GitHub release page from the tag message      |
    | `publish-to-pypi.yaml`       | `release.yaml` finished              | builds sdist and wheel, uploads them to PyPI              |

6. Check <https://pypi.org/project/pdfly/#history> and the
   [GitHub releases](https://github.com/py-pdf/pdfly/releases).

Tags created with the `GITHUB_TOKEN` do not trigger `push` events. That is why
the two downstream workflows listen to the `workflow_run` event of
`release.yaml`. If a step failed, `publish-to-pypi.yaml` and
`create-github-release.yaml` can be started manually (`workflow_dispatch`).

## Fallback: GitHub is not working

Use this only if GitHub Actions or GitHub itself is unavailable and the release
cannot wait. You publish to PyPI from your machine, and `main` is updated via
the usual PR once GitHub is back.

1. Run `make prepare-release` on an up-to-date `main`, then create the
   release branch and commit, as printed by the script. Do not tag anything.
2. Create a PyPI API token (scope: project `pdfly`) at
   <https://pypi.org/manage/account/token/> and export it:

    ```bash
    export UV_PUBLISH_TOKEN=pypi-...
    ```

    Trusted publishing only works in CI, so a token is needed here. Revoke the
    token afterwards.

3. Run `make release`. It asks for confirmation, checks that the working tree
   is clean and that `HEAD` is the `REL: X.Y.Z` commit for the version in
   `pyproject.toml`, and then runs `uv build` and `uv publish`.
4. Once GitHub is back, push the release branch and continue with steps 3 and
   4 of the normal path (PR and squash-merge). Do not merge anything else into
   `main` before it, so that `main` matches what was published.
    * `release.yaml` creates the tag and `create-github-release.yaml` the
      release page, as usual.
    * `publish-to-pypi.yaml` fails, because PyPI rejects files that were
      already uploaded. That is expected.

Without `uv`, `python -m build` followed by `twine upload dist/*` does the
same.
