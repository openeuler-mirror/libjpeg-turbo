Name:           libjpeg-turbo
Version:        2.0.5
Release:        1
Summary:        MMX/SSE2/SIMD accelerated libjpeg-compatible JPEG codec library
License:        IJG
URL:            http://sourceforge.net/projects/libjpeg-turbo
Source0:        http://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-%{version}.tar.gz

BuildRequires:  gcc cmake libtool nasm

Obsoletes:      libjpeg < 6b-47 turbojpeg = %{version}-%{release}  
Provides:       libjpeg = 6b-47 turbojpeg < %{version}-%{release}  

Provides:       %{name}-utils = %{version}-%{release}
Obsoletes:      %{name}-utils < %{version}-%{release}

%description
libjpeg-turbo is a JPEG image codec that uses SIMD instructions (MMX, SSE2, NEON, AltiVec)
to accelerate baseline JPEG compression and decompression on x86, x86-64, and ARM systems.

%package        devel
Summary:        Development files for the libjpeg-turbo library
Requires:       libjpeg-turbo = %{version}-%{release}
Provides:       libjpeg-turbo-static = 1.3.1 turbojpeg-devel = %{version}-%{release}
Obsoletes:      libjpeg-turbo-static < 1.3.1 turbojpeg-devel < %{version}-%{release}
Provides:       libjpeg-devel = 6b-47 libjpeg-devel%{?_isa} = %{version}-%{release}
Obsoletes:      libjpeg-devel < 6b-47


%description devel
Development files for the libjpeg-turbo library.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%{cmake} -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES -DENABLE_STATIC:BOOL=NO .

%make_build V=1

%install
%make_install
%delete_la

chmod -x README.md

%ifarch x86_64
  %global wordsize "64"
%else
  %global wordsize ""
%endif

if test -n "$wordsize"
then
  pushd $RPM_BUILD_ROOT%{_includedir}
    mv jconfig.h jconfig-$wordsize.h
    cat > jconfig.h <<EOF
#ifndef JCONFIG_H_MULTILIB
#define JCONFIG_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "jconfig-32.h"
#elif __WORDSIZE == 64
# include "jconfig-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF
fi
    
%check
%if %{?_with_check:1}%{!?_with_check:0}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test %{?_smp_mflags}
%endif

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.*
%license LICENSE.md
%{_bindir}/*
%{_libdir}/libjpeg.so.62*
%{_libdir}/libturbojpeg.so.0*
%exclude /usr/share/doc/libjpeg-turbo/*

%files devel
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.txt tjexample.c
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files help
%doc usage.txt wizard.txt ChangeLog.md
%{_mandir}/man1/*.1*

%changelog
* Wed Jul 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.5-1
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:upgrade to 2.0.5

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.0-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:remove the libjpeg-devel with arch in obsoletes

* Fri Nov 1 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.0.0-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the libjpeg-devel and jconfig.h

* Sat Sep 21 2019 Lijin Yang <yanglijin@huawei.com> - 2.0.0-2
- Package init
