Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 0.6.1
Release: 1
License: LGPL
Group: Development/Tools
URL: http://fabrice.bellard.free.fr/qemu
Source0: http://fabrice.bellard.free.fr/qemu/%{name}-%{version}.tar.gz
Source1: qemu.init
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: SDL-devel
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
   a processor and various peripherials. Currently, it is only used to launch
   an x86 Linux kernel on an x86 Linux system. It enables easier testing and
   debugging of system code. It can also be used to provide virtual hosting
   of several virtual PC on a single server. 

As QEMU requires no host kernel patches to run, it is very safe and easy to use.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --interp-prefix=%{_prefix}/qemu-%%M
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
	bindir="${RPM_BUILD_ROOT}%{_bindir}" \
	sharedir="${RPM_BUILD_ROOT}%{_prefix}/share/qemu" \
	mandir="${RPM_BUILD_ROOT}%{_mandir}" \
	docdir="${RPM_BUILD_ROOT}%{_docdir}" \
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

%files
%defattr(-,root,root)
%doc Changelog README README.distrib TODO
%doc qemu-tech.texi qemu-doc.texi 
%doc linux-2.6-qemu-fast.patch
%doc %{_docdir}
%{_bindir}
%{_prefix}/share/qemu
%{_mandir}
%{_sysconfdir}/rc.d/init.d/qemu

%changelog
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
