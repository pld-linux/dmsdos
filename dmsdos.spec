
# conditional build
# _without_dist_kernel          without distribution kernel

%define		_rel 1

Summary:	Support for FAT compressed volumes
Name:		dmsdos
Version:	0.9.2.2
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
URL:		http://cmp.felk.cvut.cz/~pisa/dmsdos/
Source0: 	http://cmp.felk.cvut.cz/~pisa/dmsdos/sources/dmsdos-0.9.2.2.tar.gz
Source1:	dmsdos.config
Source2:	dmsdos-config.h
%{!?_without_dist_kernel:BuildRequires:         kernel-headers >= 2.2.0 }
BuildRequires:	%{kgcc_package}
BuildRequires:	grep
BuildRequires:	textutils
PreReq:		/sbin/depmod
PreReq:		modutils >= 2.3.18-2
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires:	dev >= 2.7.7-10
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%package -n dmsdos-smp
Summary:	SMP module for dmsdos
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
PreReq:		/sbin/depmod
PreReq:		modutils >= 2.3.18-2
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires:	dev >= 2.7.7-10

%description -n dmsdos-smp

%prep
%setup -q

%build
cp %{SOURCE1} src/.config
cp %{SOURCE2} src/dmsdos-config.h
cd src
make depend
make clean
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/fs
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/fs
install NVdriver-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/NVdriver.o
install NVdriver.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/NVdriver.o

gzip -9nf README

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n dmsdos-smp
/sbin/depmod -a

%postun -n dmsdos-smp
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}/misc/*

%files -n dmsdos-smp
%defattr(644,root,root,755)
%doc *.gz
/lib/modules/%{_kernel_ver}smp/misc/*
