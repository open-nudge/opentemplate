#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

# enq: keep the portable numeric argument-count check
# shellcheck disable=SC2292
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 '<usernames>' '<team-slugs>' (whitespace separated)" >&2
    exit 1
fi

# Split input into names without expanding wildcard characters into filenames.
set -f
IFS=$' \t\r\n'
reviewers=()

for user in $1; do
    reviewer=$(gh api "users/${user}" --jq '{type, id}')
    reviewers+=("${reviewer}")
done

for team in $2; do
    id=$(gh api "orgs/{owner}/teams/${team}" --jq '.id')
    members=$(gh api --paginate \
        "orgs/{owner}/teams/${team}/members?per_page=100" \
        --jq '.[] | select(.type == "User") | .id')
    reviewer=$(printf '%s\n' "${members}" | jq -cs --argjson id "${id}" \
        '{type: "Team", id: $id, members: .}')
    reviewers+=("${reviewer}")
done

printf '%s\n' "${reviewers[@]}" | jq -cs '
    ([.[] | select(.type == "User") | .id] + [.[].members[]?]
        | unique | length) as $count
    | if $count < 2 then
        error("Release approvers must cover at least 2 distinct people")
      else
        {
            prevent_self_review: true,
            reviewers: (map({type, id}) | unique)
        }
      end'
