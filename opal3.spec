%define major		3
%define libname		%mklibname opal %{major}
%define develname	%mklibname %{name} -d

Summary:	VoIP library
Name:		opal3
Version:	3.2.0
Release:	%mkrel 1
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org/
Source0:	http://prdownloads.sourceforge.net/opalvoip/opal-%{version}-src.tar.bz2
BuildRequires:	gawk
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	ptlib-devel >= 2.2.0
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
%setup -q -n opal_%{version}

%build
%configure2_5x \
    --enable-localspeex \
    --enable-h263avcodec 

%make OPTCCFLAGS="" RPM_OPT_FLAGS="" 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%post -p /sbin/ldconfig -n %{libname}

%postun -p /sbin/ldconfig -n %{libname}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/lib*.so.%{major}*

%files -n %{libname}-plugins
%defattr(-,root,root)
%{_libdir}/ptlib/codecs/audio/*
%{_libdir}/ptlib/codecs/video/*
%{_libdir}/ptlib/lid/*

%files -n %{develname}
%defattr(-,root,root)
%doc mpl-1.0.htm
%attr(0755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/opal
%{_prefix}/lib/pkgconfig/opal.pc
