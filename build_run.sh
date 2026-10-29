#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

log=$(mktemp)
if ! docker compose build --progress=plain 2>&1 | tee "$log" | awk '
    /^#[0-9]+ \[[0-9]+\/[0-9]+\]/ && !seen[$2]++ {
        split(substr($2, 2, length($2) - 2), p, "/")
        printf "\r\033[KBuilding %3d%%\n", (p[1] - 1) * 100 / p[2]
        fflush()
    }
    /^#[0-9]+ [0-9.]+ / {
        line = $0
        sub(/^#[0-9]+ [0-9.]+ /, "", line)
        printf "\r\033[K    %s", substr(line, 1, 90)
        fflush()
    }
    END { printf "\r\033[K" }'; then
    echo "Build failed. Last lines:" >&2
    tail -n 30 "$log" >&2
    rm -f "$log"
    exit 1
fi
rm -f "$log"

echo "Building 100%"
echo "Running..."
exec ./run.sh "$@"