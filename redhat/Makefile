all: rh-help
include Makefile.common
include Makefile.test

LOCVERFILE:=../localversion
LANG=C
BUILD_DEFAULT_TARGET = rhel-7.6-candidate
BUILD_SCRATCH_TARGET = rhel-7.6-candidate

#ifeq ($(shell git diff --quiet HEAD && git describe --exact-match 2>/dev/null && echo ok),)
BUILD_TARGET ?= --scratch $(BUILD_SCRATCH_TARGET)
#else
#BUILD_TARGET ?= $(BUILD_DEFAULT_TARGET)
#endif

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

rh-configs:
	cd $(REDHAT)/configs; $(MAKE) VERSION=$(KVERSION) configs

rh-configs-prep:
	cd $(REDHAT)/configs; $(MAKE) VERSION=$(KVERSION) O=$(KBUILD_OUTPUT) configs-prep

rh-clean-configs:
	cd $(REDHAT)/configs; $(MAKE) VERSION=$(KVERSION) clean

rh-clean-sources:
	@for i in $(SOURCES)/*; do \
		rm -f $$i; \
	done;

rh-pull-configs:
	cd $(REDHAT)/configs; $(MAKE) VERSION=$(KVERSION) pull-configs

rh-key:
	echo "Creating a new module signing key...";
	@cd $(KBUILD_OUTPUT); \
	/sbin/rngd -r /dev/urandom; \
	gpg --homedir . --batch --gen-key $(REDHAT)/genkey; \
	if [ -s $(REDHAT)/extrakeys.pub ]; then \
		gpg --homedir . --no-default-keyring --keyring $(COMMON_NAME).pub --import $(REDHAT)/extrakeys.pub; \
	fi; \
	gpg --homedir . --export --keyring $(COMMON_NAME).pub Red > extract.pub; \
	mkdir -p crypto/signature/ scripts/; \
	gcc -o scripts/bin2c $(REDHAT)/../scripts/bin2c.c; \
	scripts/bin2c ksign_def_public_key __initdata < extract.pub >crypto/signature/key.h;

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
	@$(REDHAT)/create-patches.sh $(MARKER) $(SOURCES) $(SOURCES)/$(SPECFILE) $(PKGRELEASE) '$(PREBUILD)' $(BUILD) $(RHEV_FLAG) $(BUILDID) 
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

.PHONY: rh-brew rh-koji rh-brew-rhev
rh-brew rh-brew-rhev rh-brew-rhev-autotest: BUILD_FLAGS ?= $(BREW_FLAGS) $(TEST_FLAGS)
rh-koji rh-koji-rhev rh-koji-rhev-autotest: BUILD_FLAGS ?= $(KOJI_FLAGS) $(TEST_FLAGS)
rh-brew-rhev rh-brew-rhev-autotest rh-koji-rhev-autotest: RHEV_FLAG=1
rh-brew-rhev rh-brew-rhev-autotest rh-koji-rhev-autotest: PKG_FULL_NVR=$(PKGNAME)-rhev-$(PKG_FULL_VR)
rh-brew rh-koji: rh-%: rh-srpm
	$* build $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)
rh-brew-rhev rh-koji-rhev: rh-%-rhev: rh-srpm
	$* build $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)
rh-brew-autotest rh-koji-autotest: rh-%-autotest: rh-srpm
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)" "autotest"
rh-brew-rhev-autotest rh-koji-rhev-autotest: rh-%-rhev-autotest: rh-srpm-rhev
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET_RHEV) $(SRPMS)/$(PKG_FULL_NVR_RHEV).src.rpm $(OUTPUT_FILE)" "autotest"
rh-brew-covscan rh-koji-covscan: rh-%-covscan: rh-srpm
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)" "coverity"
rh-brew-rhev-covscan rh-koji-rhev-covscan: rh-%-rhev-covscan: rh-srpm-rhev
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET_RHEV) $(SRPMS)/$(PKG_FULL_NVR_RHEV).src.rpm $(OUTPUT_FILE)" "coverity"
rh-brew-at-covscan rh-koji-at-covscan: rh-%-at-covscan: rh-srpm
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET) $(SRPMS)/$(PKG_FULL_NVR).src.rpm $(OUTPUT_FILE)" "autotest-coverity"
rh-brew-rhev-at-covscan rh-koji-rhev-at-covscan: rh-%-rhev-at-covscan: rh-srpm-rhev
	./schedule-tests.sh "$* build --nowait $(BUILD_FLAGS) $(BUILD_TARGET_RHEV) $(SRPMS)/$(PKG_FULL_NVR_RHEV).src.rpm $(OUTPUT_FILE)" "autotest-coverity"

rh-help:
	@echo  'Cleaning targets:'
	@echo  '  rh-clean-sources    - Clean the redhat/rpm/SOURCES/ directory'
	@echo  '  rh-clean-configs    - Clean the redhat/configs/ directory'
	@echo  ''
	@echo  'Building targets:'
	@echo  ' All RPM/SRPM files will be put under the redhat/rpm/ directory'
	@echo  ''
	@echo  '  rh-srpm		- Create a source RPM and put it into the redhat/rpm/SRPMS/ directory'
	@echo  '  rh-brew		- Create a $(COMMON_NAME) SRPM and then call brew to build the created SRPM'
	@echo  '  rh-brew-covscan         - Create a $(COMMON_NAME) RPMs on brew and then send directly to coverity scan testing'
	@echo  '  rh-brew-autotest        - Create a $(COMMON_NAME) RPMs on brew and then send directly to autotest server'
	@echo  '  rh-brew-at-covscan      - Create a $(COMMON_NAME) RPMs on brew and then send directly to autotest and coverity testing'
	@echo  '  rh-brew-rhev            - Create a $(COMMON_NAME)-rhev SRPM and then call brew to build the created SRPM'
	@echo  '  rh-brew-rhev-covscan    - Create a $(COMMON_NAME)-rhev RPMs on brew and then send directly to coverity scan testing'
	@echo  '  rh-brew-rhev-autotest   - Create a $(COMMON_NAME)-rhev RPMs on brew and then send directly to autotest server'
	@echo  '  rh-brew-rhev-at-covscan - Create a $(COMMON_NAME)-rhev RPMs on brew and then send directly to autotest and coverity testing'
	@echo  '  rh-koji		- Create a $(COMMON_NAME) SRPM and then call koji to build the created SRPM'
	@echo  '  rh-koji-rhev          - Create a rhev version of $(COMMON_NAME) SRPM and then call koji to build the created SRPM'
	@echo  '  rh-koji-rhev-autotest - Create a rhev version of $(COMMON_NAME) RPMs on koji and then send directly to autotest server'
	@echo  '  rh-test		- Pass in brew task number, TASK=1234 make rh-test, to use for an RHTS test'
	@echo  '		  	  setup ./tests to use a test from redhat/tests (minus the .xml)'
	@echo  '		  	  uses a known stable RHEL6 distro as the default'
	@echo  '		  	  use TASK=None to use a non-scratch build based on RELEASE string'
	@echo  '		  	  see output for possible override options (USER_ID,DISTRO,FAMILY,..)'
	@echo  '  rh-brew-test  	- Calls rh-brew and passes the task number into an RHTS test. See rh-test for more'
	@echo  '  rh-rpms		- Create the binary RPMS for the $(COMMON_NAME)'
	@echo  '  rh-$(COMMON_NAME)-<type> 	- Create  binary RPMS for a particular $(COMMON_NAME) type'
	@echo  '                   	- <type> can be: baseonly, smponly, dbgonly'
	@echo  '  rh-all-rpms		- Create the binary RPMS and the SRPM for the $(COMMON_NAME)'
	@echo  '  rh-prep		- Setup the redhat/rpm/BUILD/ directory with the $(COMMON_NAME) source'
	@echo  '  rh-test-patch 	- Create a diff against HEAD and put it in $(COMMON_NAME)-test.patch.'
	@echo  '                  	  Then $(COMMON_NAME)-test.patch will be added to the $(COMMON_NAME) build'
	@echo  '  rh-key		- Generate the required files for compiling with module signing enabled'
	@echo  ''
	@echo  'Configuration targets:'
	@echo
	@echo  '  rh-configs-prep   Creates config files for RHEL 6 architectures, cleans them'
	@echo  '		    by running make nonint_oldconfig, and copies them to'
	@echo  '		    configs/ directory. This is the target to use for a config!'
	@echo  '		    Copy the config file you want from the configs/ directory'
	@echo  '		    to .config'
	@echo  ''
	@echo  ' Most developers will NOT use the following config targets.'
	@echo  ' See the redhat/README file for more info'
	@echo  '  rh-configs	    Creates config files in the redhat/configs/ directory,'
	@echo  '		    these will be used by other Makefile targets and are not'
	@echo  '		    intended for developer use'
