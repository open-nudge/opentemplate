<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Installation

## Prerequisites

Before starting, install the following on your local machine:

1. [Python](https://www.python.org/downloads/) (latest version recommended).
1. [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
    package manager.

> [!NOTE]
> Learn more about `uv` in the [uv documentation](https://docs.astral.sh/uv/)

## Setup

1. Create a new GitHub repository using this template (`Use this template` button).
1. Name your repo (__use underscores `_` instead of hyphens `-`__).
1. Add a project description (__required!__).
1. __Wait for the setup commit__ (done by `github-actions[bot]`, may take a few minutes).

Once complete, clone the repository and run `uv run poe setup`
to install dependencies and set up the project.

## Effects

The following features (and more) will be enabled:

- Ready-to-use state of the art project structure
- Set of `20+` labels (see the [OpenTemplate issue labels](https://github.com/open-nudge/opentemplate/labels)),
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
- Create a short-lived, repository-scoped fine-grained PAT and save it as
    `TEMPLATE_GITHUB_TOKEN`. Grant __Contents: read and write__, __Workflows: read
    and write__, __Administration: read and write__, and __Pages: read and write__.
- Prefer a repository secret. An organization-level secret exposes the token to
    more repositories; if you use one, restrict it to the target repository.
- Manually run the hardening workflow using its existing workflow dispatch.
- Set up [trusted PyPI publishing](https://docs.pypi.org/trusted-publishers/).
- For private repositories __without__ GitHub Enterprise Cloud,
    set the `NO_GITHUB_ENTERPRISE_CLOUD` configuration variable
    (repository or organization) to any value (e.g. `true`),
    as releases are attested by default
    (ignored for public and internal repositories).
- For private repositories __without__ GitHub Code Security
    (formerly part of GitHub Advanced Security),
    set the `NO_GITHUB_CODE_SECURITY` configuration variable
    (repository or organization) to any value (e.g. `true`),
    as CodeQL runs and findings are uploaded to the Security tab by default
    (switch ignored for public and internal repositories, see
    [security](../details/security.md#without-github-code-security)).

> [!WARNING]
> Any non-empty value disables the feature, including `false`.
> Delete the variable to enable it again.

> [!NOTE]
> Full automation is not currently possible due to platform limitations.

### Local hardening

> [!WARNING]
> If you ran the `harden` workflow feel free to skip it.

The executable scripts in [`.github/tools/harden`](../../../.github/tools/harden)
apply individual settings locally and are also called by `harden.yml`.

| File                                 | Purpose                                |
| ------------------------------------ | -------------------------------------- |
| `rulesets.sh`                        | Apply repository rulesets              |
| `pages.sh`                           | Enable Pages via Actions               |
| `pages-tags.sh`                      | Allow Pages deployments from tags      |
| `settings.sh`                        | Configure repository settings          |
| `security.sh`                        | Enable security features               |
| `codeql.sh`                          | Disable CodeQL default setup           |
| `discussions.sh`                     | Enable discussions                     |
| `immutable-releases.sh`              | Enable immutable releases              |
| `private-vulnerability-reporting.sh` | Enable private reports                 |
| `vulnerability-alerts.sh`            | Enable vulnerability alerts            |
| `pypi.sh`                            | Configure the PyPI release environment |

Install __Bash__, __GitHub CLI__ (`gh`), and __jq__, then authenticate with
`gh auth login` or `GH_TOKEN` using `Administration` `write` permission
(also `Pages` `write` for Pages operations).
Run scripts directly from the checkout root:

```bash
./.github/tools/harden/rulesets.sh 2 .github/rulesets
./.github/tools/harden/settings.sh
./.github/tools/harden/pages.sh
./.github/tools/harden/pages-tags.sh
```

GitHub CLI resolves the target from the current checkout; set `GH_REPO=owner/repo`
to override it.
Pass `0` approvals for solo projects, `1` for two contributors, or `2`
for larger teams (just like hosted `harden` workflow).

> [!NOTE]
> Local scripts apply only their selected settings and require the corresponding
> GitHub features to be available for the repository.

> [!NOTE]
> Scripts are idempotent, __existing rulesets will be deleted
> ONLY after new ones were created successfully.__

Configure PyPI approvers locally:

```bash
./.github/tools/harden/pypi.sh 'alice bob' 'release-team'
```

Both arguments accept whitespace-separated values; use `''`
for an empty user or team list. The resolver requires at least two distinct
people to allow an alternative approver when self-review is prevented.
GitHub checks reviewer eligibility, repository access, and the six-reviewer limit
when applying the environment. In the workflow, these errors can occur after
other hardening changes have been applied.
GitHub requires only one of those people to approve each deployment.
Team lookups additionally need organization Members read permission
(`read:org` for classic tokens). Users and team members are deduplicated by ID.
The script resolves approvers before updating the environment. With no arguments,
it uses `BODY` if nonempty, otherwise `{}`. Explicit arguments take precedence
over `BODY`.

For solo projects or plans without environment reviewers, use the default:

```bash
./.github/tools/harden/pypi.sh
```

### Benefits

- Improved security following
    [Open Source Security Foundation's Scorecard best practices](https://securityscorecards.dev/#the-checks).
- Enabled GitHub Pages for documentation hosting.
- Applied [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
    (including [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)).
- Required status checks (from GitHub Actions only) before merging to
    the default branch.
- Blocked tags shadowing long-running branches (e.g., a `main` tag).
- Configured pull request defaults and other repository settings.
- Activated GitHub security features (e.g., [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)).

> [!WARNING]
> Exact features depend on repository type,
> but in general: `public` > `enterprise` > `private`.

## Updates

> [!CAUTION]
> This feature is not yet implemented.

The template update workflow is a placeholder and does not currently update
repositories.

## Code sources

- `/.github/workflows/template-setup.yml`
- `/.github/workflows/template-update.yml`
- `/.github/workflows/harden.yml`
- `/.github/tools/harden`
- `/.github/rulesets`
