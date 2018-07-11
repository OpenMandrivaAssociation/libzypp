%define major 1519
%define beta %{nil}
%define scmrev %{nil}
%define libname %mklibname zypp %{major}
%define devname %mklibname zypp -d
%define _disable_lto 1

Summary:	Software management engine
Name:		libzypp
Version:	15.25.12
%if "%{beta}" == ""
%if "%{scmrev}" == ""
Release:	1
Source0:	%{name}-%{version}.tar.gz
%else
Release:	0.%{scmrev}.1
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
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	solv-devel
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libudev)
BuildConflicts:	pkgconfig(rpm) >= 5

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

