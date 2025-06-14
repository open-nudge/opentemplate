<!--
SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Documentation

Perform adaptations in the `mkdocs.yml` if you want to change
the properties of the documentation (e.g. theme, title, and so on).

## Sections

### Provided

The following sections are provided:

- Reference - code reference, public API documentation, etc.,
    __automatically generated from the codebase__
- For contributors - how to contribute to the project, guidelines,
    governance and similar
- Security - security-related information of the project
- Legal - legal information, licenses and similar
- Hall of fame - list of adopters and announcements

> [!TIP]
> See `mkdocs.yml` for more details

### Predefined

Predefined sections (each in a separate folder)
which you can fill up with your content:

- [`tutorials`](./tutorials/README.md)
- [`how-tos`](./how-to/README.md)
- [`explanations`](./explanations/README.md)

> [!TIP]
> See the README.md in each folder for more details

> [!NOTE]
> If you do not need one of the above sections, you do not have to delete it.
> These will not be included automatically if there is no content.

### Advised

Sections below are not predefined, nor mandatory, but you may consider adding
them:

- About - general information about the project which may include:
    - History - history of the project (naming, milestones, fun facts)
    - Alternatives - similar software and comparisons
    - Benchmarks - performance, possibly compared to alternatives
- FAQ - frequently asked questions
- Hall of fame additions, which may include:
    - Testimonials - quotes from adopters
    - Case studies - detailed stories of adopters
    - Sponsorship - information about sponsors
    - Acknowledgements - thank you notes
    - Contributors - list of contributors

## Resources

- [Diátaxis](https://diataxis.fr/) - a conceptual framework for documentation
