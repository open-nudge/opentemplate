<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Release checklist

> [!NOTE]
> While automation handles most of the release process,
> some project-specific details require manual updates.

## [README](../../index.md)

1. Update __`Features`__ section with ~5 key points.

1. Keep __`Usage`__ clear and concise.

1. Add `__Examples__`:

    1. Basic usage

    1. Common task

    1. Advanced/expert-level usage

> [!CAUTION]
> Review [README](../../index.md) after changes to ensure coherence.

## pyproject.toml

> [!CAUTION]
> Do not edit sections starting with `DO NOT EDIT UNTIL end marker`
> and ending with `[[[end]]]`.

- `[project.classifiers]` – Add relevant
    [PyPI classifiers](https://pypi.org/classifiers/).
- `[project.dependencies]` and `[project.optional-dependencies]` – Double-check
    correctness.

> [!TIP]
> For public projects after the first release, remove `exclude_links`
> in `[tool.md_dead_link_check]` to validate all links.

## Documentation

> [!CAUTION]
> Adjust `/docs` structure and content as needed.

You should consult the [documentation guide](../details/documentation.md)
for more details.

> [!NOTE]
> Content in folders like `/docs/tutorials` is auto-included via
> [`mkdocs-awesome-pages`](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin)
> if any content is present there.

> [!CAUTION]
> Manually validate `mkdocs.yml` and generated docs.

## Security

- Verify and update `CODEOWNERS`
    ([docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)).
- Complete `TBD` sections in `SECURITY-SELF-ASSESSMENT.md`
    ([CNCF guide](https://tag-security.cncf.io/community/assessments/guide/self-assessment/#non-goals)).
- __Optional:__ Add more contact details to [`SECURITY.md`](../../SECURITY.md).

## Documents

- Ensure `ROADMAP.md` outlines plans for the next release (if applicable).
- __Optional:__ Add more governance details to [`GOVERNANCE.md`](../../GOVERNANCE.md).
