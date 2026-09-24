#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

mode="$1"
shift
files=("$@")

if (( ${#files[@]} == 0 )); then
    # enq: tracked-file discovery failures are non-fatal
    # shellcheck disable=SC2312
    while IFS= read -r -d '' file; do
        files+=("${file}")
    done < <(git ls-files -z)
fi

arguments=()
if [[ "${mode}" == "fix" ]]; then
    arguments+=("--write-changes")
fi

codespell "${arguments[@]}" "${files[@]}"
