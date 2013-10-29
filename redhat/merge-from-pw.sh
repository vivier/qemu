#!/bin/bash

MASTER="7.0"
REPOBASE="/home/patchwork/git/qemu-kvm-rhel"
BRANCHBASE="rhel"
REPORT_EMAIL="minovotn@redhat.com"

if [ "x$1" == "x" ]; then
	echo "Syntax: $0 version"
	echo "Example: $0 7.0"
	exit 1
fi

rver=$(echo $1 | awk '{ print substr($0, 1, 1); }')

VER="$1"

if [ ! -f "/home/patchwork/public_reports/qemu-kvm-RHEL-$VER/short_report.txt" ]; then
	echo "Error: Invalid target"
	exit 1
fi

oldPath="$(pwd)"
tmpFile="$(mktemp)"

rpath="$REPOBASE$rver"

if [ ! -d "$rpath" ]; then
	echo "Error: Repository path $rpath doesn't exist"
	exit
fi

r=$(echo $1 | tr -d ".0")

if [ "$1" == "$MASTER" ]; then
	branchname="$BRANCHBASE$rver"
fi

branchname="$BRANCHBASE$r"

# Server path
cd $rpath
git checkout $branchname/master-1.5.3 > /dev/null 2>&1
git pull > /dev/null 2>&1
git branch -D $branchname/mergetest > /dev/null 2>&1
git checkout -b $branchname/mergetest > /dev/null 2>&1

failed=0
applied=0
pwids=$(cat /home/patchwork/public_reports/qemu-kvm-RHEL-$VER/short_report.txt  | grep PATCH | awk '{ split($0, a, " "); if (a[1] != "123456") print a[2] }')
for pwid in ${pwids[@]}
do
	pjw patch apply $pwid >> $tmpFile 2>&1
	if [ "$?" -eq 0 ]; then
		let applied=$applied+1
	else
		let failed=$failed+1
	fi
done

if [ $failed -gt 0 ]; then
	for addr in ${REPORT_EMAIL[@]}
	do
		(
		echo "Results from $(date): $failed failed, $applied applied"
		echo
		echo "Output of 'pjw patch apply':"
		cat $tmpFile
		) | mail -s "[PATCHWORK] Repository test failed: qemu-kvm-rhel$rver" $addr
	done
fi

if [ "$failed" -eq 0 -a "$applied" -gt 0 ]; then
	make -C redhat rh-brew-at-covscan LOCALVERSION=".automergetest"
fi

rm -f $tmpFile

git checkout $branchname/master-1.5.3 > /dev/null 2>&1
cd $oldPath
