#!/usr/bin/env bash

ROOT="${1:-.}"
OUT_FILE="${2:-poetry-modules.json}"
IGNORE_TESTS=true
EXCLUDE_CORE=true

echo "[" >"${OUT_FILE}"
first=1

find "${ROOT}" -type f -name pyproject.toml | while read -r T; do
	DIR=$(dirname "${T}")

	META=$(python3 -c "
import toml, json
try:
    data = toml.load('${T}')
    tool = data['tool']['poetry']
    name = tool['name']
    if name == 'haive-core' and ${EXCLUDE_CORE}:
        raise SystemExit(0)
    pkgs = tool.get('packages', [])
    for p in pkgs:
        if 'include' in p and 'from' in p:
            print(json.dumps({
                'name': name,
                'version': tool.get('version'),
                'description': tool.get('description'),
                'pkg_root': '${DIR}/' + p['from'],
                'pkg_name': p['include'],
            }))
except:
    pass
")

	[[ -z ${META} ]] && continue

	PKG_NAME=$(echo "${META}" | jq -r '.pkg_name')
	PKG_ROOT=$(echo "${META}" | jq -r '.pkg_root')
	FULL_PATH="${PKG_ROOT}/$(echo "${PKG_NAME}" | tr . /)"

	[[ ! -d ${FULL_PATH} ]] && continue

	MODULES=$(find "${FULL_PATH}" -type f -name "*.py" |
		grep -v "__pycache__" |
		([[ ${IGNORE_TESTS} == true ]] && grep -vE "(test_|tests/)") |
		sed "s|${PKG_ROOT}/||" |
		sed "s|\.py\$||" |
		sed "s|/|.|g" |
		sort -u |
		jq -R . | jq -s .)

	[[ ${first} -eq 0 ]] && echo "," >>"${OUT_FILE}"
	first=0

	echo "${META}" | jq --argjson modules "${MODULES}" '. + {modules: $modules}' >>"${OUT_FILE}"
done

echo "]" >>"${OUT_FILE}"
echo "✅ Saved compressed poetry module tree to${ $OUT_FI}LE"
