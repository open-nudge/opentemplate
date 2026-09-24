#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Change local references to global references in GitHub Actions workflows
# skip_files should be a comma-separated list of files to skip
# Usage: ./reusability/globalize.sh [directory] [skip_files] [repository] [commit_sha]

directory="${1:-.github}"
skip_files="${2:-}" # Comma-separated list of files to skip
repo="${3:-open-nudge/opentemplate}" # Customizable repository reference
ref="${4:-}"
comment=""

if [[ -z "${ref}" ]]; then
    remote_ref="$(git ls-remote "https://github.com/${repo}.git" refs/heads/main)"
    ref="${remote_ref%%$'\t'*}"
    if [[ -z "${ref}" ]]; then
        printf 'Unable to resolve the latest commit on %s main\n' "${repo}" >&2
        exit 1
    fi
else
    comment="# zizmor: ignore[unpinned-uses]"
fi

IFS=',' read -r -a skip_array <<< "${skip_files}"

# enq: every matching file is processed independently by the loop
# shellcheck disable=SC2312
find "${directory}" -type f -name '*.yml' -print0 | while IFS= read -r -d '' file; do
    [[ -f "${file}" ]] || continue  # Skip if no files match

    for skip in "${skip_array[@]}"; do
        if [[ "$(basename "${file}")" = "${skip}" ]]; then
            printf 'Skipped: %s\n' "${file}"
            continue 2
        fi
    done

    awk -v repo="${repo}" -v ref="${ref}" -v comment="${comment}" '
    {
        if ($0 ~ /uses: "\$\/\.github\//) {
            gsub(/uses: "\$\/\.github\//, "uses: \"" repo "/.github/");
            sub(/"$/, "@" ref "\"");  # Add @ref before the closing quote
            if (comment != "") {
                $0 = $0 " " comment;
            }
        }
        print;
    }' "${file}" > "${file}.tmp"

    # Compare original and modified file, only replace if different
    if ! cmp -s "${file}" "${file}.tmp"; then
        mv "${file}.tmp" "${file}"
        printf 'Updated: %s\n' "${file}"
    else
        rm "${file}.tmp"
    fi

done
