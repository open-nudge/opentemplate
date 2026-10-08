<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Release process

To release a new version, either:

- __UI__: go to `Actions` → `Release Tag` → `Run workflow` (on `main`)
    and enter the `major`, `minor` and `patch` numbers
    (`vX.Y.Z` must be greater than the latest released one)
    and, optionally, a `message` (release notes).
    This tags the latest `main` commit as `vX.Y.Z`.

- __CLI__: push a signed tag of a `main` commit,
    its message being the release notes:

    ```sh
    git tag --sign vX.Y.Z --message "<release notes>"
    git push origin vX.Y.Z
    ```

    Repeat `--message` for more paragraphs, use `--file <notes.md>`
    or omit both to write the notes in your editor.

> [!IMPORTANT]
> Rulesets reject tags not shaped like `vX.Y.Z`.

Both trigger all necessary pipelines, which create a draft
[GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
with all assets and publish it as the last step.

> [!NOTE]
> Changelog (release description) will be automatically created by the pipelines.
> The tag message (if any) is placed above it.

> [!CAUTION]
> Do not create GitHub releases via `Releases` → `Draft a new release`.
> Drafts trigger no workflows, therefore the release will be incomplete.

> [!WARNING]
> Merging to `main` __does not__ trigger package or documentation releases.

## Versioning

This project uses a __double versioning__ scheme based on [Semantic Versioning](https://semver.org/):

- __Public version__ – The official release version (e.g., `v1.2.0`).
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

Releases include only attested artifacts:

- __Python package__ ([packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/))

- [OSV-Scanner](https://google.github.io/osv-scanner/output/#sarif),
    [Semgrep](https://semgrep.dev/docs/cli-reference),
    [zizmor](https://github.com/zizmorcore/zizmor),
    [GuardDog](https://github.com/DataDog/guarddog) (core, extras and actions)
    and [CodeQL](https://codeql.github.com/) SARIFs, named
    `security-<tool>-<commit SHA>.sarif`
    (CodeQL not available [without GitHub Code Security](../details/security.md#without-github-code-security))

- __Software Bills of Materials (SBOMs)__ ([CISA guide](https://www.cisa.gov/sbom))
    and their [Grype](https://github.com/anchore/grype) scans (SARIF):

    1. Python package with its `core`, `extras` and `dev` dependencies
        per Python version and per OS
        (via [CycloneDX](https://github.com/CycloneDX/cyclonedx-python))

    1. GitHub Actions of the project and of the reusable workflows
        (extracted from `uses:` references, see `sbom-actions` in `pyproject.toml`)

    1. REUSE SBOM ([docs](https://reuse.readthedocs.io/en/stable/man/reuse-spdx.html))

- __Python package attestations__ ([PyPI guide](https://blog.pypi.org/posts/2024-11-14-pypi-now-supports-digital-attestations/))

- `<asset>.sigstore.jsonl` for every asset above: attestation bundles
    ([actions/attest](https://github.com/actions/attest)) for offline verification

## Attestations

> [!IMPORTANT]
> Public/internal repositories created from `open-nudge/opentemplate`
> (and private ones on GitHub Enterprise Cloud) satisfy SLSA L3 Build.

> [!WARNING]
> Private repositories without GitHub Enterprise Cloud
> (`NO_GITHUB_ENTERPRISE_CLOUD` variable set) do not have any SLSA
> attestations, therefore are L0.

Every signed release asset is produced by an `open-nudge/opentemplate`
reusable workflow and __attested within the same workflow__ by a separate job.
Before attaching to the release each artifact is verified against the
attestation of __its__ producing workflow:

<!-- pyml disable-num-lines 7 line-length-->

| Asset                                                 | Signer workflow               |
| ----------------------------------------------------- | ----------------------------- |
| Wheel and source distribution                         | `release-build-reusable.yml`  |
| SBOMs and their Grype SARIFs                          | `sbom-reusable.yml`           |
| OSV-Scanner, Semgrep, zizmor, GuardDog, CodeQL SARIFs | `release-sarifs-reusable.yml` |

> [!NOTE]
> Release notes (changelog) and documentation are not attested (their build
> runs project __not open-nudge/opentemplate__ code), therefore not attached.

The release fails __if it contains any unexpected asset__.

> [!IMPORTANT]
> The package is uploaded to PyPI only when all previous steps succeed,
> and the release is published only afterwards, otherwise it stays a draft.
> Published releases are
> [immutable](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
> (enabled by `harden.yml`): their assets and tag cannot be changed.

The distributions carry
[SLSA Build Provenance](https://slsa.dev/spec/v1.0/provenance)
([SLSA Build L3](https://slsa.dev/spec/v1.0/levels#build-l3)
for attested releases, see [below](#attestations)).

> [!WARNING]
> You need to run `harden.yml` before releasing, otherwise it will fail!

> [!NOTE]
> `open-nudge/opentemplate` is SLSA L2 itself as it relies on its own build.

> [!WARNING]
> Only commits of the default branch (merged via reviewed pull requests)
> are built. Follow default release approach of `open-nudge/opentemplate`

> [!WARNING]
> Private repositories without GitHub Enterprise Cloud must opt out by
> setting the `NO_GITHUB_ENTERPRISE_CLOUD` configuration variable to any
> value, e.g. `true` (at the
> [organization or repository level](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables#defining-configuration-variables-for-multiple-workflows)),
> otherwise their release fails. No attestations are created and attached then.
> __This escape hatch is ignored for public and internal repositories!__

## Verifications

To verify an artifact run the following:

```sh
gh attestation verify <asset> \
  --bundle <asset>.sigstore.jsonl \
  --repo <owner>/<repo> \
  --signer-workflow open-nudge/opentemplate/.github/workflows/<signer> \
  --signer-digest <sha> \
  --source-ref refs/tags/<tag> \
  --deny-self-hosted-runners
```

where `<signer>` comes from the table in previous section and
`<sha>` is the template commit the project pins (`@<sha>` in its `.github/workflows`).

> [!NOTE]
> Drop `--bundle` to fetch the attestations from GitHub instead.

The same command verifies files downloaded from PyPI (the provenance is bound
to the digest). PyPI itself only shows its publish attestations, signed by the
project's `release.yml`, as trusted publishing does not support reusable
workflows ([pypi/warehouse#11096](https://github.com/pypi/warehouse/issues/11096)).

Ensure the commit belongs to the template (and not to a fork of it),
the command below should output `ahead` or `identical`:

```sh
gh api repos/open-nudge/opentemplate/compare/<sha>...main --jq .status
```

Every SBOM is additionally attested __against the wheel and source
distribution__ (subject: distribution digest, predicate: the SBOM),
__only after their provenance is verified__.

While the attestation of the SBOM file proves where the file came from,
this one binds its content to the artifact you actually have:
starting from the wheel's digest, verifiers (or policy engines) can verify:

- its SBOMs without relying on file names
- that the wheel was installed in the environment the SBOM describes.

The bundles of the distributions include these attestations.

> [!WARNING]
> SBOMs are created in an environment where dependencies' code may run
> (e.g. source distribution builds), therefore their __content__ is only as
> trustworthy as the dependencies. The attestation proves which workflow
> produced them, not that their content is correct.

Verify them with
`--signer-workflow` pointing to `sbom-reusable.yml` and
`--predicate-type https://cyclonedx.org/bom`
(or `https://spdx.dev/Document/v2.2` for the REUSE SBOM).

## Changelog

Generated via [git-cliff](https://github.com/orhun/git-cliff)
(configured in `pyproject.toml`) and:

- The latest version's changelog becomes the release description.
- `CHANGELOG.md` inside the repository links to GitHub releases

The changelog includes:

- Public version, date, and comparison link
- Commit statistics (e.g., how many commits done by human compared to bots,
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

    1. `[dependency-groups]` → `dev-release` – changing SBOM dependencies

> [!IMPORTANT]
> Reusable workflows run from the template commit pinned in
> `.github/workflows` (`@<sha>`), editing their local copies has no effect.
> To change them, fork the template and point `uses:` to the fork
> (attestations are then signed by the fork's workflows).

## Code sources

- `pyproject.toml`
- `.github/workflows/release.yml`
- `.github/workflows/release-tag.yml`
- `.github/workflows/release-upload.yml`
- `.github/workflows/release-sarifs-reusable.yml`
- `.github/workflows/security-sarifs-reusable.yml`
- `.github/workflows/release-changelog-reusable.yml`
- `.github/workflows/release-docs-reusable.yml`
- `.github/workflows/release-build-reusable.yml`
- `.github/workflows/release-sboms-reusable.yml`
- `.github/workflows/sbom-reusable.yml`
- `.github/workflows/security-upload-reusable.yml`
- `.github/actions/attestation-verify/action.yml`
- `.github/actions/digests-verify/action.yml`
