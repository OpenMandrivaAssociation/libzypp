# Avoid any -g (triggers compiler bug causing .LLST* undefined references)
%define optflags -O2
%define major 1430
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname zypp %{major}
%define devname %mklibname zypp -d

Summary:	Software management engine
Name:		libzypp
Version:	14.30.0
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release:	2
Source0:	%{name}-%{version}.tar.gz
%else
Release:	0.%{scmrev}.2
Source0:	%{name}-%{scmrev}.tar.xz
%endif
%else
%if "%{scmrev}" == ""
Release:	0.%{beta}.1
Source0:	%{name}-%{version}%{beta}.tar.bz2
%else
Release:	0.%{beta}.%{scmrev}.1
Source0:	%{name}-%{scmrev}.tar.xz
%endif
%endif
License:	GPLv2+ with extra permission to link to OpenSSL
Group:		System/Libraries
Url:		https://github.com/openSUSE/libzypp
Patch0:		libzypp-20130619-rpm5.patch
Patch1:		libzypp-14.30.0-compile.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	solv-devel
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(libcurl)

%description
ZYpp is a Linux software management engine that powers products like
Zypper with a powerful dependency resolver and a convenient package
management API.

%package -n %{libname}
Summary:	Software management engine
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{libname}
Software management engine.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	zypp-devel = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%if "%{scmrev}" == ""
%setup -q -n %{name}-%{version}%{beta}
%else
%setup -q -n %{name}
%endif
%apply_patches

%build
export CC=gcc
export CXX=g++
%cmake
%make

%install
%makeinstall_std -C build

%files
%{_bindir}/*
%config %{_sysconfdir}/logrotate.d/zypp-history.lr
%dir %{_sysconfdir}/zypp
%config %{_sysconfdir}/zypp/systemCheck
%config %{_sysconfdir}/zypp/zypp.conf
%dir %{_prefix}/lib/zypp
%{_prefix}/lib/zypp/notify-message
%{_datadir}/man/man5/*.5*
%{_mandir}/man1/*
%{_datadir}/zypp

%files -n %{libname}
%{_libdir}/libzypp.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/Modules/*

