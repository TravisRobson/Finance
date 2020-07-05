# Finance

[![Build](https://github.com/TravisRobson/Finance/workflows/Python%20application/badge.svg?branch=master&event=push)](https://github.com/TravisRobson/Finance/actions?query=workflow%3A%22Build%22)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A simple program to estimate when my student loans will be payed off. 
Allowing the user to twiddle with how much they pay and when they pay extra. 
Including multiple payment strategies such as strictly minimum payments or 
minimum payment as well as paying extra on highest interest loans first 
(the optimal allocation of your payments).

To run the CLI
```bash
./bin/finance.sh <options>
```
where you can pass the option `--help` to see your options.

## Goals

I would like expand this application past student loan payments. I would like to estimate
total post-tax income, depending on your work benefits, estimate status of re tirement goals,
see how your financial situation changes in different states.

## Developers

Activate a local virtual environment and install requirements
```bash
python3 -m venv <venv-name>
source <venv-name>/bin/activate
pip install -r requirements.txt
```

To deactivate `$ deactivate`.

To run the test suite execute
```bash
./bin/runTests.sh
```

