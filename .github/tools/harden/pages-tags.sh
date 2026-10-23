#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

endpoint="repos/{owner}/{repo}/environments/github-pages"
gh api --method PUT "${endpoint}" \
    -F "deployment_branch_policy[protected_branches]=false" \
    -F "deployment_branch_policy[custom_branch_policies]=true"
policies=$(gh api --paginate "${endpoint}/deployment-branch-policies?per_page=100" | jq -s '[.[].branch_policies[]]')
if ! jq -e 'any(.[]; .name == "*" and .type == "tag")' <<< "${policies}" >/dev/null; then
    gh api --method POST "${endpoint}/deployment-branch-policies" -f "name=*" -f "type=tag"
fi
