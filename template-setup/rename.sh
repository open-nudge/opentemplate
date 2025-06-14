#!/usr/bin/env sh

# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Check for required arguments
if [ "${#}" -lt 8 ]; then
  echo "Usage: $0 \
    <TEMPLATE_REPOSITORY> <REPOSITORY> \
    <TEMPLATE_OWNER> <OWNER> \
    <TEMPLATE_DESCRIPTION> <DESCRIPTION> \
    <SKIP_N_LINES> <EXCLUDE_LIST>"
  exit 1
fi

TEMPLATE_REPOSITORY="${1}"
REPOSITORY="${2}"
TEMPLATE_OWNER="${3}"
OWNER="${4}"
TEMPLATE_DESCRIPTION="${5}"
DESCRIPTION="${6}"
SKIP_N_LINES="${7}"
EXCLUDE_LIST="${8}"

# Build find exclude options
EXCLUDE_ARGS=""
if [ -n "${EXCLUDE_LIST}" ]; then
  for item in ${EXCLUDE_LIST}; do
    EXCLUDE_ARGS="${EXCLUDE_ARGS} -path ${item} -prune -o"
  done
fi

# shellcheck disable=SC2086
find . ${EXCLUDE_ARGS} -type f \
  -exec sh -c '
    process_file() {
      file="${1}"
      temp_file="${file}.tmp"
      echo "Processing: ${file}"

      awk -v skip="${2}" \
        -v old_repo="${3}" -v new_repo="${4}" \
        -v old_owner="${5}" -v new_owner="${6}" \
        -v old_desc="${7}" -v new_desc="${8}" "
      NR <= skip {print; next}
      /templateskip|SPDX-FileCopyrightText/ {
        print; next
      }
      {
        gsub(old_repo, new_repo);
        gsub(old_owner, new_owner);
        gsub(old_desc, new_desc);
        print;
      }" "${file}" > "${temp_file}" && mv "${temp_file}" "${file}"
    }; process_file "$@"' _ {} "${SKIP_N_LINES}" \
    "${TEMPLATE_REPOSITORY}" "${REPOSITORY}" \
    "${TEMPLATE_OWNER}" "${OWNER}" \
    "${TEMPLATE_DESCRIPTION}" "${DESCRIPTION}" \;

echo "String replacements completed."
