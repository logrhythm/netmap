Name:          netmap
Version:       %{version}
Release:       %{buildnumber}%{?dist}
Summary:       netmap for Network Monitor
Group:         Development/Tools
License:       Dual BSD/GPL
BuildRequires: kernel-devel = 2.6.32-573.7.1.el6
Requires:      kernel = 2.6.32-573.7.1.el6
ExclusiveArch: x86_64

%description

%prep
cd ~/rpmbuild/BUILD
/bin/rm -rf %{name}
/bin/mkdir %{name}
cd %{name}
/bin/tar xzf ~/rpmbuild/SOURCES/%{name}-%{version}.%{buildnumber}.tar.gz
if [ $? -ne 0 ]; then
   exit $?
fi

%build
# SKIP_BUILD_RPATH, CMAKE_SKIP_BUILD_RPATH, 
cd %{name}/LINUX/
PATH=/usr/local/probe/bin:$PATH
./configure --no-drivers
make

%install
mkdir -p $RPM_BUILD_ROOT/lib/modules/2.6.32-573.7.1.el6.x86_64/extra/
cd ~/rpmbuild/BUILD/%{name}/LINUX
make install

/bin/mkdir -p $RPM_BUILD_ROOT/usr/local/probe/include/netmap
/bin/cp ../sys/net/*.h $RPM_BUILD_ROOT/usr/local/probe/include/netmap

%post

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/local/probe/include
/usr/local/probe/include/netmap
