#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1 && pwd)"

python3 ${dir}/../finance/__main__.py $@