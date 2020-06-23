#!/usr/bin/env bash

set -o errexit -o pipefail

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null 2>&1 && pwd)"

export PYTHONPATH=$PYTHONPATH:finance/

pytest -v tests 