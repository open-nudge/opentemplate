<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Environment dependencies policy

## Purpose

This policy describes how `opentemplate` maintainers
consume third-party packages.

## Scope

This policy applies to all `opentemplate` maintainers
and all third-party packages used in the `opentemplate`
project.

## Policy

`opentemplate` contributors must follow these guidelines
when consuming third-party packages:

### General

- Only use third-party packages necessary for the functionality of
    `opentemplate`.
- Use maintained third-party packages with a reasonably good reputation.
- Prefer small, single-purpose packages over large, complex ones.
- Implement small functionalities within the project instead of
    using a third-party package (unless the third-party package is lightweight,
    well-maintained and has a good reputation).
- Avoid using third-party packages with known security vulnerabilities.
- Before sending changes with new dependencies, make sure all automated
    tests pass (`pre-commit` checks and continuous integration pipelines)

### Versioning

- Use package manager to manage third-party dependencies.
- Lock __all of the dependencies__ (including developer tools) before
    merging the changes.
- Specify __only__ `major` versions for all stable third-party packages
    (version `1.x.y` or above) unless `minor` or `patch` versions
    are required for compatibility or functionality.
- Specify `major`, `minor`, and `patch` versions for all pre-release
    third-party packages (version `0.x.y`).
- Use the latest `major` version of all third-party packages whenever possible.

## Procedure

When adding a new third-party package to `opentemplate`,
contributors must follow these steps:

1. Is the package necessary for the functionality
    of `opentemplate`?
1. How stable is the package? Is it a pre-release version (`0.x.y`) or a stable
    version (`1.x.y` or above)?
1. Research the package. Is it well-maintained? Does it have a good reputation?
1. Choose a compatible version of the package.
    Use the latest version whenever possible.
1. Update the `pyproject.toml` and lock the dependencies.

## Archived or deprecated packages

When a third-party package is discontinued, the `opentemplate`
maintainers must ensure replacement of the package with a suitable alternative.

## Enforcement

This policy is enforced by the `opentemplate` maintainers.
Maintainers are expected to review each other's code changes to ensure
that they comply with this policy.

## Exceptions

Exceptions to this policy may be granted by the `opentemplate`
maintainers/leaders on a case-by-case basis.

## Credits

This policy was adapted from the
[Kubescape Community](https://github.com/kubescape/kubescape/blob/master/docs/environment-dependencies-policy.md)
and
[Project Capsule](https://github.com/projectcapsule/capsule/blob/main/DEPENDENCY.md)
