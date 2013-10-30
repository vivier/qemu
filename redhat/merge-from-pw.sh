#!/bin/bash

MASTER="7.0"
REPOBASE="/home/patchwork/git/qemu-kvm-rhel"
BRANCHBASE="rhel"
REPORT_EMAIL="minovotn@redhat.com mrezanin@redhat.com"

# Activate Kerberos 5 keytab
/home/patchwork/activate-keytab.sh > /dev/null

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

branchname="$BRANCHBASE$r"
if [ "$1" == "$MASTER" ]; then
	branchname="$BRANCHBASE$rver"
fi

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

export BUILD_TEST_SCRIPTED=1

if [ "$failed" -eq 0 -a "$applied" -gt 0 ]; then
        tmpFileR="$(mktemp)"

        make -C redhat rh-brew-at-covscan LOCALVERSION="automergetest" | egrep 'Task ID seems to be|\(id |New Coverity test job has been created:' | awk '{ if (match($0, "seems") != 0) { split($0, a, "be "); gsub(/\./, "", a[2]); print "Brew ID: "a[2] }; if (match($0, "id") != 0) { split($0, a, "id "); gsub(/)\047/, "", a[2]); print "Autotest job ID: "a[2] }; if (match($0, "Coverity test job has been created:") != 0) { split($0, a, ": "); split(a[2], b, " ."); print "Coverity job ID: "b[1] } }' 2> /dev/null > test.tmp

        echo "Hi," > $tmpFileR
        echo "these are test results for automatic mergetest build." >> $tmpFileR
        echo "Relevant identifiers are:" >> $tmpFileR
        echo >> $tmpFileR
        cat test.tmp >> $tmpFileR
        echo >> $tmpFileR
        cat /home/patchwork/public_reports/qemu-kvm-RHEL-6.5/short_report.txt  | grep PATCH | awk '{ split($0, a, " "); if (a[1] != "123456") { if (match(a[5], "N") == 0) print $0 } }' >> $tmpFileR
        echo >> $tmpFileR
        echo "All patches on queue ($applied) were applied successfully" >> $tmpFileR

        for addr in ${REPORT_EMAIL[@]}
        do
                cat $tmpFileR | mail -s "[PATCHWORK] Automergetest results for qemu-kvm-rhel$rver" $addr
        done

        rm -f $tmpFileR
fi

rm -f $tmpFile

git checkout $branchname/master-1.5.3 > /dev/null 2>&1
cd $oldPath
