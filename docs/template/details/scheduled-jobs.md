<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Scheduled jobs

`opentemplate` runs scheduled jobs weekly, typically on weekends.

> [!TIP]
> All cron-like jobs are in `/.github/workflows` and use the
> `on: schedule` trigger.

## Jobs

Most scheduled jobs focus on security (`security-_` workflows)
and are run periodically as vulnerabilities evolve, namely:

- __Security posture analysis:__ [`ossf/scorecard`](https://github.com/ossf/scorecard)
- __Vulnerability scanning:__ [`uv audit`](https://docs.astral.sh/uv/)
    and [Trivy](https://github.com/aquasecurity/trivy) (Python SBOMs)
- __License compliance:__ Trivy (all distributed Python dependencies) and
    [`dependency-review-action`](https://github.com/actions/dependency-review-action)
    (GitHub Actions, `requirements.txt` added since the first commit)
- __Bug detection and code quality:__ [`semgrep/semgrep`](https://github.com/semgrep/semgrep)
- __Malicious dependencies detection:__ [`DataDog/guarddog`](https://github.com/DataDog/guarddog)
- __GitHub Actions analysis:__ [CodeQL](https://codeql.github.com/)
    and [`zizmor`](https://github.com/zizmorcore/zizmor)

> [!NOTE]
> These also run after every merge to `main`, so the GitHub Security tab
> (and the baseline pull request alerts are compared against) stays current.
> SBOM scans (`security-sbom-python-update.yml`) and
> `legal-dependencies-update.yml` run on schedule only.

Weekly `uv audit`, `semgrep`, `guarddog`, CodeQL and `zizmor` scans
run from a single workflow (`security-sarifs-update.yml`), against both
`main` and the latest release (the code users install), as `main` may
contain unreleased commits. The same applies to Python SBOM scans
(`security-sbom-python-update.yml`), while `legal-dependencies-update.yml`
checks dependencies added between the first commit and the latest release,
and those changed between the latest release and `main` (the first commit
before the first release), as the dependency graph only compares two commits.
Dependencies of the first commit come from `opentemplate`, which checks them
continuously.

## Cache

Dependency caches are rebuilt after every merge to `main` and weekly,
so they are not evicted by GitHub (unused for 7 days).

## prek (previously pre-commit)

Independent `prek` hooks update weekly. All hooks run against the
latest `main` branch state to ensure updates are correct.

## Content generation

[`cog`](https://github.com/nedbat/cog) automates content generation based on
source code comments (`DO NOT EDIT UNTIL end marker` in `pyproject.toml`).

Additionally, [`open-nudge/cogeol`](https://github.com/open-nudge/cogeol)
integrates [Python's end-of-life](https://endoflife.date/) data to simplify management.

Together with GitHub Actions, these ensure:

- Support for the latest three Python versions.
- CI/CD always runs appropriate versions.
- PRs are opened for new releases and scheduled deprecations.

## Template updates

> [!NOTE]
> Template updates are not __currently__ automated; the workflow is a
> placeholder for future use.

## Code sources

- `.github/workflows/*prek*.yml`
- `.github/workflows/*security-uv-audit*.yml`
- `.github/workflows/*security-semgrep*.yml`
- `.github/workflows/*security-guarddog*.yml`
- `.github/workflows/*security-codeql*.yml`
- `.github/workflows/*security-zizmor*.yml`
- `.github/workflows/*security-sarifs*.yml`
- `.github/workflows/security-sbom-python-update.yml`
- `.github/workflows/legal-dependencies-update.yml`
- `.github/workflows/security-scorecard-update.yml`
- `.github/workflows/cache.yml`
- `.github/workflows/*generation*.yml`
