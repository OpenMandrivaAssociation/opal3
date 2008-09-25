%define _disable_ld_as_needed		1
%define _disable_ld_no_undefined	1

%define major		3.4.1
%define libname		%mklibname opal %{major}
%define develname	%mklibname %{name} -d

Summary:	VoIP library
Name:		opal3
Version:	3.4.1
Release:	%mkrel 2
License:	MPL
Group:		System/Libraries
URL:		http://www.opalvoip.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/opal/3.4/opal-%{version}.tar.bz2
BuildRequires:	gawk
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	ptlib-devel >= 2.4.1
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

%build
%configure2_5x

%make OPTCCFLAGS="%{optflags}" RPM_OPT_FLAGS="%{optflags}" 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
