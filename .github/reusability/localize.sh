#!/usr/bin/env sh

# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Change global references to local references in GitHub Actions workflows
# skip_files should be a comma-separated list of files to skip
# Usage: ./reusability/localize.sh [directory] [skip_files]

directory="${1:-./workflows}"
skip_files="${2:-}" # Comma-separated list of files to skip
repo="${3:-open-nudge/opentemplate}" # Customizable repository reference

# shellcheck disable=SC3045,SC3011
IFS=',' read -r -a skip_array <<< "${skip_files}"

# shellcheck disable=SC3045
find "${directory}" -type f -name '*.yml' -print0 | while IFS= read -r -d '' file; do
    [ -f "${file}" ] || continue  # Skip if no files match

    # Check if file should be skipped
    # shellcheck disable=SC3054
    for skip in "${skip_array[@]}"; do
        if [ "$(basename "${file}")" = "${skip}" ]; then
            printf 'Skipped: %s\n' "${file}"
            continue 2
        fi
    done

    awk -v repo="${repo}" '
    {
        if ($0 ~ "uses: \"" repo "/.github/") {
            # Replace repo with local path
            gsub("uses: \"" repo "/.github/", "uses: \"./.github/");

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
