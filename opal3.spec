%define version		3.6.8
%define major		%version
%define libname		%mklibname opal %{major}
%define develname	%mklibname %{name} -d

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Summary:	VoIP library
Name:		opal3
Version:	%version
Release:	%mkrel 3
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/opal/opal-%{version}.tar.bz2
Patch0:		opal-3.6.8-link.patch
BuildRequires:	gawk
BuildRequires:	openssl-devel
BuildRequires:	libilbc-devel
BuildRequires:	ptlib-devel >= 2.6.6
BuildRequires:	libspeex-devel
BuildRequires:	libtheora-devel
BuildRequires:	isdn4k-utils-devel
%if %build_plf
BuildRequires: x264-devel
%endif
#BuildRequires:	celt-devel >= 0.7.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires:	ptlib-devel >= 2.4.1
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{mklibname opal -d}

%description -n	%{develname}
Header files and libraries for developing applications that use
Opal.

%prep
%setup -q -n opal-%{version}
%patch0 -p1 -b .link

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

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{libname}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{libname}
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{libname}-plugins
%defattr(-,root,root)
%{_libdir}/opal-%{version}/codecs/audio/*
%{_libdir}/opal-%{version}/codecs/video/*
%{_libdir}/opal-%{version}/lid/*

%files -n %{develname}
%defattr(-,root,root)
%doc mpl-1.0.htm
%attr(0755,root,root) %{_libdir}/*.so
%{_libdir}/*.*a
%{_includedir}/*
%{_libdir}/pkgconfig/opal.pc
