#!/usr/bin/env bash
set -euo pipefail

FILE="CHANGELOG.md"
TMP="CHANGELOG.cleaned.md"

# 1. Keep the first occurrence of the "Changelog" header + preamble
awk '
  BEGIN {
    seen_header = 0
  }
  /^# Changelog/ {
    if (seen_header) {
      skip=1
      next
    } else {
      seen_header=1
      skip=0
    }
  }
  /^---$/ {
    if (seen_header && ++divider > 1) {
      # second or later divider (preamble duplicated) -> skip
      skip=1
      next
    }
  }
  {
    if (!skip) print
  }
' "$FILE" > "$TMP"

mv "$TMP" "$FILE"
