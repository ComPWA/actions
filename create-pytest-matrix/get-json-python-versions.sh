function to_json_list() {
  local separator=' <->'
  result=$(printf "%s" "$separator" "${@/#/$separator}")
  echo '["'${result}'"]'
}
python_versions="$(to_json_list ${{ inputs.python-versions }})"
echo "PYTHON_VERSIONS=${python_versions}"
echo "{PYTHON_VERSIONS}=${python_versions}" >> $GITHUB_ENV
