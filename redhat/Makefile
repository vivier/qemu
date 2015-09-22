all: rh-help
include Makefile.common
include Makefile.test

LOCVERFILE:=../localversion
LANG=C
BUILD_DEFAULT_TARGET = rhevh-rhel-7.2-candidate
BUILD_SCRATCH_TARGET = rhevh-rhel-7.2-candidate

#ifeq ($(shell git diff --quiet HEAD && git describe --exact-match 2>/dev/null && echo ok),)
BUILD_TARGET ?= --scratch $(BUILD_SCRATCH_TARGET)
#else
#BUILD_TARGET ?= $(BUILD_DEFAULT_TARGET)
#endif

ifeq ($(NOWAIT),1)
  NOWAITFLAG=--nowait
endif

RHEV_FLAG=0
RELEASE:=$(shell sed -ne 's/^[^\#]*define release \(.*\)%.*%.*/\1/p' $(REDHAT)/$(SPECFILE).template)

# create an empty localversion file if you don't want a local buildid
ifneq ($(wildcard $(LOCVERFILE)),)
LOCALVERSION:=$(shell cat $(LOCVERFILE))
else
LOCALVERSION:=test
endif
ifneq ($(LOCALVERSION),)
BUILDID:=.$(LOCALVERSION)
$(info BUILDID is "$(BUILDID)". Update '$(shell dirname $(REDHAT))/localversion' to change.)
else
  ifneq ($(RCMARKER),)
     BUILDID:=.$(RCMARKER)
  endif
endif

# this section is needed in order to make O= and KBUILD_OUTPUT to work
ifeq ($(KBUILD_OUTPUT),)
ifeq ("$(origin O)", "command line")
  KBUILD_OUTPUT := $(O)
endif
ifeq ($(KBUILD_OUTPUT),)
  KBUILD_OUTPUT := $(REDHAT)/..
endif
endif

PKGRELEASE=$(PREBUILD)$(BUILD)
PKG_FULL_VR = $(STAMP_VERSION)-$(PKGRELEASE)$(DIST)$(BUILDID)
PKG_FULL_NVR = $(PKGNAME)-$(PKG_FULL_VR)

RPMBUILD_DEFS = --define "_sourcedir $(SOURCES)" --define "_builddir $(RPM)/BUILD" --define "_srcrpmdir $(RPM)/SRPMS" --define "_rpmdir $(RPM)/RPMS" --define "_specdir $(RPM)/SPECS" --define "dist $(DIST)"

default: rh-help

rh-clean-sources:
	@for i in $(SOURCES)/*; do \
		rm -f $$i; \
	done;


$(TARBALL):
	@if [ -n "$(TARURL)" ];then \
		echo "Downloading $(TARBALL) from $(TARURL)"; \
		wget -O $(TARBALL) $(TARURL) || exit; \
	else \
		echo "Creating archive $(TARBALL)"; \
		rm -f $(TARBALL); \
		scripts/kvm-make-release --formal $(MARKER) $(COMMON_NAME)-$(KVERSION) $(TARBALL); \
	fi

$(RC_PATCH):
	@if [ -n "$(RCREV)" ]; then \
		git diff $(COMMON_NAME)-$(KVERSION)..$(COMMON_NAME)-$(SUBLEVEL)-rc$(RCREV) | \
			gzip >$(REDHAT)/$(RC_PATCH); \
	fi

$(GIT_PATCH):
	@if [ -n "$(GITREV)" ]; then \
		git diff $(COMMON_NAME)-$(SUBLEVEL)-rc$(RCREV)..$(MARKER) | \
			gzip >$(REDHAT)/$(GIT_PATCH); \
	fi

setup-source: rh-clean-sources
	@cp $(REDHAT)/$(SPECFILE).template $(SOURCES)/$(SPECFILE)

sources-rh: $(TARBALL) $(RC_PATCH) $(GIT_PATCH) $(REDHAT)/create-patches.sh Makefile lastcommit
	@if [ -n "$(TARSHA1)" -a "$$(sha1sum < $(TARBALL) | cut -d' ' -f1)" != "$(TARSHA1)" ];then \
			echo "$(TARBALL) sha1sum does not match (expected: $(TARSHA1))" >&2; \
			exit 1; \
	fi
	@(if [ -n "$(RCREV)" ]; then \
		cp $(RC_PATCH) $(SOURCES)/; \
	fi)
	@(if [ -n "$(GITREV)" ]; then \
		cp $(GIT_PATCH) $(SOURCES)/; \
	fi)
	@touch $(TESTPATCH)
	@git diff --no-renames HEAD > $(TESTPATCH).tmp
	@diff $(TESTPATCH).tmp $(TESTPATCH) > /dev/null || \
		echo "WARNING: There are uncommitted changes in your tree or the changes are not in sync with the $(COMMON_NAME)-test.patch.  Either commit the changes or run 'make rh-test-patch'"
	@rm $(TESTPATCH).tmp
	@mkdir -p $(SOURCES)
	@cp $(TARBALL) $(SOURCES)/$(TARFILE)
	@cp $(TARBALL) $(SOURCES)/$(TARFILE)
	@cp *.patch $(SOURCES)
	@cp bridge.conf $(SOURCES)
	@$(REDHAT)/create-patches.sh $(MARKER) $(SOURCES) $(SOURCES)/$(SPECFILE) $(PKGRELEASE) '$(PREBUILD)' $(BUILD) $(RHEV_FLAG) $(BUILDID) $(RCMARKER)
	@cp $(SOURCES)/$(SPECFILE) $(SOURCES)/../SPECS
	@cp $(TESTPATCH) $(SOURCES)/$(COMMON_NAME)-test.patch
	@cp ../sysconfigs/target/target-x86_64.conf $(SOURCES)
	@cp Makefile.common $(SOURCES)/
	@cp $(EXTRA_SOURCES) $(SOURCES)/

rh-sources: setup-source sources-rh

rh-test-patch:
	git diff --no-renames HEAD > $(TESTPATCH);
	filterdiff -x '*redhat/*' -x '*/.gitignore' -x '*/makefile' $(TESTPATCH) >$(TESTPATCH).tmp;
	mv $(TESTPATCH).tmp $(TESTPATCH);

rh-all-rpms: rh-sources
	$(RPMBUILD) $(RPMBUILD_DEFS) --target $(MACH) -ba $(RPM)/SOURCES/$(SPECFILE)

rh-srpm: rh-sources
	$(RPMBUILD) $(RPMBUILD_DEFS) --nodeps -bs $(RPM)/SOURCES/$(SPECFILE)

rh-rpms: rh-sources
	$(RPMBUILD) $(RPMBUILD_DEFS) --target $(MACH) -bb $(RPM)/SOURCES/$(SPECFILE)

rh-$(COMMON_NAME)-%: rh-sources
	$(RPMBUILD) $(RPMBUILD_DEFS) --target $(MACH) --with $* --without vdso_install --with firmware -bb $(RPM)/SOURCES/$(SPECFILE)

rh-prep: rh-sources
	$(RPMBUILD) $(RPMBUILD_DEFS) --nodeps --target $(MACH) -bp $(RPM)/SOURCES/$(SPECFILE)

# we could just print the version number to stderr, but make dumps too much junk
# to stdout to make it usable, so a 'verrel' file is created
rh-verrel:
	@echo $(PKG_FULL_NVR) > verrel

# unless you know what you're doing, you don't want to use the next two ones
rh-release: rh-clean-sources
	@$(REDHAT)/scripts/new_release.sh $(KVERSION) $(BUILD) $(REDHAT)
	@make rh-srpm
	# this will be use the new BUILD definition from Makefile.common:
	@$(MAKE) rh-update-changelog

rh-release-commit:
	@git commit -s Makefile.common $(SPECFILE).template -m "[redhat] tagging $(PKG_FULL_VR)"
	@git tag $(PKG_FULL_NVR)
	@git log --max-count=1 --pretty=format:%H >$(REDHAT)/lastcommit;
	@git commit -s lastcommit -m "[redhat] updating lastcommit for $(PKG_FULL_VR)"

rh-update-changelog:
	@$(REDHAT)/scripts/update_changelog.sh $(KVERSION) $(PKG_FULL_VR)

.PHONY: rh-brew rh-koji rh-brew-ga rh-brew-ppc rh-brew-aarch64
rh-brew rh-brew-ppc rh-brew-aarch64 rh-brew-rhev rh-brew-rhev-autotest: BUILD_FLAGS ?= $(BREW_FLAGS) $(TEST_FLAGS)
rh-brew-ga: BUILD_SCRATCH_TARGET = rhel-7.2-candidate
rh-brew-ga rh-brew-ga-ppc: SPECFILE = $(GASPECFILE)
rh-brew-ga rh-brew-ga-ppc: PKGNAME = $(GAPKGNAME)
rh-brew-ga rh-brew-ga-ppc: BUILD = $(GABUILD)
rh-brew-aarch64: BREW_FLAGS += --arch-override=aarch64
rh-brew-ppc rh-brew-ga-ppc: BREW_FLAGS += --arch-override=ppc64le
rh-koji rh-koji-ga rh-koji-autotest: BUILD_FLAGS ?= $(KOJI_FLAGS) $(TEST_FLAGS)
rh-brew rh-brew-ppc rh-brew-aarch64 rh-brew-autotest rh-koji-autotest: RHEV_FLAG=1
rh-brew rh-brew-ppc rh-brew-aarch64 rh-brew-autotest rh-koji-autotest: PKG_FULL_NVR=$(PKGNAME)-rhev-$(PKG_FULL_VR)
rh-brew-ppc rh-brew-aarch64: rh-srpm
	brew build $(BUILD_FLAGS) $(BUILD_TARGET) $(NOWAITFLAG) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)
rh-brew rh-koji: rh-%: rh-srpm
	$* build $(BUILD_FLAGS) $(BUILD_TARGET) $(NOWAITFLAG) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)
rh-brew-ga rh-koji-ga: rh-%-ga: rh-srpm
	$* build $(BUILD_FLAGS) $(BUILD_TARGET) $(NOWAITFLAG) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)
rh-brew-ga-ppc: rh-srpm
	brew build $(BUILD_FLAGS) $(BUILD_TARGET) $(NOWAITFLAG) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)
rh-brew-autotest rh-koji-autotest: rh-%-autotest: rh-srpm
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)" "autotest"
rh-brew-covscan rh-koji-covscan: rh-%-covscan: rh-srpm
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)" "coverity"
rh-brew-at-covscan rh-koji-at-covscan: rh-%-at-covscan: rh-srpm
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)" "autotest-coverity"

rh-help:
	@echo  'Cleaning targets:'
	@echo  '  rh-clean-sources    - Clean the redhat/rpm/SOURCES/ directory'
	@echo  ''
	@echo  'Building targets:'
	@echo  ' All RPM/SRPM files will be put under the redhat/rpm/ directory'
	@echo  ''
	@echo  '  rh-srpm                 - Create a source RPM and put it into the redhat/rpm/SRPMS/ directory'
	@echo  '  rh-brew                 - Create a $(COMMON_NAME)-rhev SRPM and then call brew to build the created SRPM'
	@echo  '  rh-brew-covscan         - Create a $(COMMON_NAME)-rhev RPMs on brew and then send directly to coverity scan testing'
	@echo  '  rh-brew-autotest        - Create a $(COMMON_NAME)-rhev RPMs on brew and then send directly to autotest server'
	@echo  '  rh-brew-at-covscan      - Create a $(COMMON_NAME)-rhev RPMs on brew and then send directly to autotest and coverity testing'
	@echo  '  rh-brew-ga              - Build guest-agent rpm using brew'
	@echo  '  rh-brew-ga-ppc          - Build guest-agent rpm for ppc64le using brew'
	@echo  '  rh-brew-ppc             - Build qemu-kvm-rhev for ppc64le using brew'
	@echo  '  rh-brew-aarch64         - Build qemu-kvm-rhev for aarch64 using brew'
	@echo  '  rh-koji                 - Create a $(COMMON_NAME)-rhev SRPM and then call koji to build the created SRPM'
	@echo  '  rh-brew-covscan         - Create a $(COMMON_NAME)-rhev RPMs on koji and then send directly to coverity scan testing'
	@echo  '  rh-brew-autotest        - Create a $(COMMON_NAME)-rhev RPMs on koji and then send directly to autotest server'
	@echo  '  rh-brew-at-covscan      - Create a $(COMMON_NAME)-rhev RPMs on koji and then send directly to autotest and coverity testing'
	@echo  '  rh-koji-ga              - Build guest-agent rpm using koji'
	@echo  '  rh-$(COMMON_NAME)-<type> 	- Create  binary RPMS for a particular $(COMMON_NAME) type'
	@echo  '                   	- <type> can be: baseonly, smponly, dbgonly'
	@echo  '  rh-all-rpms		- Create the binary RPMS and the SRPM for the $(COMMON_NAME)'
	@echo  '  rh-prep		- Setup the redhat/rpm/BUILD/ directory with the $(COMMON_NAME) source'
	@echo  '  rh-test-patch 	- Create a diff against HEAD and put it in $(COMMON_NAME)-test.patch.'
	@echo  '                  	  Then $(COMMON_NAME)-test.patch will be added to the $(COMMON_NAME) build'
