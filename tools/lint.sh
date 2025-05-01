#!/bin/sh

set -eux

cd "$(dirname "$0")/.."

git ls-files "*.sh" | xargs shellcheck
git ls-files "*.py" "*.pyi" | xargs uv run ruff check
git ls-files "*.py" "*.pyi" | xargs uv run codespell
git ls-files "*.py" "*.pyi" | xargs uv run mypy --show-error-codes
git ls-files "*.sh" | xargs shfmt -d -s
npm install
uv run ./node_modules/.bin/pyright --warnings
npm exec --yes -- prettier --check .
