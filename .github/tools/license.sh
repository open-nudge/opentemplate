#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Print SPDX identifier of the LICENSES/ file identical to /LICENSE
# Used by fix-legal (pyproject.toml) and as a consistency check (prek.toml)
# /LICENSE must be a regular file, GitHub's license detection skips symlinks
if [[ -L LICENSE ]]; then
    echo "LICENSE must be a regular file, not a symlink" >&2
    exit 1
fi

for file in LICENSES/*.txt; do
    if cmp -s LICENSE "${file}"; then
        basename "${file}" .txt
        exit 0
    fi
done

echo "LICENSE must be an exact copy of a file in LICENSES/" >&2
exit 1
