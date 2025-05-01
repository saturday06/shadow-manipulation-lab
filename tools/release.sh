#!/bin/sh

set -eux

gh release edit "$RELEASE_TAG_NAME" --draft=false --latest
