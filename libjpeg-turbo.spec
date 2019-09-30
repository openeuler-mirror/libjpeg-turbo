Name:           libjpeg-turbo
Version:        2.0.0
Release:        2
Summary:        MMX/SSE2/SIMD accelerated libjpeg-compatible JPEG codec library
License:        IJG
URL:            http://sourceforge.net/projects/libjpeg-turbo
Source0:        http://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-%{version}.tar.gz

Patch0:         libjpeg-turbo-cmake.patch

BuildRequires:  gcc cmake libtool nasm

Obsoletes:      libjpeg < 6b-47 turbojpeg %{name}-utils
Provides:       libjpeg = 6b-47 turbojpeg %{name}-utils

%description
libjpeg-turbo is a JPEG image codec that uses SIMD instructions (MMX, SSE2, NEON, AltiVec)
to accelerate baseline JPEG compression and decompression on x86, x86-64, and ARM systems.

%package   devel
Summary:   Development files for the libjpeg-turbo library
Requires:  libjpeg-turbo = %{version}-%{release}
Provides:  libjpeg-devel = 6b-47 libjpeg-turbo-static = 1.3.1 turbojpeg-devel
Obsoletes: libjpeg-devel < 6b-47 libjpeg-turbo-static < 1.3.1 turbojpeg-devel

%description devel
Development files for the libjpeg-turbo library.

%package   help
Summary:   help document for the libjpeg-turbo package
Buildarch: noarch

%description help
help document for the libjpeg-turbo package.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%{cmake} -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES -DENABLE_STATIC:BOOL=NO .

%make_build V=1

%install
%make_install
%delete_la

chmod -x README.md

%check
%if %{?_with_check:1}%{!?_with_check:0}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test %{?_smp_mflags}
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc LICENSE.md README.* ChangeLog.md usage.txt wizard.txt
%{_libdir}/libjpeg.so.62*
%{_libdir}/libturbojpeg.so.0*
%{_bindir}/*

%files devel
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.txt tjexample.c
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files help
%{_mandir}/man1/*.1*

%changelog
* Sat Sep 21 2019 Lijin Yang <yanglijin@huawei.com> - 2.0.0-2
- Package init
