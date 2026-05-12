<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Tests

This document outlines the testing process of `opentemplate`-based projects.

## Features

- Uses [`pytest`](https://github.com/pytest-dev/pytest) for testing.
- Collects doctests from source modules.
- Measures test coverage with [`coverage`](https://github.com/nedbat/coveragepy)
    (default threshold: `100%`).
- Runs mutation testing with [`mutmut`](https://mutmut.readthedocs.io/en/latest/).
- __Local testing:__ Runs on the latest three Python versions,
    following [SPEC 0](https://scientific-python.org/specs/spec-0000/),
    then runs mutation testing once.
- __CI testing:__ Runs across multiple Python versions and
    OSs (Linux, macOS, Windows) via GitHub Actions.
- __CI mutation testing:__ Runs once on Ubuntu, as `mutmut`
    requires fork support.
- __Randomized test execution__ ensures independence.
- Includes [`Hypothesis`](https://github.com/HypothesisWorks/hypothesis)
    for property-based testing.

> [!NOTE]
> `tox` is not used; instead, tests are run with different interpreters
> locally and across CI runners.

## Writing tests

- All tests are in the `tests` directory, named `test_.py`.
- Tests should follow `pytest` style.
- __Recommended:__ Use [`Hypothesis`](https://github.com/HypothesisWorks/hypothesis)
    for property-based testing, as required
    by [OSSF Scorecard](https://github.com/ossf/scorecard).

> [!TIP]
> `opentemplate` does not enforce a specific testing style,
> but methodologies like Test/Behavior Driven Development may be beneficial.

## Checks and fixes

Tests should be documented, formatted, and typed as they will be checked like
regular source code.

> [!TIP]
> See the [Python section](python.md) for more information.

## Adjustments

> [!NOTE]
> All changes apply to the CI as well.

- To change coverage requirements, update the `fail_under`
    flag in `[tool.coverage.report]` section in `pyproject.toml`
- To change mutation testing, update the `[tool.mutmut]` section
    in `pyproject.toml`.
- To change the test runner, update the `tests-coverage` script in
    the `pyproject.toml` file.

## Code sources

- `pyproject.toml`
- `.github/workflows/tests*.yml`
- `.github/workflows/typing*.yml`
