#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2025, 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Run mutation testing with mutmut, forwarding all arguments.
# mutmut errors out when there is nothing to mutate (e.g. source code
# without any mutation candidates), which should not fail the pipeline.

set -uo pipefail

mutmut run "$@"
STATUS=$?

if [[ "${STATUS}" -eq 0 ]]; then
  exit 0
fi

mapfile -d '' METAS < <(find mutants -name '*.meta' -print0 2>/dev/null || true)

if [[ "${#METAS[@]}" -eq 0 ]]; then
  exit "${STATUS}"
fi

for META in "${METAS[@]}"; do
  if ! grep -qF '"exit_code_by_key": {}' "${META}"; then
    exit "${STATUS}"
  fi
done

echo "No mutants were generated, skipping mutation testing."
