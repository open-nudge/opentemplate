#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <approvals: 0|1|2> <ruleset-directory>" >&2
    exit 1
fi
case "$1" in
    0) last_push=false ;;
    1|2) last_push=true ;;
    *) echo "Approvals must be 0, 1, or 2" >&2; exit 1 ;;
esac

shopt -s nullglob
files=("$2"/*.json)
if [[ ${#files[@]} -lt 1 ]]; then
    echo "No ruleset JSON files found in $2" >&2
    exit 1
fi

# Snapshot repository-owned IDs only; inherited rulesets are never replaced.
existing=$(gh api --paginate "repos/{owner}/{repo}/rulesets?includes_parents=false&per_page=100" --jq '.[].id')

for file in "${files[@]}"; do
    jq --argjson reviewers "$1" --argjson last_push "${last_push}" '
        walk(if . == "PLACEHOLDER_REVIEWERS" then $reviewers
             elif . == "PLACEHOLDER_LAST_PUSH_APPROVAL" then $last_push
             else . end)' "${file}" \
        | gh api --method POST "repos/{owner}/{repo}/rulesets" --input -
done

# Only start deleting once every replacement has been created successfully.
for id in ${existing}; do
    gh api --method DELETE "repos/{owner}/{repo}/rulesets/${id}"
done
