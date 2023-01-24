function to_json_list() {
  for item in $@; do
    str+="\"$item\", "
  done
  echo "[${str%, }]"
}

PYTHON_VERSIONS="$@"
JSON="$(to_json_list ${PYTHON_VERSIONS})"
echo "{PYTHON_VERSIONS}=${JSON}" >>$GITHUB_ENV
