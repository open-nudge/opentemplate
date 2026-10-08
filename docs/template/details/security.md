<!--
SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
SPDX-FileContributor: szymonmaszke <github@maszke.co>

SPDX-License-Identifier: Apache-2.0
-->

# Security

This document outlines security practices in the template.

> [!NOTE]
> See [installation/hardening](../quickstart/installation.md)
> for additional security measures.

## Checks

Key security checks include:

- __Commit validation:__ Enforced signature and DCO sign-off
    ([`siderolabs/conform`](https://github.com/siderolabs/conform))

- __Branch protection:__ No direct commits to `main` enforced locally by
    [`prek` built-in `no-commit-to-branch` hook](https://prek.j178.dev/built-in-hooks/)

- __Vulnerability scanning:__ [`google/osv-scanner`](https://github.com/google/osv-scanner)

- __Malicious dependencies detection:__ [`DataDog/guarddog`](https://github.com/DataDog/guarddog)
    (runtime Python dependencies and GitHub Actions, CI only)

- __Secret scanning:__ [`trufflesecurity/trufflehog`](https://github.com/trufflesecurity/trufflehog)

- __Language-specific security checks:__

    - [`zizmor`](https://github.com/woodruffw/zizmor) for GitHub Actions security
    - [CodeQL](https://codeql.github.com/) for GitHub Actions security (CI only)
    - [`semgrep/semgrep`](https://github.com/semgrep/semgrep) for Python/general

- __Pinned dependencies:__ [OSSF Scorecard](https://github.com/ossf/scorecard/blob/main/docs/checks.md#pinned-dependencies)

> [!IMPORTANT]
> These checks run both locally (`prek`) and in CI/CD.

> [!TIP]
> Configuration is primarily in `pyproject.toml` and `prek.toml`,
> with a few additional settings in `.github/workflows`.

## GitHub Actions

> [!IMPORTANT]
> See [GitHub Actions section](github-actions.md) for details.

Security measures:

- __Minimal permissions__ for GitHub Actions
- __Software Bill of Materials (SBOMs):__ Generated, stored, and attested in releases
- __Reusable workflows__ for key tasks (e.g., `release`, `test`) to minimize
    misconfiguration risks
    ([more info](https://github.blog/security/supply-chain-security/slsa-3-compliance-with-github-actions/))
- __Egress monitoring:__ [`stepsecurity/harden-runner`](https://github.com/step-security/harden-runner)
- __Static analysis:__ [`actionlint`](https://github.com/rhysd/actionlint)

> [!IMPORTANT]
> Security checks (e.g., `scorecard`) run __weekly__.

## Security documents

> [!TIP]
> Review these documents and adapt them to your project.

Following [Open Source Security Foundation best practices](https://www.bestpractices.dev/en):

- __Security policy:__ [`SECURITY.md`](https://github.com/ossf/scorecard/blob/main/docs/checks.md#security-policy)
- __Machine-readable security insights:__ [`SECURITY-INSIGHTS.yml`](https://github.com/ossf/security-insights-spec)
- __Third-party dependency policy:__ [`SECURITY-DEPENDENCY.md`](../../SECURITY-DEPENDENCY.md)
- __Self-assessment report:__ [`SECURITY-SELF-ASSESSMENT.md`](../../SECURITY-SELF-ASSESSMENT.md)
    per [CNCF guidelines](https://tag-security.cncf.io/community/assessments/guide/self-assessment/#non-goals)
- __Changelog:__ [`CHANGELOG.md`](../../CHANGELOG.md) linking to
    GitHub releases ([FAQ](../about/faq.md))

> [!IMPORTANT]
> See the full [OpenSSF Scorecard checklist](https://github.com/ossf/scorecard/blob/main/docs/checks.md).

## Adjustments

Most security configurations (e.g., `check-security`, `check-workflow`) are in `pyproject.toml`.
Additional security workflows are in `.github/workflows` (prefix: `security-`).

### Security tab categories

Scanners do not upload results themselves (pull requests run without write
permissions). Their SARIF files are uploaded by
`.github/workflows/security-upload-reusable.yml` on `main` (push and weekly)
and during releases, one analysis per tool, categorized as
`/tool:<tool>/scope:<scope>/language:<language>`:

<!-- pyml disable-num-lines 12 line-length-->

| Tool        | Category                                                   |
| ----------- | ---------------------------------------------------------- |
| CodeQL      | `/tool:codeql/scope:workflows/language:actions`            |
| zizmor      | `/tool:zizmor/scope:workflows/language:actions`            |
| Semgrep     | `/tool:semgrep/scope:repository/language:all`              |
| OSV-Scanner | `/tool:osv-scanner/scope:dependencies/language:python`     |
| GuardDog    | `/tool:guarddog/scope:dependencies-<tier>/language:python` |
| GuardDog    | `/tool:guarddog/scope:actions/language:actions`            |
| Grype       | `/tool:grype/scope:sbom-<name>/language:python`            |
| Scorecard   | `/tool:scorecard/scope:repository/language:all`            |

> [!NOTE]
> Analyses uploaded under other categories (e.g. by previous template
> versions) are not replaced. Delete them under
> __Security → Code scanning → Tool status__ so their alerts get closed.

Analyses are kept per ref and category:

- `main` (push and weekly) replaces the previous `main` analysis,
    so the Security tab reflects the latest commit, not the latest release
- releases upload against the tag (separate from `main`); the SARIF files
    are also attested and attached to the GitHub release, describing
    exactly the released commit
- pull requests upload nothing, findings are listed in the job summary

### OSV Scanner

To ignore specific vulnerabilities, modify `osv-scanner.toml` ([docs](https://google.github.io/osv-scanner/configuration/)).

> [!WARNING]
> License-related issues in __currently defined__ development dependencies
> are ignored by default.

> [!TIP]
> `osv-scanner.toml` settings are respected by OSSF Scorecard.

### GuardDog

[GuardDog](https://github.com/DataDog/guarddog) looks for malicious code
(heuristics such as obfuscation, exfiltration or typosquatting) in Python
dependencies and in the source of third-party actions used by
`.github/workflows` steps (`.github/workflows/security-guarddog*.yml`).
Unlike OSV-Scanner, Grype or `zizmor`, it does not rely on known advisories.
GuardDog is installed (hash-locked) from the template's `dev-security` group.

Python dependencies are scanned per tier (as SBOMs are):

| Tier     | Dependencies     | Scanned on                     |
| -------- | ---------------- | ------------------------------ |
| `core`   | `--prod`         | releases                       |
| `extras` | `--prod -G :all` | pull requests, `main`, release |

> [!NOTE]
> Heuristics produce false positives, therefore findings do not fail the
> check. Review them in the Security tab (dismissed alerts stay dismissed).
> On pull requests findings are listed only in the job summary.

> [!IMPORTANT]
> Development dependencies are not scanned. GuardDog downloads every
> package anew (roughly 1.5 seconds per package), the template's own
> development dependencies (over 250 packages) take around 8 minutes.

Excluded rules (`--exclude-rules` in the reusable workflow):

- `capability-*` (Python dependencies only): describe normal behavior
    (reading files, spawning processes, network access), around 90% of
    findings for Python packages. Actions are scanned with all rules,
    their capabilities (e.g. downloads, spawned processes) are few
    and worth triaging in the Security tab
- `repository_integrity_mismatch`: fully clones the GitHub repository of
    every package (for 68 dependencies it took 10 minutes instead of 2,
    a single repository took over 5 minutes), finding no issues in practice

> [!WARNING]
> Maintainers' e-mail domains are checked with WHOIS (unclaimed or
> re-registered domains indicate account takeover risk).
> [`harden-runner`](https://github.com/step-security/harden-runner)
> allows only the WHOIS servers of currently used top-level domains.
> If the job warns about coverage and its log shows
> `Error trying to connect to socket`, add the missing registry
> (see its IANA entry) to the reusable workflow.

Known limitations (the job warns when something was not scanned):

- GuardDog exits successfully even if a package could not be downloaded
- actions referenced by a path inside a repository
    (e.g. `github/codeql-action/init`) and `docker://` images are not scanned,
    neither are actions used by composite actions in `.github/actions`
- each action is scanned once per workflow using it, alerts point to the
    first such workflow

### CodeQL

[CodeQL](https://codeql.github.com/) only analyzes GitHub Actions workflows
(`.github/workflows/security-codeql*.yml`).
Pull requests fail on any finding, while results are uploaded to the
Security tab on `main` (push and weekly) and attached to releases.

> [!IMPORTANT]
> Dismissing an alert in the Security tab does not affect the check,
> the findings have to be fixed.

> [!WARNING]
> GitHub's CodeQL _default setup_ rejects uploads of the advanced setup.
> `harden.yml` disables it (best effort), otherwise go to
> __Settings → Advanced Security → CodeQL analysis → ⋯__
> and choose __Disable CodeQL__ (or __Switch to advanced__).
> If an organization security configuration enforces default setup,
> an organization owner has to change it.

> [!NOTE]
> Advanced setup needs no switch, the first upload enables code scanning
> for public repositories. Private repositories need
> GitHub Code Security, see
> [Without GitHub Code Security](#without-github-code-security).

### zizmor

[zizmor](https://github.com/zizmorcore/zizmor) audits GitHub Actions
workflows (`check-github` in `pyproject.toml`) on pull requests, on `main`
(push and weekly) and during releases.

> [!IMPORTANT]
> Outside of pull requests zizmor is installed from `open-nudge/opentemplate`
> (`dev-security` group) and ignores zizmor configuration files
> (`--no-config`), so the attested results cannot be altered by the project.
> Use inline `# zizmor: ignore[<audit>]` comments instead.

### Without GitHub Code Security

Private repositories need
[GitHub Code Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)
(formerly part of GitHub Advanced Security) for the Security tab.
Without it set the `NO_GITHUB_CODE_SECURITY` configuration variable
(repository or organization) to any value, e.g. `true`, which:

- skips CodeQL (the required check passes as skipped), as its
    [license](https://securitylab.github.com/tools/codeql/license/)
    does not allow analyzing private code without GitHub Code Security
- skips uploads to the Security tab, findings are listed in the job
    summary of each scanner instead (checks still fail on findings)

> [!NOTE]
> SARIFs are still produced and attached to releases. Their attestation
> depends only on `NO_GITHUB_ENTERPRISE_CLOUD`
> (see [release process](../release-your-project/process.md)).

> [!CAUTION]
> __This escape hatch is ignored for public and internal repositories!__

### Conform

[`siderolabs/conform`](https://github.com/siderolabs/conform) enforces
DCO sign-off and GPG signatures. Modify `.conform.yml` to adjust checks.

## Additional resources

- [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/)
- [CNCF Tag Security](https://tag-security.cncf.io/)
