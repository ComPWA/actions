function to_json_list() {
  local separator=' <->'
  result=$(printf "%s" "$separator" "${@/#/$separator}")
  echo '["'${result}'"]'
}

PYTHON_VERSIONS="$@"
JSON="$(to_json_list ${PYTHON_VERSIONS}})"
echo "PYTHON_VERSIONS=${JSON}"
echo "{PYTHON_VERSIONS}=${JSON}" >>$GITHUB_ENV
