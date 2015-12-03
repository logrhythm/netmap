Name:          netmap
Version:       %{version}
Release:       %{buildnumber}%{?dist}
Summary:       netmap for Network Monitor
Group:         Development/Tools
License:       Dual BSD/GPL
BuildRequires: kernel-devel = @KERNEL_VERSION@, kernel = @KERNEL_VERSION@
Requires:      kernel = @KERNEL_VERSION@
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
/bin/mkdir -p $RPM_BUILD_ROOT/lib/modules/@KERNEL_VERSION@.x86_64/extra/
cd ~/rpmbuild/BUILD/%{name}/
/bin/cp LINUX/netmap.ko $RPM_BUILD_ROOT/lib/modules/@KERNEL_VERSION@.x86_64/extra/

/bin/mkdir -p $RPM_BUILD_ROOT/usr/local/probe/include/net
/bin/cp sys/net/*.h $RPM_BUILD_ROOT/usr/local/probe/include/net

/bin/mkdir -p $RPM_BUILD_ROOT/etc/udev/rules.d/
echo 'KERNEL=="netmap", GROUP="dpi"' > $RPM_BUILD_ROOT/etc/udev/rules.d/010_netmap.rules

%post
depmod -a
grep -q "modprobe netmap" /etc/rc.modules 2&>1 > /dev/null
if [ $? -ne 0 ]
then
   echo modprobe netmap >> /etc/rc.modules
fi
chmod +x /etc/rc.modules

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/local/probe/include/net
/lib/modules/@KERNEL_VERSION@.x86_64/extra/
/etc/udev/rules.d/
