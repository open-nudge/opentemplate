<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Installation

## Prerequisites

Before starting, install the following on your local machine:

1. [Python](https://www.python.org/downloads/) (latest version recommended).
1. [`pdm`](https://pdm-project.org/en/latest/#recommended-installation-method)
    package manager.

> [!NOTE]
> Learn more about `pdm` in the [pdm documentation](https://pdm-project.org/en/latest/)

## Setup

1. Create a new GitHub repository using this template (`Use this template` button).
1. Name your repo (__use underscores `_` instead of hyphens `-`__).
1. Add a project description (__required!__).
1. __Wait for the setup commit__ (done by `github-actions[bot]`, may take a few minutes).

Once complete, clone the repository and run `pdm setup`
to install dependencies and set up the project.

## Effects

The following features (and more) will be enabled:

- Ready-to-use state of the art project structure
- Set of `20+` labels (see [here](https://github.com/open-nudge/opentemplate/labels)),
    many of which are automatically applied to pull requests
- Predefined templates for issues, pull requests and discussions
- Initial dependency-specific caching enabled in GitHub Actions

## Hardening

After the setup, an issue will be created (named `Update repository settings`)
outlining security hardening steps.

> [!CAUTION]
> Following these steps is __strongly recommended__ for better security.

### Hardening steps

> [!TIP]
> These steps will be further detailed in the aforementioned issue.

- Enable third-party bots (if applicable).
- Create a short-lived, minimally scoped `TEMPLATE_GITHUB_TOKEN`.
- Run the hardening workflow.
- Set up [trusted PyPI publishing](https://docs.pypi.org/trusted-publishers/).

> [!NOTE]
> Full automation is not currently possible due to platform limitations.

### Benefits

- Improved security following
    [Open Source Security Foundation's Scorecard best practices](https://securityscorecards.dev/#the-checks).
- Enabled GitHub Pages for documentation hosting.
- Applied [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
    (including [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)).
- Configured pull request defaults and other repository settings.
- Activated GitHub security features (e.g., [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)).

> [!WARNING]
> Exact features depend on repository type,
> but in general: `public` > `enterprise` > `private`.

## Updates

> [!CAUTION]
> This feature is not yet implemented.

Your repository will be automatically updated with the latest `opentemplate`
version every weekend.

## Code sources

- `/.github/workflows/template_setup.yml`
- `/.github/workflows/template_update.yml`
- `/.github/workflows/harden.yml`
- `/.github/rulesets`
