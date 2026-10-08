<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
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
    as defined in the [Security Insights specification](https://github.com/ossf/security-insights-spec)
- [Security Self Assessment](SECURITY-SELF-ASSESSMENT.md)
- [Security Dependencies Policy](SECURITY-DEPENDENCY.md)
- [Software Bills Of Material (SBOMs)](https://github.com/open-nudge/opentemplate/releases)
    scanned by [Grype](https://github.com/anchore/grype)
- [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
    (Sigstore-backed) of distributions, SBOMs and SARIF files, each verified
    against its producing workflow before being attached to the
    [release](https://github.com/open-nudge/opentemplate/releases)
- Static analysis and vulnerability scanning in CI, before every release
    and weekly, with results uploaded to the GitHub Security tab:
    - [CodeQL](https://codeql.github.com/) (GitHub Actions workflows)
    - [zizmor](https://github.com/zizmorcore/zizmor) (GitHub Actions workflows)
    - [Semgrep](https://github.com/semgrep/semgrep)
    - [OSV-Scanner](https://github.com/google/osv-scanner) (dependencies)
    - [GuardDog](https://github.com/DataDog/guarddog)
        (malicious runtime dependencies and actions)
- Protected `main` branch (rulesets) with required status checks
- GitHub Actions CI/CD pipelines with minimal permissions
    (write permissions only in dedicated upload and attestation jobs)
- GitHub Actions CI/CD pipelines hardened via [Harden Runner](https://github.com/step-security/harden-runner)
- [Prek hooks](https://prek.j178.dev/) for local code quality
    and security verification
