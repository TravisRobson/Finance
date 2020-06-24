#!/usr/bin/env bash

set -o errexit -o pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1 && pwd)"
root_dir="$(cd ${dir}/.. > /dev/null 2>&1 && pwd)"

export PYTHONPATH=$PYTHONPATH:${root_dir}/finance

python3 ${root_dir}/finance/__main__.py $@
