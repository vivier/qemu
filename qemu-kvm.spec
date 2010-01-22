Summary: Userspace component of KVM
Name: qemu-kvm
Version: 0.12.1.2
Release: 2.12%{?dist}
# Epoch because we pushed a qemu-1.0 package
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.linux-kvm.org
ExclusiveArch: x86_64

Source0: http://downloads.sourceforge.net/sourceforge/kvm/qemu-kvm-%{version}.tar.gz

# Loads kvm kernel modules at boot
Source2: kvm.modules

# Creates /dev/kvm
Source3: 80-kvm.rules

# KSM control scripts
Source4: ksm.init
Source5: ksm.sysconfig
Source6: ksmtuned.init
Source7: ksmtuned
Source8: ksmtuned.conf

# Change datadir to /usr/share/qemu-kvm
Patch1000: qemu-change-share-suffix.patch
# Install manpage as qemu-kvm(1)
Patch1001: qemu-rename-manpage.patch
# Change SASL server name to qemu-kvm
Patch1002: qemu-rename-sasl-server-name.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1003: kvm-virtio-Remove-duplicate-macro-definition-for-max.-vi.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1004: kvm-virtio-console-qdev-conversion-new-virtio-serial-bus.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1005: kvm-virtio-serial-bus-Maintain-guest-and-host-port-open-.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1006: kvm-virtio-serial-bus-Add-a-port-name-property-for-port-.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1007: kvm-virtio-serial-bus-Add-support-for-buffering-guest-ou.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1008: kvm-virtio-serial-bus-Add-ability-to-hot-unplug-ports.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1009: kvm-virtio-serial-Add-a-virtserialport-device-for-generi.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1010: kvm-Move-virtio-serial-to-Makefile.hw.patch
# For bz#556459 - RFE - In-place backing file format change
Patch1011: kvm-block-Introduce-BDRV_O_NO_BACKING.patch
# For bz#556459 - RFE - In-place backing file format change
Patch1012: kvm-block-Add-bdrv_change_backing_file.patch
# For bz#556459 - RFE - In-place backing file format change
Patch1013: kvm-qemu-img-rebase.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1014: kvm-virtio-serial-bus-Remove-guest-buffer-caching-and-th.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1015: kvm-virtio-serial-Make-sure-we-don-t-crash-when-host-por.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1016: kvm-virtio-serial-Use-MSI-vectors-for-port-virtqueues.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1017: kvm-virtio-serial-bus-Match-upstream-whitespace.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: SDL-devel zlib-devel which texi2html gnutls-devel cyrus-sasl-devel
BuildRequires: rsync dev86 iasl
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: ncurses-devel
BuildRequires: libaio-devel

Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service

Provides: kvm = 85
Obsoletes: kvm < 85
Requires: vgabios
Requires: seabios
Requires: /usr/share/gpxe/e1000-0x100e.rom
Requires: /usr/share/gpxe/rtl8029.rom
Requires: /usr/share/gpxe/pcnet32.rom
Requires: /usr/share/gpxe/rtl8139.rom
Requires: /usr/share/gpxe/virtio-net.rom

# We don't provide vvfat anymore, that is used by older VDSM versions.
Conflicts: vdsm < 4.5

Requires: qemu-img = %{epoch}:%{version}-%{release}

%define qemudocdir %{_docdir}/%{name}-%{version}

%description
KVM (for Kernel-based Virtual Machine) is a full virtualization solution
for Linux on x86 hardware.

Using KVM, one can run multiple virtual machines running unmodified Linux
or Windows images. Each virtual machine has private virtualized hardware:
a network card, disk, graphics adapter, etc.

%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
%description -n qemu-img
This package provides a command line tool for manipulating disk images

%package tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description tools
This package contains some diagnostics and debugging tools for KVM,
such as kvmtrace and kvm_stat.

%prep
%setup -q -n qemu-kvm-%{version}


%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1
%patch1010 -p1
%patch1011 -p1
%patch1012 -p1
%patch1013 -p1
%patch1014 -p1
%patch1015 -p1
%patch1016 -p1
%patch1017 -p1

%build
# --build-id option is used fedora 8 onwards for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (#495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --prefix=%{_prefix} \
            --audio-drv-list=pa,alsa \
            --audio-card-list=ac97,es1370 \
            --disable-strip \
            --extra-ldflags=$extraldflags \
            --extra-cflags="$RPM_OPT_FLAGS" \
            --disable-xen \
            --block-drv-whitelist=qcow2,raw,host_device,host_cdrom \
            --disable-debug-tcg \
            --disable-sparse \
            --disable-werror \
            --disable-sdl \
            --disable-curses \
            --disable-curl \
            --disable-check-utests \
            --enable-vnc-tls \
            --enable-vnc-sasl \
            --disable-brlapi \
            --disable-bluez \
            --enable-docs \
            --disable-vde \
            --enable-linux-aio \
            --enable-kvm \
            --enable-kvm-cap-pit \
            --enable-kvm-cap-device-assignment

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

cd kvm/user
./configure --prefix=%{_prefix} --kerneldir=$(pwd)/../kernel/
make kvmtrace
cd ../../

%install
rm -rf $RPM_BUILD_ROOT

install -D -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_initddir}/ksm
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm

install -D -p -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_initddir}/ksmtuned
install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/user/kvmtrace $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/user/kvmtrace_format $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" install

mv ${RPM_BUILD_ROOT}%{_bindir}/qemu-system-x86_64 ${RPM_BUILD_ROOT}%{_bindir}/qemu-kvm

rm -rf ${RPM_BUILD_ROOT}%{_bindir}/qemu-nbd
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8/qemu-nbd.8*

chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu-kvm.conf

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/petalogix-s3adsp1800.dtb
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/video.x
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bamboo.dtb
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/ppc_rom.bin

# the pxe gpxe images will be symlinks to the images on
# /usr/share/gpxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../gpxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.bin
}

pxe_link e1000 e1000-0x100e
pxe_link ne2k_pci rtl8029
pxe_link pcnet pcnet32
pxe_link rtl8139 rtl8139
pxe_link virtio virtio-net
ln -s ../vgabios/VGABIOS-lgpl-latest.bin  %{buildroot}/%{_datadir}/%{name}/vgabios.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.cirrus.bin %{buildroot}/%{_datadir}/%{name}/vgabios-cirrus.bin
ln -s ../seabios/bios.bin %{buildroot}/%{_datadir}/%{name}/bios.bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

/sbin/chkconfig --add ksm
/sbin/chkconfig --add ksmtuned

# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh %{_sysconfdir}/sysconfig/modules/kvm.modules

%preun
if [ $1 -eq 0 ]; then
    /sbin/service ksmtuned stop &>/dev/null || :
    /sbin/chkconfig --del ksmtuned
    /sbin/service ksm stop &>/dev/null || :
    /sbin/chkconfig --del ksm
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service ksm condrestart &>/dev/null || :
    /sbin/service ksmtuned condrestart &>/dev/null || :
fi

%files
%defattr(-,root,root)
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu-kvm.1*
%config(noreplace) %{_sysconfdir}/sasl2/qemu-kvm.conf
%{_initddir}/ksm
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_initddir}/ksmtuned
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/vapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/pxe-e1000.bin
%{_datadir}/%{name}/pxe-virtio.bin
%{_datadir}/%{name}/pxe-pcnet.bin
%{_datadir}/%{name}/pxe-rtl8139.bin
%{_datadir}/%{name}/pxe-ne2k_pci.bin
%{_datadir}/%{name}/extboot.bin
%{_bindir}/qemu-kvm
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/udev/rules.d/80-kvm.rules
%files tools
%defattr(-,root,root,-)
%{_bindir}/kvmtrace
%{_bindir}/kvmtrace_format
%{_bindir}/kvm_stat

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_mandir}/man1/qemu-img.1*

%changelog
* Fri Jan 22 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.12.el6
- kvm-virtio-serial-bus-Remove-guest-buffer-caching-and-th.patch [bz#543825]
- kvm-virtio-serial-Make-sure-we-don-t-crash-when-host-por.patch [bz#543825]
- kvm-virtio-serial-Use-MSI-vectors-for-port-virtqueues.patch [bz#543825]
- kvm-virtio-serial-bus-Match-upstream-whitespace.patch [bz#543825]
- Resolves: bz#543825
  ([RFE] Backport virtio-serial device to qemu)

* Mon Jan 18 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.11.el6
- kvm-block-Introduce-BDRV_O_NO_BACKING.patch [bz#556459]
- kvm-block-Add-bdrv_change_backing_file.patch [bz#556459]
- kvm-qemu-img-rebase.patch [bz#556459]
- Resolves: bz#556459
  (RFE - In-place backing file format change)

* Mon Jan 18 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.10.el6
- Conflicts with older vdsm version, that needs vvfat support
- Related: bz#555336

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.9.el6
- Disable -Werror again, as there are still warnings on the build
- Related: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.8.el6
- Require libaio-devel for build
- Related: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.7.el6
- Disable vvfat support
- Resolves: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.6.el6
- Fix misapply of virtio patches
- Related: bz#543825

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.5.el6
- Remove unneeded/unsupported features: [bz#555336]
  - make default options explicit
  - remove sdl support
  - remove sb16 emulation
  - remove oss support
  - remove curses support
  - disable curl support
  - disable bluez support
  - enable -Werror
  - limit block drivers support
  - add host_cdrom block device
- Resolves: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.4.el6
- kvm-virtio-Remove-duplicate-macro-definition-for-max.-vi.patch [bz#543825]
- kvm-virtio-console-qdev-conversion-new-virtio-serial-bus.patch [bz#543825]
- kvm-virtio-serial-bus-Maintain-guest-and-host-port-open-.patch [bz#543825]
- kvm-virtio-serial-bus-Add-a-port-name-property-for-port-.patch [bz#543825]
- kvm-virtio-serial-bus-Add-support-for-buffering-guest-ou.patch [bz#543825]
- kvm-virtio-serial-bus-Add-ability-to-hot-unplug-ports.patch [bz#543825]
- kvm-virtio-serial-Add-a-virtserialport-device-for-generi.patch [bz#543825]
- kvm-Move-virtio-serial-to-Makefile.hw.patch [bz#543825]
- Resolves: bz#543825
  ([RFE] Backport virtio-serial device to qemu)

* Tue Jan 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.3.el6
- Use seabios instead of bochs-bios
- Resolves: bz#553732

* Tue Jan 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.2.el6
- Build only on x86_64
- Resolves: bz#538039

* Thu Jan 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.1.el6
- Rebasing to 0.12.1.2-2.fc13
- Resolves: bz#553271

* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 2:0.11.0-7.1
- Rebuilt for RHEL 6

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-7.el6
- Initial RHEL6 qemu-kvm package
