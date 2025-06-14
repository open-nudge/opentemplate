<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Security

Report any security vulnerabilities you find according to these
guidelines.

## General

- Please adhere to [Code of Conduct](./CODE_OF_CONDUCT.md) at all times.

## Reporting a vulnerability

- If you discover a vulnerability, report it directly to the code
    maintainers, __preferably using GitHub's
    [Private Vulnerability Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability)__.
- If you cannot find a way to report it, or have received no
    response after repeated attempts,
    __[contact the creators directly](https://github.com/open-nudge).__

Thank you.

## Security measures

This project strives to implement
[Open Source Security Foundation](https://openssf.org/)
(OSSF) [Best Practices](https://www.bestpractices.dev/en).

Some of the security measures undertaken in this project include:

- [OSSF Scorecard](https://github.com/ossf/scorecard)
- [Security file](./SECURITY.md)
- [Security Insights Specification](https://github.com/open-nudge/opentemplate/blob/main/SECURITY-INSIGHTS.yml)
    as defined [here](https://github.com/ossf/security-insights-spec)
- [Security Self Assessment](SECURITY-SELF-ASSESSMENT.md)
- [Security Dependencies Policy](SECURITY-DEPENDENCY.md)
- [Renovate Bot](https://github.com/open-nudge/opentemplate/blob/main/.github/renovate.json)
    for automated dependency updates
- [Software Bills Of Material (SBOMs)](https://github.com/open-nudge/opentemplate/releases)
- [Sigstore signing](https://github.com/open-nudge/opentemplate/releases)
    as seen [here](https://github.com/sigstore/sigstore-python)
- GitHub Actions CI/CD pipelines with minimal permissions
- GitHub Actions CI/CD pipelines hardened via [Harden Runner](https://github.com/step-security/harden-runner)
- [Pre-commit hooks](https://pre-commit.com/) for local code quality
    and security verification
