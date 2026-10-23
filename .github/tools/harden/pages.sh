#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

# Pages uses POST for creation and PUT for updates
# Only a missing site (404) should trigger creation; propagate other failures.
if response=$(gh api --include "repos/{owner}/{repo}/pages"); then
    method=PUT
elif [[ "${response}" =~ ^HTTP/[^[:space:]]+[[:space:]]404[[:space:]] ]]; then
    method=POST
else
    echo "Could not inspect GitHub Pages" >&2
    exit 1
fi

gh api --method "${method}" "repos/{owner}/{repo}/pages" -f "build_type=workflow"
