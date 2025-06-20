<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Security self-assessment of opentemplate

Source: https://tag-security.cncf.io/community/assessments/guide/self-assessment/

## Table of Contents

- [Metadata](#metadata)
    - [Security links](#security-links)
- [Overview](#overview)
    - [Actors](#actors)
    - [Actions](#actions)
    - [Background](#background)
    - [Goals](#goals)
    - [Non-goals](#non-goals)
- [Self-assessment use](#self-assessment-use)
- [Security functions and features](#security-functions-and-features)
- [Project compliance](#project-compliance)
- [Secure development practices](#secure-development-practices)
    - [Deployment pipeline](#deployment-pipeline)
    - [Communication channels](#communication-channels)
    - [Ecosystem](#ecosystem)
- [Security issue resolution](#security-issue-resolution)
    - [Responsible disclosure practice](#responsible-disclosure-practice)
    - [Incident response](#incident-response)
- [Appendix](#appendix)

## Metadata

<!-- pyml disable-num-lines 21 line-length-->

| Category          | Resource                                                                                                   |
| ----------------- | ---------------------------------------------------------------------------------------------------------- |
| Assessment Stage  | Complete                                                                                                   |
| Creator           | open-nudge                                                                                                 |
| Software          | [https://github.com/open-nudge/opentemplate](https://github.com/open-nudge/opentemplate)                   |
| Website           | [https://open-nudge.github.io/opentemplate](https://open-nudge.github.io/opentemplate)                     |
| Security Provider | Yes                                                                                                        |
| Languages         | Python                                                                                                     |
| SBOM              | [https://github.com/open-nudge/opentemplate/releases](https://github.com/open-nudge/opentemplate/releases) |

### Security links

| Category          | Resource                                                                                                                                                 |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Security File     | [https://github.com/open-nudge/opentemplate/blob/main/SECURITY.md](https://github.com/open-nudge/opentemplate/blob/main/SECURITY.md)                     |
| Security Insights | [https://github.com/open-nudge/opentemplate/blob/main/SECURITY-INSIGHTS.yml](https://github.com/open-nudge/opentemplate/blob/main/SECURITY-INSIGHTS.yml) |
| Dependencies      | [https://github.com/open-nudge/opentemplate/blob/main/pyproject.toml](https://github.com/open-nudge/opentemplate/blob/main/pyproject.toml)               |
| Release Artifacts | [https://github.com/open-nudge/opentemplate/releases](https://github.com/open-nudge/opentemplate/releases)                                               |

## Overview

All-in-one Python template. One click. Everything included.

### Background

This project provides a base for Python projects, which provides
developer workflows, security posture and best practices.

### Actors

- [opennudge](https://opennudge.com) - organization providing core
    security features

### Actions

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

### Goals

Provide high quality secure project template free of charge.

### Non-goals

Full automation of security for any type of Python projects
(e.g. web projects using cloud services).

## Self-assessment use

This self-assessment was automatically generated by the
[opentemplate](https://github.com/open-nudge/opentemplate) [](templateskip)
template to provide basic security information about the project.
__It should be extended by adding project-specific security information.__

> [!IMPORTANT]
> [opennudge](https://opennudge.com)
> does not intend to provide a security audit of the project
> or function as an independent assessment or attestation
> of its security posture.

## Security functions and features

<!-- pyml disable-num-lines 5 line-length-->

| Component | Applicability | Description of Importance                                                                                                                                                                                                                                  |
| --------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| template  | Critical      | Base GitHub template of the repository provided by `opennudge`. Used to provide initial security posture (pipelines, pre-commit, practices, hardening etc.) See [open-nudge/opentemplate](https://github.com/open-nudge/opentemplate) for more information |

## Project compliance

Project tries to comply with the following security standards:

- [SLSA](https://slsa.dev/) - L3+ if the project is public or coming
    from a GitHub Enterprise Account with Advanced Security, L2 otherwise
- The project is currently not third-party audited or verified

## Secure development practices

### Deployment pipeline

Core of the deployment pipeline is based on the following tools:

- [opentemplate](https://github.com/open-nudge/opentemplate) [](templateskip):
    see [](templateskip) [open-nudge/opentemplate](https://github.com/open-nudge/opentemplate)
    for more information

### Communication channels

You can reach out to us by
[Private Security Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
or by:

- means of communication provided at the account level [here](https://github.com/open-nudge)
- opening an issue in the repository (somebody will get back to you)

### Ecosystem

This project is a part of the Python ecosystem.

## Security issue resolution

The [`open-nudge/opentemplate`](https://github.com/open-nudge/opentemplate)
security policy is maintained in the
[`SECURITY.md`](https://github.com/open-nudge/opentemplate/blob/master/SECURITY.md)
file.

### Responsible disclosure practice

The [`open-nudge/opentemplate`](https://github.com/open-nudge/opentemplate)
accepts vulnerability reports as outlined in the security policy defined in
[`SECURITY.md`](https://github.com/open-nudge/opentemplate/blob/master/SECURITY.md#reporting-a-vulnerability.)
file.

### Incident response

Project maintainers will respond to security incidents privately
on a case-by-case basis.

## Appendix

- Project is largely aligned with the
    [Open Source Security Foundation best practices](https://www.bestpractices.dev/en)
- Some false negatives regarding the best practices were spotted
    (e.g. not using fuzzing), consult `scorecard.yml` for more information
