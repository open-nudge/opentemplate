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
- __Vulnerability scanning:__ [`google/osv-scanner`](https://github.com/google/osv-scanner)
- __Bug detection and code quality:__ [`semgrep/semgrep`](https://github.com/semgrep/semgrep)

## pre-commit

Independent `prek` hooks update weekly. All hooks run against the
latest `main` branch state to ensure updates are correct.

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
- `.github/workflows/prek-update*.yml`
- `.github/workflows/security-osv-scanner-update*.yml`
- `.github/workflows/security-semgrep*.yml`
- `.github/workflows/generation*.yml`
