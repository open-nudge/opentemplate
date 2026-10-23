#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

HOMEPAGE=${HOMEPAGE:-'https://{owner}.github.io/{repo}'}
gh api --method PATCH "repos/{owner}/{repo}" \
    -F "allow_auto_merge=true" \
    -F "allow_merge_commit=false" \
    -F "allow_rebase_merge=false" \
    -F "allow_squash_merge=true" \
    -F "allow_update_branch=true" \
    -F "delete_branch_on_merge=true" \
    -F "use_squash_pr_title_as_default=true" \
    -F "has_issues=true" \
    -F "has_projects=true" \
    -F "has_wiki=false" \
    -F "homepage=${HOMEPAGE}" \
    -f "squash_merge_commit_title=PR_TITLE" \
    -f "squash_merge_commit_message=COMMIT_MESSAGES" \
    -F "web_commit_signoff_required=true"
