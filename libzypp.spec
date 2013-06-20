# Avoid any -g (triggers compiler bug causing .LLST* undefined references)
%define optflags -O2
%define major 1302
%define beta %{nil}
%define scmrev 20130619
%define libname %mklibname zypp %{major}
%define devname %mklibname zypp -d

Name: libzypp
Version: 13.3.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release: 1
Source0: %{name}-%{version}.tar.bz2
%else
Release: 0.%{scmrev}.2
Source0: %{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release: 0.%{beta}.1
Source0: %{name}-%{version}%{beta}.tar.bz2
%else
Release: 0.%{beta}.%{scmrev}.1
Source0: %{name}-%{scmrev}.tar.xz
%endif
%endif
Summary: Software management engine
Patch0: libzypp-20130619-rpm5.patch
URL: https://github.com/openSUSE/libzypp
License: GPLv2+ with extra permission to link to OpenSSL
Group: System/Libraries
BuildRequires: solv-devel
BuildRequires: pkgconfig(rpm)

%description
ZYpp is a Linux software management engine that powers products like
Zypper with a powerful dependency resolver and a convenient package
management API.

%package -n %{libname}
Summary: Software management engine
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Software management engine

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
Provides: zypp-devel = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}-%{scmrev}
%endif
%apply_patches
%cmake

%build
cd build
%make

%install
cd build
%makeinstall_std

%files
%{_bindir}/*
%config %{_sysconfdir}/logrotate.d/zypp-history.lr
%dir %{_sysconfdir}/zypp
%config %{_sysconfdir}/zypp/systemCheck
%config %{_sysconfdir}/zypp/zypp.conf
%dir %{_prefix}/lib/zypp
%{_prefix}/lib/zypp/notify-message
%{_datadir}/man/man5/*.5*
%{_datadir}/zypp

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/Modules/*
