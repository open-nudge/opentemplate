#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Change global references to local references in GitHub Actions workflows
# skip_files should be a comma-separated list of files to skip
# Usage: ./reusability/localize.sh [directory] [skip_files] [repository]

directory="${1:-.github}"
skip_files="${2:-}" # Comma-separated list of files to skip
repo="${3:-open-nudge/opentemplate}" # Customizable repository reference

IFS=',' read -r -a skip_array <<< "${skip_files}"

# enq: every matching file is processed independently by the loop
# shellcheck disable=SC2312
find "${directory}" -type f -name '*.yml' -print0 | while IFS= read -r -d '' file; do
    [[ -f "${file}" ]] || continue  # Skip if no files match

    # Check if file should be skipped
    for skip in "${skip_array[@]}"; do
        if [[ "$(basename "${file}")" = "${skip}" ]]; then
            printf 'Skipped: %s\n' "${file}"
            continue 2
        fi
    done

    awk -v repo="${repo}" '
    {
        if ($0 ~ "uses: \"" repo "/.github/") {
            # Replace repo with local path
            gsub("uses: \"" repo "/.github/", "uses: \"$/.github/");

            # Remove @ref from quoted uses (e.g., @main)
            gsub(/@[^"]+/, "");

            # Remove comment after the closing quote (optional)
            sub(/"[[:space:]]+#.*/, "\"");
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
