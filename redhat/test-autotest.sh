#!/bin/bash

space="rhel70-brew"
label="auto-rhel7"

if [ ! -x /usr/bin/autotest-rpc-client ]; then
	echo "ERROR: Cannot find autotest-rpc-client executable in your /usr/bin directory"
	exit 1
fi

if [ -z "$1" ]; then
	echo "Syntax: $0 server brew_build_id [space is $space]"
	exit 1
fi

server="$1"
task_id="$2"

wget -O test.tmp --no-check-certificate "https://brewweb.devel.redhat.com/taskinfo?taskID=$task_id" > /dev/null 2> /dev/null
task=$(cat test.tmp | grep "<h4>Information for task <a href=" | awk '{ split($0, a, ">"); split(a[3], b, "<"); split(b[1], c, "("); split(c[2], d, ","); gsub(/.src.rpm)/, "", d[2]); print d[2] }')

var=""
echo $task | grep rhev > /dev/null
if [ $? -eq 0 ]; then
        var="-rhev"
fi

if [[ "$task" == *rpms/* ]]; then
	task="official $(cat test.tmp | grep buildArch | awk '{split($0, a, "buildArch"); split(a[2], b, "("); split(b[2], c, ","); gsub(/.src.rpm/, "", c[1]); if (NR == 1) print c[1] }')"
fi

ping -c1 $server
/usr/bin/autotest-rpc-client job create -w $server -B never -a never -s -e $(cat ./at-control.mails) -f ./at-control$var.template -T --timestamp -m "1*$label" -x "only $space..sanity" -x "koji_qemu_kvm_build=$task_id" "RHEL 7 $task sanity"
/usr/bin/autotest-rpc-client job create -w $server -B never -a never -s -e $(cat ./at-control.mails) -f ./at-control-hugepages$var.template -T --timestamp -m "1*$label" -x "only $space..sanity" -x "koji_qemu_kvm_build=$task_id" "RHEL 7 $task (hugepages) sanity"

echo "Autotest jobs submitted"
