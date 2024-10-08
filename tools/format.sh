#!/bin/sh

set -eux

cd "$(dirname "$0")/.."

git ls-files "*.py" "*.pyi" | xargs uv run ruff format
git ls-files "*.py" "*.pyi" | xargs uv run ruff check --fix
git ls-files "*.sh" | xargs shfmt -w -s
npm exec --yes -- prettier --write .
