#!/bin/bash

prefix="/usr"
sysconfdir="/etc"
filename="qemu-kvm.spec.template"
binname="x86_64-softmmu/qemu-system-x86_64"

function get_core_count()
{
	max=0
	for i in $(ls /dev/cpu)
	do
		let id=$i+0

		if [ $id -gt $max ]; then
			max=$id
		fi
	done

	echo $max
}

function get_configure()
{
	local fn="$1"

	sln=$(grep -n "./configure" "$fn" | awk '{ split($0, a, ":"); print a[1] }')
	if [ -z $sln ]; then
		return
	fi

	while [ 1 ]; do
		str=$sln"p"
		line=$(sed -n $str "$fn")
		echo $line | tr -d '\\'

		if [ "${#line}" -eq 0 ]; then
			break
		fi

		let sln=$sln+1
	done
}

cfg=$(get_configure "$filename")
cfg=${cfg/\%\{fake_machine_arg\}/}
cfg=${cfg/\%\{disable_rhev_features_arg\}/}
cfg=${cfg/\%\{_prefix\}/$prefix}
cfg=${cfg/\%\{_sysconfdir\}/$sysconfdir}
cfg=${cfg/\$RPM_OPT_FLAGS/-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic}
cfg=${cfg/\$extraldflags/-Wl,--build-id -pie -Wl,-z,relro -Wl,-z,now}

let j=$(get_core_count)+1

cd ..
eval $cfg

if [ $? -ne 0 ]; then
	echo "ERROR: Cannot run configure"
	exit 1
fi

make -j $j

if [ ! -x "$binname" ]; then
	echo "ERROR: Cannot compile"
	exit 1
fi

echo "File $binname written"
