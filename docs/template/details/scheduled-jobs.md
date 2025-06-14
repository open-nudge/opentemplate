<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
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
- __Vulnerability scanning:__ [`google/osv-scanner`](https://github.com/google/osv-scanner)
- __Bug detection and code quality:__ [`semgrep/semgrep`](https://github.com/semgrep/semgrep)

## Dependency automation

Automating dependency updates ensures security and stability.

### Renovate

> [!IMPORTANT]
> Only relevant workflows run when `renovate` opens a PR
> (e.g., `markdown` checks for `dev-markdown` updates).

- Updates run on weekends.
- Dependencies are grouped by `dev-<type>`.
- Updates are handled by `github-actions[bot]`.

#### Adjustments

> [!CAUTION]
> If adding a `dev` dependency in `pyproject.toml`,
> update `.github/renovate.json` accordingly.

New `dev-<type>` groups require:

- A corresponding entry in `renovate.json`.
- (Probably) a new `.github/workflows/renovate-<type>.yml` workflow.

> [!NOTE]
> `.github/workflows/<type>-renovate.yml` should run only when the
> branch name matches `dependencies-dev-<type>`.

> [!TIP]
> See the [GitHub Actions section](github-actions.md) for more details.

### pre-commit

Independent `pre-commit` hooks update weekly. All hooks run against the
latest `main` branch state to ensure updates are correct.

> [!NOTE]
> `renovate` does not update `pre-commit` hooks due to maintainers'
> policy ([details](https://docs.renovatebot.com/modules/manager/pre-commit/#additional-information)).

## Content generation

[`cog`](https://github.com/nedbat/cog) automates content generation based on
source code comments (`DO NOT EDIT UNTIL end marker` in `pyproject.toml`).

Additionally, [`opennudge/cogeol`](https://github.com/nedbat/cog)
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

- `.github/renovate.json`
- `.github/workflows/pre-commit-update*.yml`
- `.github/workflows/security-osv-scanner-update*.yml`
- `.github/workflows/security-semgrep*.yml`
- `.github/workflows/*-renovate.yml`
- `.github/workflows/generation*.yml`
