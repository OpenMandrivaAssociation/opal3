%define major		3
%define libname		%mklibname opal %{major}
%define develname	%mklibname %{name} -d

Summary:	VoIP library
Name:		opal3
Version:	3.3.1
Release:	%mkrel 1
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/opal/3.3/opal-%{version}.tar.bz2
# Fixes build with underlinking protection. Not actually needed as
# it's in a plugin, but it's better to have the build working with
# underlinking protection so we can catch any future underlinking 
# issues in the shared library rather than disable it for the whole
# build - AdamW 2008/09
Patch0:		opal-3.3.1-pthread.patch
BuildRequires:	gawk
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	ptlib-devel >= 2.3.1
BuildRequires:	libspeex-devel
BuildRequires:	libtheora-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	X11-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is an open source class library for the development of
applications that wish to use SIP / H.323 protocols for multimedia
communications over packet based networks.

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
Requires:	%{libname}-plugins = %{version}-%{release}

%description -n	%{libname}
Shared library for OPAL (SIP / H323 stack).

%package -n	%{develname}
Summary:	Opal development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release} 
Requires:	ptlib-devel >= 2.1.2
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{mklibname opal -d}

%description -n	%{develname}
Header files and libraries for developing applications that use
Opal.

%prep
%setup -q -n opal-%{version}
%patch0 -p1 -b .pthread

%build
%configure2_5x \
    --enable-localspeex \
    --enable-h263avcodec 

%make OPTCCFLAGS="" RPM_OPT_FLAGS="" 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{libname}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{libname}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{libname}-plugins
%defattr(-,root,root)
%{_libdir}/ptlib/plugins/codec/audio/*
%{_libdir}/ptlib/plugins/codec/video/*
%{_libdir}/ptlib/plugins/lid/*

%files -n %{develname}
%defattr(-,root,root)
%doc mpl-1.0.htm
%attr(0755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/opal
%{_libdir}/pkgconfig/opal.pc
