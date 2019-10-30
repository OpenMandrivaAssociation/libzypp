%define major 1712
%define libname %mklibname zypp %{major}
%define devname %mklibname zypp -d
%define _disable_lto 1

Summary:	Software management engine
Name:		libzypp
Version:	17.16.0
Release:	1
Source0:	https://github.com/openSUSE/libzypp/archive/%{version}/%{name}-%{version}.tar.gz
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
BuildRequires:  pkgconfig(gpgme)

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
%setup -q
%autopatch -p1

%build
%cmake -DFEDORA:BOOL=TRUE -DENABLE_BUILD_TRANS=ON
%make_build

%install
%make_install -C build

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

