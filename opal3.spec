%define url_ver %(echo %{version} | cut -d. -f1,2)

%define major	%{version}
%define libname	%mklibname opal %{major}
%define devname	%mklibname %{name} -d

######################
# Hardcode PLF build
%define build_plf 0
######################

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

Summary:	VoIP library
Name:		opal3
Version:	3.10.10
Release:	1%{?extrarelsuffix}
License:	MPL
Group:		System/Libraries
Url:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/opal/%{url_ver}/opal-%{version}.tar.xz
Patch0:		opal-3.10.7-fix-link.patch
Patch2:		opal-3.10.7-ffmpeg-0.11.patch
BuildRequires:	gawk
BuildRequires:	ffmpeg-devel
BuildRequires:	gomp-devel
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(ptlib)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
%if %{build_plf}
BuildRequires:	pkgconfig(x264)
%endif

%description
This is an open source class library for the development of
applications that wish to use SIP / H.323 protocols for multimedia
communications over packet based networks.

%if %{build_plf}
This package is in restricted repository because the H264 codec is
covered by patents.
%endif

%package -n	%{libname}-plugins
Summary:	Codec plugins for Opal
Group:		System/Libraries
Provides:	%{name}-plugins = %{version}-%{release}

%description -n	%{libname}-plugins
PTlib codec plugins for various formats provided by Opal.

%package -n	%{libname}
Summary:	Opal Library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Suggests:	%{libname}-plugins = %{version}-%{release}

%description -n	%{libname}
Shared library for OPAL (SIP / H323 stack).

%package -n	%{devname}
Summary:	Opal development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release} 
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Header files and libraries for developing applications that use
Opal.

%prep
%setup -qn opal-%{version}
%patch0 -p0 -b .link~
%patch2 -p0 -b .ffmpeg~

%build
%global optflags %{optflags} -Ofast -fopenmp
%configure2_5x --disable-static
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libopal.so.%{major}*

%files -n %{libname}-plugins
%{_libdir}/opal-%{version}/codecs/audio/*
%{_libdir}/opal-%{version}/codecs/video/*

%files -n %{devname}
%doc mpl-1.0.htm
%{_libdir}/libopal.so
%{_libdir}/libopal_s.a
%{_includedir}/opal
%{_libdir}/pkgconfig/opal.pc

