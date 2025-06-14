<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Release process

To release a new version, [create a GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).
This triggers all necessary pipelines.

> [!NOTE]
> Specify a new tag version and (optionally) release title.
> Changelog will be automatically updated by the pipelines.

> [!CAUTION]
> You must create GitHub release manually. Merging to `main` __does not__
> trigger package or documentation releases.

## Versioning

This project uses a __double versioning__ scheme based on [Semantic Versioning](https://semver.org/):

- __Public version__ – The official release version (e.g., `1.2.0`).
- __Python version__ – Automatically generated from commits
    and independent of the public version.

### Rationale

Public versions are there to signify the release to the audience
(mainly for marketing purposes), while the Python
version ensures semantic consistency (needed by package users).
This approach also enhances security by preventing automated
`tag` pushes to `main` (no `bot` automerges).

### Public version

Public releases follow [Semantic Versioning](https://semver.org/) and trigger:

- Package release to `PyPI` (__for public repositories__, versioned by Python version).
- Documentation updates.
- Artifact generation (e.g., [Software Bill of Materials](https://www.cisa.gov/sbom)).

### Python version

Managed automatically based on commit messages:

- `fix` → Patch version update
- `feat` → Minor version update
- `BREAKING` (or `feat!`/`fix!`) → Major version update

<!-- md-dead-link-check: off -->

> [!TIP]
> Check out [commition](https://github.com/open-nudge/commition)
> for details about Python version calculations.

<!-- md-dead-link-check: on -->

## Artifacts

Releases include the following artifacts:

- __Python package__ ([packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/))

- `CHANGELOG.md` (full changelog)

- `LICENSE.md` (project license)

- Documentation (uploaded to `gh-pages`)

- [OSV-Scanner SARIF](https://google.github.io/osv-scanner/output/#sarif)

- __Software Bills of Materials (SBOMs)__ ([CISA guide](https://www.cisa.gov/sbom)):

    1. Python package (via [CycloneDX](https://github.com/CycloneDX/cyclonedx-python))

    1. Python dependencies (via [CycloneDX](https://github.com/CycloneDX/cyclonedx-python))

    1. GitHub SBOM ([docs](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/exporting-a-software-bill-of-materials-for-your-repository))

    1. REUSE SBOM ([docs](https://reuse.readthedocs.io/en/stable/man/reuse-spdx.html))

- SBOM attestations ([actions/attest-sbom](https://github.com/actions/attest-sbom))

- __Python package attestations__ ([PyPI guide](https://blog.pypi.org/posts/2024-11-14-pypi-now-supports-digital-attestations/))

- __SLSA Build Provenance__ ([SLSA spec](https://slsa.dev/spec/v1.0/provenance))

> [!IMPORTANT]
> Some artifacts depend on repository visibility, the more public the repository,
> the more artifacts are produced.

> [!NOTE]
> Attestations of Python package SBOMs use hashes of `RECORD` files as inputs, see
> [here](https://packaging.python.org/en/latest/specifications/recording-installed-packages/#the-record-file)
> for more information about them.

## Repository visibility and compliance

<!-- pyml disable-num-lines 7 line-length-->

| Visibility     | Artifacts produced                  | Compliance level                                  |
| -------------- | ----------------------------------- | ------------------------------------------------- |
| __Public__     | All artifacts                       | [SLSA Level 3](https://slsa.dev/spec/v1.0/levels) |
| __Enterprise__ | No provenance, private attestations | [SLSA Level 3](https://slsa.dev/spec/v1.0/levels) |
| __Private__    | No attestations, limited artifacts  | [SLSA Level 2](https://slsa.dev/spec/v1.0/levels) |

## Changelog

Generated via [git-cliff](https://github.com/orhun/git-cliff)
(configured in `pyproject.toml`) and:

- The latest version's changelog becomes the release description.
- Full `CHANGELOG.md` attached to the release
- `CHANGELOG.md` inside the repository links to GitHub releases

The changelog includes:

- Public version, date, and comparison link
- Commit statistics (e.g., how many commits done by human vs bots,
    types of commit like security, tests, legal etc.)
- Python changes (Breaking, Features, Fixes, Bots)
- Other changes (same structure as Python changes)
- Each commit includes message, author, and metadata (if available)

> [!TIP]
> Read more about changelogs in the [FAQ](../about/faq.md)

## Customization

This process can be adjusted by editing:

- `.github/workflows/release.yml`

- `pyproject.toml`:

    1. `[tool.git-cliff]` – Changelog settings

    1. `[dependency-groups]` → `dev-security` – changing SBOM dependencies

> [!IMPORTANT]
> Due to pipeline complexity, fine-tuning is more challenging,
> consult the source files if necessary.

## Code sources

- `pyproject.toml`
- `.github/workflows/release.yml`
- `.github/workflows/release-upload.yml`
- `.github/workflows/release-sarifs-reusable.yml`
- `.github/workflows/release-sbom-attest-reusable.yml`
- `.github/workflows/release-sbom-run-reusable.yml`
- `.github/workflows/release-sboms-reusable.yml`
- `.github/workflows/release-slsa-provenance-reusable.yml`
