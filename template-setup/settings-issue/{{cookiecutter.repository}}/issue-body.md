<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

<!-- pyml disable-num-lines 120 line-length,single-title,single-h1 -->

> [!CAUTION]
> This issue is raised due to current limitations of the GitHub API and/or for security reasons.
> __Human should review and apply all/some of the settings__ described here.

# Pre-requisites

Enable the following for all repositories:

- __[StepSecurity Actions Security](https://github.com/apps/stepsecurity-actions-security)__ (manages GitHub Actions egress rules).

> [!NOTE]
> If [StepSecurity App](https://github.com/apps/stepsecurity-actions-security) is not installed, your code remains functional but less secure. More details [here](https://github.com/step-security/harden-runner).

# Security hardening

Follow these steps for best practices (available in your plan).

## Creating Personal Access Token (PAT)

> [!CAUTION]
> Use the suggested scope and expiration date to reduce exposure.

1. Go to [__GitHub Personal Access Token__ creation page](https://github.com/settings/personal-access-tokens/new) and create a token with:

- __Token name__: {{cookiecutter.repository}}-one-time-settings

- __Resource owner__: {{cookiecutter.repository_owner}}

- __Expiration date__: Custom ➡️ next day

- __Repository access__: Only select repositories ➡️ Select repositories ➡️ {{cookiecutter.repository_owner}}/{{cookiecutter.repository}}

- __Permissions__: Repository permissions:

  - __Contents__: Read & write (globalize local workflow references and commit the result)
  - __Workflows__: Read & write (update workflow files)
  - __Administration__: Read & write (multiple operations: [`rulesets`](https://docs.github.com/en/rest/repos/rules?apiVersion=2022-11-28#create-a-repository-ruleset), [`gh-pages`](https://docs.github.com/en/rest/pages/pages?apiVersion=2022-11-28#create-a-github-pages-site), [general](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#update-a-repository), [private vulnerability reporting](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#enable-private-vulnerability-reporting-for-a-repository), [vulnerability alerts](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#enable-vulnerability-alerts), [environments](https://docs.github.com/en/rest/deployments/environments?apiVersion=2022-11-28#create-or-update-an-environment), enabling discussions)
  - __Pages__: Read & write (setup `gh-pages`; [permission source](https://docs.github.com/en/rest/pages/pages?apiVersion=2022-11-28#create-a-github-pages-site))

- __Permissions__: Organization permissions (__only__ if passing __PyPI release teams__):

  - __Members__: Read (resolve teams and [count their members](https://docs.github.com/en/rest/teams/members?apiVersion=2022-11-28#list-team-members))

> [!WARNING]
> Prefer a repository secret. An organization-level secret exposes this token to more repositories; if you use one, restrict its access to this repository.

> Click __Generate token__ and copy it.

1. Add it to repository secrets:

- Open [secrets](https://github.com/{{cookiecutter.repository_owner}}/{{cookiecutter.repository}}/settings/secrets/actions/new)
- __Name__: `TEMPLATE_GITHUB_TOKEN` (__exactly this name__).
- __Secret__: Paste the token.

## Running the workflow

Manually run the `Harden` workflow ([click here](https://github.com/{{cookiecutter.repository_owner}}/{{cookiecutter.repository}}/actions/workflows/harden.yml)) and enter:

- __Plan type__: [Check here](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) if unsure.
- __Contributors (including you)__: `1` (solo, no required approvals), `2` (each pull request approved by the other person), `3 (or more)` (each pull request approved by two people other than its author, most secure). Read more [here](https://github.com/ossf/scorecard/blob/main/docs/checks.md#branch-protection).
- __PyPI release reviewers__: GitHub usernames approving PyPI releases, e.g. `alice, bob`.
- __PyPI release teams__: organization team slugs approving PyPI releases, e.g. `core` (teams need access to this repository).

> [!IMPORTANT]
> Release reviewers and/or teams are required with `2` or more contributors in public or Enterprise repositories. At most 6 entries (users and teams combined) are allowed and they must cover at least 2 distinct people, so whoever publishes a release can never approve it while someone else always can.

## Cleanup

Remove `TEMPLATE_GITHUB_TOKEN` from [repository secrets](https://github.com/{{cookiecutter.repository_owner}}/{{cookiecutter.repository}}/settings/secrets/actions).

# PyPI deployment

> [!CAUTION]
> __Skip if you want a private project.__ You can enable this later.

To deploy a Python package to PyPI:

Go to [PyPI Publishing](https://pypi.org/manage/account/publishing/), scroll to "Add a new pending publisher" and enter:

- __PyPI Project Name__: {{ cookiecutter.repository }}
- __Owner__: {{ cookiecutter.repository_owner }}
- __Repository name__: {{ cookiecutter.repository }}
- __Workflow name__: release.yml
- __Environment name__: pypi

> [!IMPORTANT]
> The `Harden` workflow creates the `pypi` environment. With `2` or more contributors, publishing requires approval from one of the __PyPI release reviewers__ other than the release publisher.
> Approvers are checked only after running `harden` workflow. If they later drop to one person, add approvers or disable __Prevent self-review__ in [environment settings](https://github.com/{{cookiecutter.repository_owner}}/{{cookiecutter.repository}}/settings/environments).

GitHub Actions will now deploy to PyPI on new releases (pushed tags or the `Release Tag` workflow).

> [!TIP]
> Releasing to PyPI after the setup is advised. Due to the versioning scheme, first release will be `0.0.1` which can be iterated later on (with `0.1.0` marking first usable release).

{% if not cookiecutter.has_dependency_graph %}

# Dependency Graph

[Enable Dependency Graph manually](https://github.com/{{cookiecutter.repository_owner}}/{{cookiecutter.repository}}/settings/security_analysis). __Without it, GitHub SBOM will not appear in `Releases`__.

{% endif %}

# Organization setup

> [!TIP]
> Refer to [this guide](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) for community health files (e.g. `funding.yml`).

# Additional resources

- [Open Source Guide](https://opensource.guide/)
- [Open Source Security Foundation Guides](https://openssf.org/resources/guides/)
