%define major		%{version}
%define libname		%mklibname opal %{major}
%define develname	%mklibname %{name} -d

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%if %mdvver >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

%define url_ver %(echo %version | cut -d. -f1,2)

Summary:	VoIP library
Name:		opal3
Version:	3.10.2
Release:	2%{?extrarelsuffix}
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/opal/%{url_ver}/opal-%{version}.tar.xz
Patch0:		opal-3.10.1-fix-link.patch
Patch2:		opal-3.10.2-ffmpeg0.8.patch
BuildRequires:	gawk
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	ptlib-devel >= 2.10.2
BuildRequires:	libspeex-devel
BuildRequires:	libtheora-devel
BuildRequires:	ffmpeg-devel
%if %build_plf
BuildRequires:	x264-devel
%endif
BuildRequires:	celt-devel >= 0.7.0

%description
This is an open source class library for the development of
applications that wish to use SIP / H.323 protocols for multimedia
communications over packet based networks.

%if %build_plf
This package is in PLF because the H264 codec is covered by patents.
%endif

%package -n	%{libname}-plugins
Summary:	Codec plugins for Opal
Group:		System/Libraries
Provides:	%{name}-plugins = %{version}-%{release}
Obsoletes:	%{mklibname opal 3}-plugins < 3.4.1-2mdv

%description -n	%{libname}-plugins
PTlib codec plugins for various formats provided by Opal.

%package -n	%{libname}
Summary:	Opal Library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Requires:	%{libname}-plugins = %{version}-%{release}
Obsoletes:	%{mklibname opal 3} < 3.4.1-2mdv

%description -n	%{libname}
Shared library for OPAL (SIP / H323 stack).

%package -n	%{develname}
Summary:	Opal development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release} 
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{mklibname opal -d}

%description -n	%{develname}
Header files and libraries for developing applications that use
Opal.

%prep
%setup -q -n opal-%{version}
%patch0 -p0 -b .link
%patch2 -p0 -b .ffmpeg

%build
#gw don't use the default %%optflags, see
# https://qa.mandriva.com/show_bug.cgi?id=48476
%define optflags %nil
#gw else the UINT64_C macro is not defined by stdint.h
export STDCCFLAGS=-D__STDC_CONSTANT_MACROS
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall_std

# remove incorrect symlinks (http://bugzilla.gnome.org/show_bug.cgi?id=553808 )
rm -f %{buildroot}%{_libdir}/libopal.so.?
rm -f %{buildroot}%{_libdir}/libopal.so.?.?

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{libname}-plugins
%{_libdir}/opal-%{version}/codecs/audio/*
%{_libdir}/opal-%{version}/codecs/video/*

%files -n %{develname}
%doc mpl-1.0.htm
%attr(0755,root,root) %{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/*
%{_libdir}/pkgconfig/opal.pc
