#!/bin/bash
# SPDX-License-Identifier: MIT OR GPL-3.0-or-later

set -eux -o pipefail

validate_file_name_characters() (
  set +x

  git ls-files -z | while IFS= read -r -d '' f; do
    encoding=$(echo "$f" | uchardet)
    if [ "$encoding" != "ASCII" ]; then
      echo "$f is not ascii file name but $encoding."
      exit 1
    fi
  done

  git ls-files -z "*.py" "*.pyi" | while IFS= read -r -d '' f; do
    if [ "$f" != "$(echo "$f" | LC_ALL=C tr "[:upper:]" "[:lower:]")" ]; then
      echo "$f contains uppercase character"
      exit 1
    fi
  done
)

validate_permissions() (
  set +x

  git ls-files -z ':!tools/*.sh' ':!tools/*.py' ':!tests/resources' ':!typings' | while IFS= read -r -d '' f; do
    if [ -x "$f" ]; then
      echo "$f has unnecessary executable permission."
      exit 1
    fi
  done
  git ls-files -z 'tools/*.sh' 'tools/*.py' | while IFS= read -r -d '' f; do
    if [ ! -x "$f" ]; then
      echo "$f has no executable permission."
      exit 1
    fi
  done
)

cd "$(dirname "$0")/.."

validate_file_name_characters
uv run python -c "import shadow_manipulation_lab; shadow_manipulation_lab.register(); shadow_manipulation_lab.unregister()"
git ls-files -z "*.sh" | xargs -0 shellcheck
git ls-files -z "*.py" "*.pyi" | xargs -0 uv run ruff check
uv run codespell
git ls-files -z "*.sh" | xargs -0 shfmt -d
git ls-files -z "*/Dockerfile" "*.dockerfile" | xargs -0 hadolint
deno lint
deno task pyright
validate_permissions
