#!/bin/bash

# Autotest server location
AT_SERVER="autotest-virt.virt.bos.redhat.com"

cmd="$1"
typ="$2"

if [ -z "$cmd" ]; then
	echo "ERROR: Command not specified"
	echo "Syntax: $0 command type"
	echo
	echo "where type can be:"
	echo "  autotest          - send resulting task to autotest-grid"
	echo "  coverity          - send resulting task to coverity scan"
	echo "  autotest-coverity - send resulting task to both autotest-grid and coverity scan"
	echo
	exit 1
fi

task_id=$($cmd | grep "Created task:" | awk '{ split($0, a, ": "); print a[2] }')
brew watch-task $task_id

echo "Task ID seems to be $task_id."

if [ "$typ" == "autotest" ]; then
	./test-autotest.sh $AT_SERVER $task_id
elif [ "$typ" == "coverity" ]; then
	./test-covscan.sh $task_id
elif [ "$typ" == "autotest-coverity" ]; then
	./test-covscan.sh $task_id
	./test-autotest.sh $AT_SERVER $task_id
else
	echo "ERROR: Incorrect type!"
	exit 1
fi
