#!/usr/bin/env sh

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Remove template-only blocks (markers included) from tracked files:
#
#   # templatedelete-start
#
#   # templatedelete-end
#
# Markers are matched as substrings, so any comment syntax works.

set -eu

START="templatedelete-start"
END="templatedelete-end"

git grep -l "${START}" -- ':!template-setup' | while IFS= read -r file; do
  starts="$(grep -c "${START}" "${file}")"
  ends="$(grep -c "${END}" "${file}")"
  if [ "${starts}" -ne "${ends}" ]; then
    echo "Unbalanced template markers in: ${file}" >&2
    exit 1
  fi
  echo "Removing template-only blocks from: ${file}"
  sed -i "/${START}/,/${END}/d" "${file}"
done

echo "Template-only blocks removed."
