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
/bin/mkdir %{name}
cd %{name}
/bin/tar xzf ~/rpmbuild/SOURCES/%{name}-%{version}.%{buildnumber}.tar.gz
if [ $? -ne 0 ]; then
   exit $?
fi

%build
cd %{name}/LINUX/
./configure --no-drivers --cc=/usr/bin/gcc
make CONFIG_MODULE_SIG=n

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
if ! grep -q "modprobe netmap" /etc/rc.modules 2>/dev/null; then
   echo modprobe netmap >> /etc/rc.modules
fi
chmod +x /etc/rc.modules

# Load netmap if it is not currently loaded
/sbin/lsmod | grep -q netmap
if [ $? -ne 0 ]
then
   modprobe netmap
fi

%preun

%postun

%files
%defattr(-,root,root,-)
/usr/local/probe/include/net
/lib/modules/@KERNEL_VERSION@.x86_64/extra/
/etc/udev/rules.d/
