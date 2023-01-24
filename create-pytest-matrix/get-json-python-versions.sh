function joinByString() {
  # https://dev.to/meleu/how-to-join-array-elements-in-a-bash-script-303a
  local separator="$1"
  shift
  local first="$1"
  shift
  printf "%s" "$first" "${@/#/$separator}"
}

SEPARATOR='", "'
PYTHON_VERSIONS="$@"
JSON="$(joinByString ${SEPARATOR} ${PYTHON_VERSIONS}})"
echo "PYTHON_VERSIONS=${JSON}"
echo "{PYTHON_VERSIONS}=${JSON}" >>$GITHUB_ENV
