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

  if git ls-files \
    ':(exclude)tools/*.sh' \
    ':(exclude)tools/*.py' \
    ':(exclude)src/shadow_manipulation_lab/development_support/restart.sh' \
    --stage | grep -Ev '^100644[[:space:]]'; then
    echo "Some files have executable permission but shouldn't have."
    exit 1
  fi

  if git ls-files \
    'tools/*.sh' \
    'tools/*.py' \
    'src/shadow_manipulation_lab/development_support/restart.sh' \
    --stage | grep -Ev '^100755[[:space:]]'; then
    echo "Some files have no executable permission."
    exit 1
  fi
)

cd "$(dirname "$0")/.."

validate_file_name_characters
validate_permissions
uv run python -c "import shadow_manipulation_lab; shadow_manipulation_lab.register(); shadow_manipulation_lab.unregister()"
git ls-files -z "*.sh" | xargs -0 shellcheck
git ls-files -z "*.py" "*.pyi" | xargs -0 uv run ruff check
uv run codespell
git ls-files -z "*.sh" | xargs -0 shfmt -d
deno lint
deno task pyright
: ----- OK ----- : +
