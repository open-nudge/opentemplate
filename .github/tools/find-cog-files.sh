#!/usr/bin/env sh

# SPDX-FileCopyrightText: © 2025 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

# Find all files with cog tags in a directory
# This list is later used to provide a list of files to update
# in pyproject.toml fix-generation and check-generation
DIRECTORY="${1:-.}"

find "${DIRECTORY}" -type f -exec grep -l '\[\[\[cog' {} +
