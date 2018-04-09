#!/bin/bash
set -e
if [ "$MODE" = 'UNIT' ]; then
	echo "Running unit tests"
	exec python "/ipcalculator/unit_test.py"
else
	echo "Running production"
	exec python "/ipcalculator/calculator.py"
fi
