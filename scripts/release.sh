#!/bin/sh

set -eux

curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/saturday06/VRM-Addon-for-Blender/releases/tags/${RELEASE_TAG_NAME}"
