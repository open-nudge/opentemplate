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
    done < <(
        git ls-files -z -- "*.md" ":!DCO.md" ":!docs/LICENSE.md" \
            ":!template-setup/**" ":!LICENSE" ":!LICENSES/**" ":!.agents/**"
    )
fi

if [[ "${mode}" == "fix" ]]; then
    mdformat "${files[@]}"
    pymarkdownlnt fix -r "${files[@]}"
fi

mdformat --check "${files[@]}"
pymarkdownlnt scan -r "${files[@]}"
md-dead-link-check "${files[@]}"
