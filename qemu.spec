Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 0.8.0
Release: 3%{?dist}

License: GPL/LGPL
Group: Development/Tools
URL: http://fabrice.bellard.free.fr/qemu
Source0: http://www.qemu.org/%{name}-%{version}.tar.gz
Source1: qemu.init
Patch0: qemu-0.7.0-build.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: SDL-devel compat-gcc-32
PreReq: /sbin/chkconfig
PreReq: /sbin/service
ExclusiveArch: %{ix86} ppc alpha sparc armv4l x86_64

%description
By using dynamic translation it achieves a reasonable speed while being easy
to port on new host CPUs. QEMU has two operating modes:

 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU. Linux system calls are converted because of
   endianness and 32/64 bit mismatches. Wine (Windows emulation) and DOSEMU
   (DOS emulation) are the main targets for QEMU.
 * Full system emulation. In this mode, QEMU emulates a full system, including
   a processor and various peripherals. Currently, it is only used to launch
   an x86 Linux kernel on an x86 Linux system. It enables easier testing and
   debugging of system code. It can also be used to provide virtual hosting
   of several virtual PC on a single server.

As QEMU requires no host kernel patches to run, it is very safe and easy to use.

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=%{_prefix} --interp-prefix=%{_prefix}/qemu-%%M \
%ifarch x86_64
   --target-list="i386-user arm-user armeb-user ppc-user mips-user mipsel-user i386-softmmu ppc-softmmu  x86_64-softmmu mips-softmmu arm-softmmu" \
%endif
   --cc=gcc32 --enable-alsa
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
	bindir="${RPM_BUILD_ROOT}%{_bindir}" \
	sharedir="${RPM_BUILD_ROOT}%{_prefix}/share/qemu" \
	mandir="${RPM_BUILD_ROOT}%{_mandir}" \
	docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
	datadir="${RPM_BUILD_ROOT}%{_prefix}/share/qemu" install

install -D $RPM_SOURCE_DIR/qemu.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/qemu

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add qemu

%preun
if [ $1 = 0 ]; then
        /sbin/service qemu stop > /dev/null 2>&1
fi
/sbin/chkconfig --del qemu

%files
%defattr(-,root,root)
%doc Changelog README README.distrib TODO
%doc qemu-tech.texi qemu-doc.texi
%doc *.html
%{_bindir}/qemu*
%{_prefix}/share/qemu
%{_mandir}/man?/*
%config %{_sysconfdir}/rc.d/init.d/qemu

%changelog
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
