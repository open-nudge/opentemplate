#!/usr/bin/env sh

# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Change the name of all actions in a directory from X to Y
# Usage:
#  ./tools/update-actions-names.sh <X> <Y> [directory]
# Ensure at least two arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <X> <Y> [directory]"
    exit 1
fi

X="$1"
Y="$2"
DIRECTORY="${3:-./workflows}"

for file in "${DIRECTORY}"/*.yml; do
    [ -f "${file}" ] || continue  # Skip if no files match

    awk -v x="${X}" -v y="${Y}" '
    {
        gsub("uses: \./\.github/actions/" x, "uses: \./\.github/actions/" y);
        print;
    }' "${file}" > "${file}.tmp"

    # Compare original and modified file, only replace if different
    if ! cmp -s "${file}" "${file}.tmp"; then
        mv "${file}.tmp" "${file}"
        printf 'Updated: %s' "${file}"
    else
        rm "${file}.tmp"
    fi

done
