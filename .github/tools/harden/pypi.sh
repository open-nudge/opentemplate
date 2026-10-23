#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

case "$#" in
    0) body=${BODY:-'{}'} ;;
    2) body=$(./.github/tools/pypi/resolve.sh "$1" "$2") ;;
    *) echo "Usage: $0 ['<usernames>' '<team-slugs>'] (whitespace separated)" >&2; exit 1 ;;
esac

printf '%s\n' "${body}" | gh api --method PUT "repos/{owner}/{repo}/environments/pypi" --input -
