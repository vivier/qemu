UPSTREAM_NAME=$1
MARKER=$2
NAME=$3
VERSION=$4
LOCALVERSION=$5
SOURCES=rpmbuild/SOURCES
SPEC=rpmbuild/SPECS/${NAME}.spec
BUILDIR=rpmbuild/BUILD/${UPSTREAM_NAME}-${MARKER}
SRPMDIR=rpmbuild/SRPMS
TARBALL=${UPSTREAM_NAME}-${MARKER}.tar.bz2
SOURCE_FILES="qemu.binfmt 80-kvm.rules ksm.service ksm.sysconfig ksmctl.c ksmtuned.service ksmtuned ksmtuned.conf qemu-guest-agent.service 99-qemu-guest-agent.rules bridge.conf qemu-ga.sysconfig"
START_TAG=${UPSTREAM_NAME}-${MARKER}

# Pre-cleaning
rm -rf .tmp asection psection patchlist
rm -rf ${BUILDIR} ${SPEC} ${SOURCES}/* SRPMDIR/*

# Handle sources
if [ -n "${SOURCE_FILES}" ]; then
  cp ${SOURCE_FILES} ${SOURCES}
fi

# Handle sources
if [ ! -f ${TARBALL} ]; then
    wget http://wiki.qemu.org/download/${TARBALL}
fi
cp ${TARBALL} ${SOURCES}/${TARBALL}

# Handle patches
git format-patch --first-parent --no-renames --no-binary -k ${START_TAG}.. > patchlist
for patchfile in `cat patchlist`; do
  ./frh.py ${patchfile} > .tmp
  if grep -q '^diff --git ' .tmp; then
     num=$(echo ${patchfile} | sed 's/\([0-9]*\).*/\1/')
     echo "Patch$num: ${patchfile}" >> psection
     echo "%patch$num -p1" >> asection
     mv .tmp ${SOURCES}/${patchfile}
  fi
done

# Handle spec file
cp ${NAME}.spec.template ${SPEC}

sed -i -e "/%%PATCHLIST%%/r psection
           /%%PATCHLIST%%/d
           /%%PATCHAPPLY%%/r asection
           /%%PATCHAPPLY%%/d
           s/%%UPSTREAMVERSION%%/${MARKER}/
           s/%%VERSION%%/${VERSION}/
           s/%%LOCALVERSION%%/${LOCALVERSION}/" ${SPEC}

# Final cleaning
rm -rf `cat patchlist` 
rm -rf .tmp asection psection patchlist
