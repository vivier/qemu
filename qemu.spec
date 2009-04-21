Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 0.10
Release: 12%{?dist}
# I have mistakenly thought the revision name would be 1.0.
# So 0.10 series get Epoch = 1
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
#Source0: http://www.qemu.org/%{name}-%{version}.tar.gz
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/avi/kvm.git
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/avi/kvm-userspace.git
# echo "kdir=$(pwd)/kvm" > ~/.kvm-release-config
# cd kvm-userspace
# mkdir $(HOME)/sf-releases
# ./scripts/make-release kvm-85rc-1.git-snapshot-date +%Y%m%d HEAD HEAD

Source0: qemu-kvm-%{version}.tar.gz
Source1: qemu.init
Source2: kvm.modules


Patch1: 01-tls-handshake-fix.patch
Patch2: 02-vnc-monitor-info.patch
Patch3: 03-display-keymaps.patch
Patch4: 04-vnc-struct.patch
Patch5: 05-vnc-tls-vencrypt.patch
Patch6: 06-vnc-sasl.patch
Patch7: 07-vnc-monitor-authinfo.patch
Patch8: 08-vnc-acl-mgmt.patch

Patch9: kvm-upstream-ppc.patch
Patch10: qemu-fix-debuginfo.patch
Patch11: qemu-fix-gcc.patch
Patch12: qemu-roms-more-room.patch
Patch13: qemu-roms-more-room-fix-vga-align.patch
Patch14: qemu-bios-bigger-roms.patch
Patch15: qemu-fix-display-breakage.patch
Patch16: qemu-fix-qcow2-2TB.patch
Patch17: qemu-fix-qcow2-corruption.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: SDL-devel zlib-devel which texi2html gnutls-devel cyrus-sasl-devel
BuildRequires: rsync dev86 iasl
BuildRequires: pciutils-devel
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}

%define qemudocdir %{_docdir}/%{name}-%{version}

%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
%description img
QEMU is a generic and open source processor emulator which achieves a good 
emulation speed by using dynamic translation.

This package provides the command line tool for manipulating disk images

%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service
%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets

%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: etherboot-zroms-kvm
Requires: vgabios
Requires: bochs-bios >= 2.3.8-0.5
Provides: kvm = 85
Obsoletes: kvm < 85
%ifarch %{ix86} x86_64
Provides: qemu-kvm = %{epoch}:%{version}-%{release}
%endif

%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package system-ppc
Summary: QEMU system emulator for ppc
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios-ppc
%ifarch ppc ppc64
Provides: qemu-kvm = %{epoch}:%{version}-%{release}
%endif
%description system-ppc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ppc

%package system-sparc
Summary: QEMU system emulator for sparc
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sparc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for sparc

%package system-arm
Summary: QEMU system emulator for arm
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for arm

%package system-mips
Summary: QEMU system emulator for mips
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for mips

%package system-cris
Summary: QEMU system emulator for cris
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for cris

%package system-m68k
Summary: QEMU system emulator for m68k
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for m68k

%package system-sh4
Summary: QEMU system emulator for sh4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for sh4

%ifarch %{ix86} x86_64
%package kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvmtrace and kvm_stat.
%endif

%prep
%setup -q -n qemu-kvm-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

%build
# systems like rhel build system does not have a recent enough linker so
# --build-id works. this option is used fedora 8 onwards for giving info
# to the debug packages.

build_id_available() {
 echo "int main () { return 0; }" | gcc -x c -Wl,--build-id - 2>/dev/null
}

if build_id_available; then
 extraldflags="-Wl,--build-id";
 buildldflags="VL_LDFLAGS=-Wl,--build-id"
else
 extraldflags=""
 buildldflags=""
fi

%ifarch %{ix86} x86_64
# sdl outputs to alsa or pulseaudio directly depending on what the system has configured
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --kerneldir=$(pwd)/kernel --prefix=%{_prefix} \
            --audio-drv-list=sdl,alsa,oss \
            --with-patched-kernel \
            --disable-strip \
            --qemu-ldflags=$extraldflags \
            --qemu-cflags="$RPM_OPT_FLAGS"

make V=1 %{?_smp_mflags} $buildldflags
cp qemu/x86_64-softmmu/qemu-system-x86_64 qemu-kvm
cp user/kvmtrace  .
cp user/kvmtrace_format  .
make clean
%endif

echo "%{name}-%{version}" > $(pwd)/kernel/.kernelrelease
cd qemu
./configure \
    --target-list="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu m68k-softmmu \
                mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu ppc-softmmu \
                ppcemb-softmmu ppc64-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu \
                i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
                armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
                mipsel-linux-user ppc-linux-user ppc64-linux-user ppc64abi32-linux-user \
                sh4-linux-user sh4eb-linux-user sparc-linux-user sparc64-linux-user \
                sparc32plus-linux-user" \
    --prefix=%{_prefix} \
    --interp-prefix=%{_prefix}/qemu-%%M \
    --kerneldir=$(pwd)/../kernel --prefix=%{_prefix} \
    --disable-strip \
    --disable-kvm \
    --extra-ldflags=$extraldflags \
    --audio-drv-list=sdl,alsa,oss \
    --extra-cflags="$RPM_OPT_FLAGS"


make %{?_smp_mflags} $buildldflags

%install
rm -rf $RPM_BUILD_ROOT

%ifarch %{ix86} x86_64
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvmtrace $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvmtrace_format $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm_stat $RPM_BUILD_ROOT%{_bindir}/

install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
%endif

cd qemu
make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_prefix}/share/qemu" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_prefix}/share/qemu" install
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/qemu
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}/%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

rm -rf ${RPM_BUILD_ROOT}/usr/share//qemu/pxe*bin
rm -rf ${RPM_BUILD_ROOT}/usr/share//qemu/vgabios*bin
rm -rf ${RPM_BUILD_ROOT}/usr/share//qemu/bios.bin
rm -rf ${RPM_BUILD_ROOT}/usr/share//qemu/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}/usr/share//qemu/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}/usr/share//qemu/openbios-sparc64

# the pxe etherboot images will be symlinks to the images on
# /usr/share/etherboot, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../etherboot/$2.zrom %{buildroot}%{_prefix}/share/qemu/pxe-$1.bin
}

pxe_link e1000 e1000-82542
pxe_link ne2k_pci ne
pxe_link pcnet pcnet32
pxe_link rtl8139 rtl8139
pxe_link virtio virtio-net
ln -s ../vgabios/VGABIOS-lgpl-latest.bin  %{buildroot}/%{_prefix}/share/qemu/vgabios.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.cirrus.bin %{buildroot}/%{_prefix}/share/qemu/vgabios-cirrus.bin
ln -s ../bochs/BIOS-bochs-kvm %{buildroot}/%{_prefix}/share/qemu/bios.bin
ln -s ../openbios/openbios-ppc %{buildroot}/%{_prefix}/share/qemu/openbios-ppc
ln -s ../openbios/openbios-sparc32 %{buildroot}/%{_prefix}/share/qemu/openbios-sparc32
ln -s ../openbios/openbios-sparc64 %{buildroot}/%{_prefix}/share/qemu/openbios-sparc64



%clean
rm -rf $RPM_BUILD_ROOT

%post system-x86
%ifarch %{ix86} x86_64
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh /%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

%post user
/sbin/chkconfig --add qemu

%preun user
if [ $1 -eq 0 ]; then
    /sbin/service qemu stop &>/dev/null || :
    /sbin/chkconfig --del qemu
fi

%postun user
if [ $1 -ge 1 ]; then
    /sbin/service qemu condrestart &>/dev/null || :
fi

%files 
%defattr(-,root,root)

%files common
%defattr(-,root,root)
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html 
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/COPYING 
%doc %{qemudocdir}/COPYING.LIB 
%doc %{qemudocdir}/LICENSE
%dir %{_prefix}/share/qemu/
%{_prefix}/share/qemu/keymaps/
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%{_bindir}/qemu-nbd
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%files user
%defattr(-,root,root)
%{_sysconfdir}/rc.d/init.d/qemu
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-sparc32plus
%files system-x86
%defattr(-,root,root)
%{_bindir}/qemu
%{_bindir}/qemu-system-x86_64
%{_prefix}/share/qemu/bios.bin
%{_prefix}/share/qemu/vgabios.bin
%{_prefix}/share/qemu/vgabios-cirrus.bin
%{_prefix}/share/qemu/pxe-e1000.bin
%{_prefix}/share/qemu/pxe-virtio.bin
%{_prefix}/share/qemu/pxe-pcnet.bin
%{_prefix}/share/qemu/pxe-rtl8139.bin
%{_prefix}/share/qemu/pxe-ne2k_pci.bin
%ifarch %{ix86} x86_64
%{_prefix}/share/qemu/extboot.bin
%{_bindir}/qemu-kvm
%{_sysconfdir}/sysconfig/modules/kvm.modules
%files kvm-tools
%defattr(-,root,root,-)
%{_bindir}/kvmtrace
%{_bindir}/kvmtrace_format
%{_bindir}/kvm_stat
%endif
%files system-sparc
%defattr(-,root,root)
%{_bindir}/qemu-system-sparc
%{_prefix}/share/qemu/openbios-sparc32
%{_prefix}/share/qemu/openbios-sparc64
%files system-arm
%defattr(-,root,root)
%{_bindir}/qemu-system-arm
%files system-mips
%defattr(-,root,root)
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%files system-ppc
%defattr(-,root,root)
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_prefix}/share/qemu/openbios-ppc
%{_prefix}/share/qemu/video.x
%{_prefix}/share/qemu/bamboo.dtb
%{_prefix}/share/qemu/ppc_rom.bin
%files system-cris
%defattr(-,root,root)
%{_bindir}/qemu-system-cris
%files system-m68k
%defattr(-,root,root)
%{_bindir}/qemu-system-m68k
%files system-sh4
%defattr(-,root,root)
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%changelog
* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-12
- Another qcow2 image corruption fix (#496642)

* Mon Apr 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-11
- Fix qcow2 image corruption (#496642)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-10
- Run sysconfig.modules from %post on x86_64 too (#494739)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-9
- Align VGA ROM to 4k boundary - fixes 'qemu-kvm -std vga' (#494376)

* Tue Apr  14 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-8
- Provide qemu-kvm conditional on the architecture.

* Thu Apr  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-7
- Add a much cleaner fix for vga segfault (#494002)

* Sun Apr  5 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-6
- Fixed qcow2 segfault creating disks over 2TB. #491943

* Fri Apr  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-5
- Fix vga segfault under kvm-autotest (#494002)
- Kill kernelrelease hack; it's not needed
- Build with "make V=1" for more verbose logs

* Thu Apr 02 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-4
- Support botting gpxe roms.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-2
- added missing patch. love for CVS.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-1
- Include debuginfo for qemu-img
- Do not require qemu-common for qemu-img
- Explicitly own each of the firmware files
- remove firmwares for ppc and sparc. They should be provided by an external package.
  Not that the packages exists for sparc in the secondary arch repo as noarch, but they
  don't automatically get into main repos. Unfortunately it's the best we can do right
  now.
- rollback a bit in time. Snapshot from avi's maint/2.6.30
  - this requires the sasl patches to come back.
  - with-patched-kernel comes back.

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-0.12.kvm20090323git
- BuildRequires pciutils-devel for device assignment (#492076)

* Mon Mar 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.11.kvm20090323git
- Update to snapshot kvm20090323.
- Removed patch2 (upstream).
- use upstream's new split package.
- --with-patched-kernel flag not needed anymore
- Tell how to get the sources.

* Wed Mar 18 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.10.kvm20090310git
- Added extboot to files list.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.9.kvm20090310git
- Fix wrong reference to bochs bios.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.8.kvm20090310git
- fix Obsolete/Provides pair
- Use kvm bios from bochs-bios package.
- Using RPM_OPT_FLAGS in configure
- Picked back audio-drv-list from kvm package

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.7.kvm20090310git
- modify ppc patch

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.6.kvm20090310git
- updated to kvm20090310git
- removed sasl patches (already in this release)

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.5.kvm20090303git
- kvm.modules were being wrongly mentioned at %%install.
- update description for the x86 system package to include kvm support
- build kvm's own bios. It is still necessary while kvm uses a slightly different
  irq routing mechanism

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.4.kvm20090303git
- seems Epoch does not go into the tags. So start back here.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.1.kvm20090303git
- Use bochs-bios instead of bochs-bios-data
- It's official: upstream set on 0.10

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.9.2-0.2.kvm20090303git
- Added BSD to license list, since many files are covered by BSD

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.9.2-0.1.kvm20090303git
- missing a dot. shame on me

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.92-0.1.kvm20090303git
- Set Epoch to 2
- Set version to 0.92. It seems upstream keep changing minds here, so pick the lowest
- Provides KVM, Obsoletes KVM
- Only install qemu-kvm in ix86 and x86_64
- Remove pkgdesc macros, as they were generating bogus output for rpm -qi.
- fix ppc and ppc64 builds

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.3.kvm20090303git
- only execute post scripts for user package.
- added kvm tools.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.2.kvm20090303git
- put kvm.modules into cvs

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.1.kvm20090303git
- Set Epoch to 1
- Build KVM (basic build, no tools yet)
- Set ppc in ExcludeArch. This is temporary, just to fix one issue at a time.
  ppc users (IBM ? ;-)) please wait a little bit.

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0-0.5.svn6666
- Support VNC SASL authentication protocol
- Fix dep on bochs-bios-data

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.4.svn6666
- use bios from bochs-bios package.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.3.svn6666
- use vgabios from vgabios package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.2.svn6666
- use pxe roms from etherboot package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.1.svn6666
- Updated to tip svn (release 6666). Featuring split packages for qemu.
  Unfortunately, still using binary blobs for the bioses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.9.1-12
- Updated build patch. Closes Red Hat Bugzilla bug #465041.

* Wed Dec 31 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.1-11
- add sparcv9 and sparc64 support

* Fri Jul 25 2008 Bill Nottingham <notting@redhat.com>
- Fix qemu-img summary (#456344)

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-10.fc10
- Rebuild for GNU TLS ABI change

* Wed Jun 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-9.fc10
- Remove bogus wildcard from files list (rhbz #450701)

* Sat May 17 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.9.1-8
- Register binary handlers also for shared libraries

* Mon May  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-7.fc10
- Fix text console PTYs to be in rawmode

* Sun Apr 27 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.9.1-6
- Register binary handler for SuperH-4 CPU

* Wed Mar 19 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-5.fc9
- Split qemu-img tool into sub-package for smaller footprint installs

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-4.fc9
- Fix block device checks for extendable disk formats (rhbz #435139)

* Sat Feb 23 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-3.fc9
- Fix block device extents check (rhbz #433560)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-2
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-1.fc9
- Updated to 0.9.1 release
- Fix license tag syntax
- Don't mark init script as a config file

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-5.fc8
- Fix rtl8139 checksum calculation for Vista (rhbz #308201)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-4.fc8
- Fix debuginfo by passing -Wl,--build-id to linker

* Tue Aug 28 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-4
- Update licence
- Fix CDROM emulation (#253542)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-3.fc8
- Added backport of VNC password auth, and TLS+x509 cert auth
- Switch to rtl8139 NIC by default for linkstate reporting
- Fix rtl8139 mmio region mappings with multiple NICs

* Sun Apr  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.0-2
- Fix direct loading of a linux kernel with -kernel & -initrd (bz 234681)
- Remove spurious execute bits from manpages (bz 222573)

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-1
- Update to 0.9.0

* Wed Jan 31 2007 David Woodhouse <dwmw2@infradead.org> 0.8.2-5
- Include licences

* Mon Nov 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.2-4
- Backport patch to make FC6 guests work by Kevin Kofler
  <Kevin@tigcc.ticalc.org> (bz 207843).

* Mon Sep 11 2006 David Woodhouse <dwmw2@infradead.org> 0.8.2-3
- Rebuild

* Thu Aug 24 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-2
- Remove the target-list iteration for x86_64 since they all build again.
- Make gcc32 vs. gcc34 conditional on %%{fedora} to share the same spec for
  FC5 and FC6.

* Wed Aug 23 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-1
- Update to 0.8.2 (#200065).
- Drop upstreamed syscall-macros patch2.
- Put correct scriplet dependencies.
- Force install mode for the init script to avoid umask problems.
- Add %%postun condrestart for changes to the init script to be applied if any.
- Update description with the latest "about" from the web page (more current).
- Update URL to qemu.org one like the Source.
- Add which build requirement.
- Don't include texi files in %%doc since we ship them in html.
- Switch to using gcc34 on devel, FC5 still has gcc32.
- Add kernheaders patch to fix linux/compiler.h inclusion.
- Add target-sparc patch to fix compiling on ppc (some int32 to float).

* Thu Jun  8 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-3
- More header abuse in modify_ldt(), change BuildRoot:

* Wed Jun  7 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-2
- Fix up kernel header abuse

* Tue May 30 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-1
- Update to 0.8.1

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-6
- Update linker script for PPC

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-5
- Just drop $RPM_OPT_FLAGS. They're too much of a PITA

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-4
- Disable stack-protector options which gcc 3.2 doesn't like

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-3
- Use -mcpu= instead of -mtune= on x86_64 too
- Disable SPARC targets on x86_64, because dyngen doesn't like fnegs

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-2
- Don't use -mtune=pentium4 on i386. GCC 3.2 doesn't like it

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-1
- Update to 0.8.0
- Resort to using compat-gcc-32
- Enable ALSA

* Mon May 16 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-2
- Proper fix for GCC 4 putting 'blr' or 'ret' in the middle of the function,
  for i386, x86_64 and PPC.

* Sat Apr 30 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-1
- Update to 0.7.0
- Fix dyngen for PPC functions which end in unconditional branch

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Mon May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Thu May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
