#!/usr/bin/env bash

# SPDX-FileCopyrightText: © 2026 open-nudge <https://github.com/open-nudge>
# SPDX-FileContributor: szymonmaszke <github@maszke.co>
#
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

gh api --method PATCH "repos/{owner}/{repo}" \
    -f "security_and_analysis[advanced_security][status]=enabled" \
    -f "security_and_analysis[secret_scanning][status]=enabled" \
    -f "security_and_analysis[secret_scanning_ai_detection][status]=enabled" \
    -f "security_and_analysis[secret_scanning_push_protection][status]=enabled" \
    -f "security_and_analysis[secret_scanning_non_provider_patterns][status]=enabled"
