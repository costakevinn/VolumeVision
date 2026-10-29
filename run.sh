#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

profile="profiles/${1:-local}.yml"
[ -f "$profile" ] || { echo "Missing $profile. Copy one of profiles/*.yml.example to it." >&2; exit 1; }
[ -f models/hand_landmarker.task ] || curl -fsSL --create-dirs -o models/hand_landmarker.task \
    https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

export HOST_UID="$(id -u)" HOST_GID="$(id -g)"

exec docker compose -f docker-compose.yml -f "$profile" run --rm --service-ports app