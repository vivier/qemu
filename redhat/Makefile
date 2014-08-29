all: rh-help
UPSTREAM_NAME=qemu
UPSTREAM_VERSION=2.1.0
NAME=qemu-kvm
VERSION=1
DIST=.el7

REDHAT:=$(shell pwd)
LOCALVERSION:=$(shell cat localversion 2>/dev/null)
ifeq (${LOCALVERSION},)
  LOCALVERSION:=$(shell cat ../localversion 2>/dev/null)
  ifeq (${LOCALVERSION},)
    LOCALVERSION=.test
  endif
endif

.PHONY: rh-brew rh-srpm rh-prep rh-help
rh-prep:
	${REDHAT}/process-rh-specific.sh ${UPSTREAM_NAME} ${UPSTREAM_VERSION} ${NAME} ${VERSION} ${LOCALVERSION}

rh-srpm: rh-prep
	rpmbuild --define "_sourcedir ${REDHAT}/rpmbuild/SOURCES" --define "_builddir ${REDHAT}/rpmbuild/BUILD" --define "_srcrpmdir ${REDHAT}/rpmbuild/SRPMS" --define "_rpmdir ${REDHAT}/rpmbuild/RPMS" --define "_specdir ${REDHAT}/rpmbuild/SPECS" --define "dist ${DIST}" --nodeps -bs rpmbuild/SPECS/${NAME}.spec

rh-brew: rh-srpm
	brew build --scratch rhel-7.1-candidate rpmbuild/SRPMS/${NAME}-${UPSTREAM_VERSION}-${VERSION}${DIST}${LOCALVERSION}.src.rpm

rh-help:
	@echo "rh-brew: Build package on brew"
	@echo "rh-srpm: Prepare srpm package"
	@echo "rh-prep: Prepare sources and spec file in rpmbuild/"
	@echo "rh-help: Print this help"
