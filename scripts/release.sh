#!/bin/sh

set -eux

if ! curl \
    --fail \
    --show-error \
    --location \
    --output release.json \
    --header "Accept: application/vnd.github+json" \
    --header "Authorization: Bearer ${GITHUB_TOKEN}" \
    --header "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/releases/tags/${RELEASE_TAG_NAME}"; then

  cat release.json
  exit 1
fi

cat release.json
