<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Legal

> [!CAUTION]
> This document is not a legal advice. Consult a professional for legal questions.

This document outlines the legal aspects of `opentemplate`.

## Compliance and fixes

### REUSE compliance

Repositories created from this template follow [REUSE](https://reuse.software/) framework,
meaning:

- Every file includes an [SPDX](https://spdx.dev/use/specifications/)
    header with `license` and copyright details.
- Headers are either language-specific comments or `<filename>.license`
    files when comments aren't supported.

> [!IMPORTANT]
> Each contributor will be added to the SPDX headers.
> See [`SPDX-FileContributor`](https://spdx.github.io/spdx-spec/v2.2.2/file-information/#8.14)
> for more details.

- The `prek` hook automatically adds missing headers (`fix-legal` in `pyproject.toml`).
- `check-legal` in `pyproject.toml` ensures compliance and runs after `fix-legal`.

### License compliance

Licenses of dependencies are checked in CI against a single list of allowed
[SPDX identifiers](https://spdx.org/licenses/) (`license.notice` in `.trivy.yaml`):

> MIT, MIT-0, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC,
> PSF-2.0, Python-2.0, 0BSD, Unlicense, Zlib, OFL-1.1

<!-- pyml disable-num-lines 7 line-length-->

| Dependencies                                        | Tool                       | Checked on                                         |
| --------------------------------------------------- | -------------------------- | -------------------------------------------------- |
| Python `core` and `extras` (distributed)            | Trivy                      | pull requests changing them, weekly, every release |
| GitHub Actions, `requirements.txt`, `uv.lock` files | `dependency-review-action` | every pull request, weekly                         |
| Python development groups                           | `dependency-review-action` | every pull request (`uv.lock`), weekly             |

Both tools fail on a license outside of the list.

> [!IMPORTANT]
> Neither runs locally, so the first feedback is on CI!

#### Python dependencies

[Trivy](https://github.com/aquasecurity/trivy) checks the licenses of
the package environments (`core` and `extras`), installed per Python version
and OS
(`.github/workflows/_sbom.yml`, configured in `.trivy.yaml` and `.trivyignore.yaml`).
It evaluates SPDX expressions (e.g. `MIT OR GPL-3.0-only` passes,
`MIT AND GPL-3.0-only` does not).

The check runs on pull requests changing the dependencies (or the Trivy
configuration), weekly against `main` and the latest release, and before every
release
(`/tool:trivy/scope:licenses-<name>/language:python`, weekly and releases).

> [!NOTE]
> Like tests, the check runs only when dependencies change, therefore it is not
> required for merging. Releases are not published with a failing check.

> [!WARNING]
> Development dependency groups are not checked, as they are not distributed.

#### GitHub Actions and other dependencies

`legal-dependencies.yml` runs
[`dependency-review-action`](https://github.com/actions/dependency-review-action)
on pull requests (and merge queues). It compares the
[dependency graph](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph)
of the base and head commits and fails if an __added or changed__ dependency
has a license outside of the list (`allow-licenses` in `.trivy.yaml`
refers to `license.notice`).

It covers ecosystems which Trivy cannot see, most notably third-party
GitHub Actions and reusable workflows used in workflows (and composite actions)
and the hash-locked `requirements.txt` files (`.github/`, `template-setup/`).
It compares `uv.lock` as well (overlapping Trivy). Development dependencies
(dependency groups) would be ignored (`fail-on-scopes`), but the dependency
graph reports every `uv.lock` package of a non-virtual project as `runtime`,
so development dependencies with other licenses are listed in
`allow-dependencies-licenses` (e.g. `pkg:pypi/hypothesis`, MPL-2.0).

`legal-dependencies-update.yml` runs the same check weekly between
the first commit and the latest release, and between the latest release
and `main` (between the first commit and `main` before the first release).

> [!WARNING]
> Dependencies of the first commit (the `opentemplate` snapshot, checked
> by `opentemplate`) are not compared, check them manually
> after narrowing the allowed licenses.

> [!WARNING]
> Dependencies without any license information are not reported by either
> tool (`dependency-review-action` only lists them in the job summary),
> review such new dependencies manually.

> [!IMPORTANT]
> The dependency graph has to be enabled
> (default for public repositories, private ones require
> [GitHub Code Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)).

## Adjustments

### Changing license

- Run `uv run reuse download <LICENSE-SPDX>`
    __and copy it over the [`/LICENSE`](../../LICENSE.md) file__
    (`prek` checks both files are identical).
- Change the package license metadata to the new SPDX identifier.
    If no dedicated `/project` source exists for it, this is one of the
    remaining direct `[project]` edits in `pyproject.toml`.

### Modifying license compliance

> [!IMPORTANT]
> Adjust project licensing as needed.

To update allowed licenses, modify `license.notice` in `.trivy.yaml`
(exact SPDX identifiers, __also used by `dependency-review-action`__).

Exceptions for single dependencies:

- Python: `licenses` in `.trivyignore.yaml`, identified by the license and
    the path of the package metadata as a glob (matching every Python version
    and OS), e.g. `**/<package>-*.dist-info/METADATA`, optionally until
    `expired_at` (prefer allowing the license if acceptable)
- GitHub Actions, `requirements.txt` and `uv.lock`: `allow-dependencies-licenses`
    in `.trivy.yaml` as [package URLs](https://github.com/package-url/purl-spec),
    e.g. `pkg:githubactions/<owner>/<repo>`

> [!NOTE]
> Both files are attested and attached to every release, so the allowed
> licenses and exceptions behind the released scans can be audited.

## Documents

- __[`/LICENSE`](../../LICENSE.md)__ (Apache-2.0 by default)
    should be a copy (not a symbolic link, which GitHub cannot detect)
    of the actual license file in `LICENSES/`.
- __`LICENSES/`__ folder contains all project licenses
    (e.g., `uv.lock` is [`CC0-1.0`](https://creativecommons.org/publicdomain/zero/1.0/deed.en)).
- __[`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md)__ follows the
    [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
- __[`DCO.md`](../../DCO.md)__ (Developer Certificate of Origin) must remain unchanged;
    all commits must be signed off ([details](https://wiki.linuxfoundation.org/dco)).
- __[`GOVERNANCE.md`](../../GOVERNANCE.md)__ outlines project governance.
- __`CITATION.cff`__ provides citation details

> [!TIP]
> See [GitHub guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)
> for more information.

## Code Sources

- `pyproject.toml`
- `.github/workflows/*legal*.yml`
- `.github/workflows/_sbom.yml`
- `.trivy.yaml`
- `.trivyignore.yaml`
