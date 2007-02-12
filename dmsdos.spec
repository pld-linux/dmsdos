#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
# TODO: proper UP/SMP modules build

%define		_rel 1

Summary:	Support for FAT compressed volumes
Summary(pl.UTF-8):	Obsługa skompresowanych systemów plików FAT
Name:		dmsdos
Version:	0.9.2.2
Release:	%{_rel}
License:	GPL/LGPL
Group:		Base/Kernel
Source0:	http://cmp.felk.cvut.cz/~pisa/dmsdos/sources/%{name}-%{version}.tar.gz
# Source0-md5:	51e0011eb5509f8e3d7f168f7ec26ece
Source1:	%{name}.config
Source2:	%{name}-config.h
Patch0:		%{name}-opt.patch
URL:		http://cmp.felk.cvut.cz/~pisa/dmsdos/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers >= 2.2.0 }
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Support for FAT compressed volumes (Stacker, DoubleSpace, DriveSpace).
This package contains some utilities like dmsdosfsck.

%description -l pl.UTF-8
Obsługa skompresowanych systemów plików FAT (Stacker, DoubleSpace,
DriveSpace). Ten pakiet zawiera narzędzia typu dmsdosfsck.

%package -n kernel-fs-dmsdos
Summary:	Linux support for compressed FAT volumes
Summary(pl.UTF-8):	Obsługa skompresowanych systemów plików FAT dla Linuksa
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-fs-dmsdos
Linux support for compressed FAT volumes (Stacker, DoubleSpace,
DriveSpace).

%description -n kernel-fs-dmsdos -l pl.UTF-8
Obsługa skompresowanych systemów plików FAT (Stacker, DoubleSpace,
DriveSpace) dla Linuksa.

%package -n kernel-smp-fs-dmsdos
Summary:	Linux SMP support for compressed FAT volumes
Summary(pl.UTF-8):	Obsługa skompresowanych systemów plików FAT dla Linuksa SMP
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-fs-dmsdos
Linux SMP support for compressed FAT volumes (Stacker, DoubleSpace,
DriveSpace).

%description -n kernel-smp-fs-dmsdos -l pl.UTF-8
Obsługa skompresowanych systemów plików FAT (Stacker, DoubleSpace,
DriveSpace) dla Linuksa SMP.

%prep
%setup -q
%patch0 -p1

%build
cp -f %{SOURCE1} src/.config
cp -f %{SOURCE2} src/dmsdos-config.h
cd src
%{__make} depend
%{__make} clean

%{__make} LIB_SHARED=1 OPT="%{rpmcflags}" libdmsdos.so.0.9.2 \
	dutil dmsdosd dcread dmsdosfsck mcdmsdos cvflist cvftest

# SMP
%{__make} dmsdos.o # PUT PROPER OPTIONS HERE
mv -f dmsdos.o dmsdos-smp.o

# UP
%{__make} dmsdos.o # PUT PROPER OPTIONS HERE

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_libdir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/fs

cd src
install dmsdos-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/fs/dmsdos.o
install dmsdos.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs/dmsdos.o

install libdmsdos.so* $RPM_BUILD_ROOT%{_libdir}
install cvflist cvftest dmsdosd dmsdosfsck dutil $RPM_BUILD_ROOT%{_sbindir}
# maybe better to /usr/lib/mc/extfs in separate subpackage?
install mcdmsdos $RPM_BUILD_ROOT%{_bindir}

cd ../man
install dmsdosfsck.8 $RPM_BUILD_ROOT%{_mandir}/man8
install cvf*.1 dmsdosd.1 dutil.1 $RPM_BUILD_ROOT%{_mandir}/man1
install mcdmsdos.1 $RPM_BUILD_ROOT%{_mandir}/man1

cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n kernel-fs-dmsdos
%depmod %{_kernel_ver}

%postun	-n kernel-fs-dmsdos
%depmod %{_kernel_ver}

%post	-n kernel-smp-fs-dmsdos
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-fs-dmsdos
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
# note: COPYING file contains only some details, not actual GPL text
%doc BUGS COPYING NEWS README doc/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/libdmsdos.so.*.*
%{_mandir}/man?/*

%files -n kernel-fs-dmsdos
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/fs/*

%files -n kernel-smp-fs-dmsdos
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/fs/*
