%define major 1735
%define libname %mklibname zypp
%define devname %mklibname zypp -d
# libzypp-tui intentionally uses libzypp symbols without linking to it
# (and libzypp-tui is created first)
%define _disable_ld_no_undefined 1

%global optflags %{optflags} -DPROTOBUF_USE_DLLS -DLIBSOLV_SOLVABLE_PREPEND_DEP -DBOOST_POINTERS_NO_IOSTREAM

Summary:	Software management engine
Name:		libzypp
Version:	17.35.19
Release:	1
Source0:	https://github.com/openSUSE/libzypp/archive/%{version}/%{name}-%{version}.tar.gz
License:	GPLv2+ with extra permission to link to OpenSSL
Group:		System/Libraries
Url:		https://github.com/openSUSE/libzypp
BuildRequires:	a2x
BuildRequires:	asciidoc
BuildRequires:	cmake
BuildRequires:	gettext
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libsolv)
BuildRequires:	graphviz
BuildRequires:	nginx
BuildRequires:	fcgi-devel
BuildRequires:	cmake(absl)
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(gpgme)
BuildRequires:	pkgconfig(libproxy-1.0)
BuildRequires:	pkgconfig(yaml-cpp)
BuildRequires:	pkgconfig(sigc++-2.0)
BuildRequires:	pkgconfig(zck)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(bzip2)
Requires:	libsolv
Recommends:	distro-release-repos

%patchlist
libzypp-17.31.8-protobuf-implicit-deps.patch
libzypp-17.16.0-omv-extra-arches.patch
libzypp-17.31-yamllinkage.patch
libzypp-17.31.18-boost-1.83.patch
libzypp-17.32.0-c++20.patch
libzypp-17.31.18-clang.patch
https://github.com/openSUSE/libzypp/pull/586/commits/902c831606f8dd04d4967187701c79bdc8e20508.patch
https://github.com/openSUSE/libzypp/pull/586/commits/263600954c4a8f8d606d7592a7f49f2b9df746ed.patch
https://github.com/openSUSE/libzypp/pull/586/commits/bd828d0f4bfc6cc8043687872656558d06cc7b10.patch

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
%autosetup -p1
#find . -name CMakeLists.txt -o -name "*.cmake" |xargs sed -i -e 's,CXX_STANDARD 17,CXX_STANDARD 20,g'

%build
%cmake \
	-DFEDORA:BOOL=TRUE \
	-DENABLE_BUILD_TRANS=ON \
	-DENABLE_ZCHUNK_COMPRESSION:BOOL=ON \
	-DENABLE_ZSTD_COMPRESSION:BOOL=ON \
	-DEXPORT_NG_API:BOOL=ON \
	-DVSFTPD=%{_bindir}/true \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
%find_lang zypp

# Let's use the same repo files for dnf and zypper...
ln -s ../yum.repos.d %{buildroot}/%{_sysconfdir}/zypp/repos.d

%files -f zypp.lang
%{_bindir}/*
%config %{_sysconfdir}/logrotate.d/zypp-history.lr
%dir %{_sysconfdir}/zypp
%config %{_sysconfdir}/zypp/needreboot
%config %{_sysconfdir}/zypp/systemCheck
%config %{_sysconfdir}/zypp/zypp.conf
%{_sysconfdir}/zypp/repos.d
%{_libexecdir}/zypp/zypp-rpm
%{_datadir}/man/man5/*.5*
%{_mandir}/man1/*
%{_datadir}/zypp

%files -n %{libname}
%{_libdir}/libzypp.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_datadir}/cmake/Modules/*
