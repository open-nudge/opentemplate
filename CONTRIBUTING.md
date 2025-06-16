<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Contributing guide

## Table of contents

- [General](#general)
- [Non-code contributions](#non-code-contributions)
- [Code contributions](#code-contributions)
    - [Prerequisites](#prerequisites)
    - [Environment setup](#environment-setup)
    - [Source code](#source-code)
    - [Making changes](#making-changes)
    - [Committing changes](#committing-changes)
    - [Creating a Pull Request](#creating-a-pull-request)
    - [Merging Pull Requests](#merging-pull-requests)
- [Coding style](#coding-style)
- [Releases](#releases)

## General

We welcome all contributions from the community.
Adhere to [Code of Conduct](./CODE_OF_CONDUCT.md) at all times.

## Non-code contributions

We welcome non-code contributions as well. If you have any suggestions,
ideas, or want to report a bug, follow these steps:

1. Verify [open issues](https://github.com/open-nudge/opentemplate/issues)
    to see if someone reposrted similar issue or requested a similar feature.
1. If the issue exists, upvote it and share more information
    in a comment (use cases, examples and so on).
1. If the issue does not exist, create a new one from the
    [Issues Templates](https://github.com/open-nudge/opentemplate/issues/new/choose)
    tab.
1. Follow the appropriate template for the issue

## Code contributions

### Prerequisites

1. Read [ROADMAP](ROADMAP.md) to understand the project's goals.
1. Read Developer's Certificate of Origin (DCO) in [DCO.md](DCO.md)
    (you must sign-off your PRs).
1. Read [LICENSE](LICENSE.md).
1. Follow the steps in [Non-code contributions](#non-code-contributions)
    and report a bug or request a feature.
1. Fork the repository
    (see [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
    for more information).

### Environment setup

Prerequisites (one time setup):

1. Check you have Python 3.x installation available (as `python3` or `python`)
1. Install `pdm` (see [official installation instructions](https://pdm-project.org/en/latest/))
1. Enable `pep582` globally (see [official instructions](https://pdm-project.org/latest/usage/pep582/#enable-pep-582-globally))

Change to the cloned directory and run:

```bash
pdm setup
```

> [!CAUTION]
> This project uses [PEP582](https://peps.python.org/pep-0582/) to manage dependencies.
> Check `__pypackages__/README.md` for more information.

<!-- vale off -->

> [!TIP]
> Check [here](https://pdm-project.org/latest/usage/pep582/#configure-ide-to-support-pep-582)
> for more information on IDE configuration with PEP582.

<!-- vale on -->

### Source code

After the setup, you will, probably, contribute to the following directories:

- [`src/`](https://github.com/open-nudge/opentemplate/blob/main/src/README.md)
    with the source code of the project
- [`tests/`](https://github.com/open-nudge/opentemplate/blob/main/tests/README.md)
    with the project's tests

Check [project documentation](https://open-nudge.github.io/opentemplate)
and `code`/`docs` in these folders for more information.

### Making changes

Keep the following in mind:

- __Tests matter__ - use `hypothesis` (or similar) for property-based
    testing if possible.
- __Any changes need 100% test coverage__ - if not possible,
    explain why in the comments or PR description and exclude these lines).
- __Your changes should pass [pre-commit hooks](https://pre-commit.com/)__.

<!-- vale off -->

> [!NOTE]
> Pre-commit hooks automatically fix your code, therefore you might
> have to recommit multiple time before the commit is accepted.

<!-- vale on -->

### Committing changes

Please follow the simplified [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
standard in every commit, for example:

```bash
git commit -s -S -m "feat: add new feature"
```

- You can __only use `fix`, `feat`, `fix!`, `feat!`__ types,
    __we do not accept any other types__ (e.g. `chore`, `refactor`, `docs` and
    others).
- Your commits should be atomic and should not contain many changes.
- __Your commits have to be signed-off (use `-s` flag in `git commit` as in
    the example above).__ Please see the [DCO](DCO.md) for more information.
- __Your commits have to be signed (use `-S` flag in `git commit` as in
    the example above).__ Please see the [Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
    for more information.

<!-- vale off -->

> [!TIP]
> You can use `pdm commit-guided` for interactive commit adhering to the guide.

> [!TIP]
> You can use `pdm commit` (same as `git commit -s -S`).

> [!TIP]
> You can use `pdm commit-fast`, a faster version of `commit-guided`.

> [!NOTE]
> Signing and commit messages are automatically checked
> by the pre-commit hooks and CI/CD pipeline.

<!-- vale on -->

### Creating a pull request

Follow [GitHub Flow](https://guides.github.com/introduction/flow/);
`main` branch should always be in the releasable state.

__Small pull requests are encouraged.__ If, for some reason,
you cannot make small a pull request, describe the reasons in the
`pull request` description.

Pull requests have to be:

- __Contain `type` akin to the commits__;
    Same rules apply (only `fix`, `feat`, `fix!`, `feat!` allowed)
- __Linked to the `issue`__ via `Closes #XXX`
    (where `XXX` is the issue number) in the description.
- Target the `main` branch.
- Contain descriptive header and (optionally) description.

<!-- vale off -->

> [!TIP]
> Type of the pull request should be the largest
> of all commits (`feat!` > `fix!` > `feat` > `fix`)

<!-- vale on -->

Other features:

- Pull requests will be automatically labeled based on the type of the commit
    (in some cases, you might want to manually add the label from the existing ones).
- __Stale pull requests__ (no changes for 7 days) will be automatically closed
    (can be reopened later).
- Pull requests will be automatically checked by the CI/CD pipeline.

> [!WARNING]
> Once you submit a PR, __do not rebase it__ (easier to review the changes).

### Merging pull requests

Maintainers will merge your pull request __only after the CI/CD checks pass__.
In general, if `pre-commit` checks pass, no major changes should be necessary.

<!-- vale off -->

> [!NOTE]
> We use `Squash and Merge` strategy for merging pull requests, individual
> commits should not matter if they follow the guidelines.

<!-- vale on -->

If you need help with this part of the process, tag one of the maintainers
in the PR.

## Coding style

`pre-commit` hooks check most of the guidelines, but maintainers
reserve the right to ask for changes in the code style if necessary.

In special cases you might want to ignore a certain style rule,
if so, describe the reason in the comment.

## Releases

After maintainers merged your PR, your changes will be automatically
included in the next release.

- __We release new versions of the project after each change__ according
    to the [Semantic Versioning](https://semver.org/) specification.
- [CHANGELOG](CHANGELOG.md) links to the release notes.
- __We show certain releases to the public__
    by a blog post or a similar announcement (see [ANNOUNCEMENTS](ANNOUNCEMENTS.md)).
- Public releases comprise of a few merged pull requests and are
    performed under maintainers' discretion.
