#!/bin/bash

# Autotest server location
AT_SERVER="autotest-virt.virt.bos.redhat.com"

cmd="$1"

if [ -z "$cmd" ]; then
	echo "ERROR: Command not specified"
	exit 1
fi

task_id=$($cmd | grep "Created task:" | awk '{ split($0, a, ": "); print a[2] }')
brew watch-task $task_id

echo "Task ID seems to be $task_id."
./autotest.sh $AT_SERVER $task_id
