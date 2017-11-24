%global selinux_variants targeted
%global selinux_policyver 3.7.19
%global modulename powa
%global tagged_files /usr/bin/powa-web /etc/po* /var/log/po*

Name: selinux-policy-%{modulename}
Version: 1.0.0
Release: 1
Summary: SELinux policy module for PoWA
BuildArch: noarch
License: PostgreSQL
Group: System Environment/Base
Url: http://github.com/dalibo/selinux-powa

Source1: %{modulename}.if
Source2: %{modulename}.te
Source3: %{modulename}.fc
BuildRequires: make
BuildRequires: selinux-policy-devel
BuildRequires: checkpolicy
BuildRequires: /usr/share/selinux/devel/policyhelp
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: selinux-policy >= %{selinux_policyver}
Requires(post):   /usr/sbin/semodule, /sbin/restorecon
Requires(postun): /usr/sbin/semodule, /sbin/restorecon

%description
SELinux policy module for PoWA. This module adds the file contexts needed to
confine PoWA.

%prep
mkdir -p SELinux
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} SELinux/

%build
cd SELinux/
for selinuxvariant in %{selinux_variants}
do
  make -f /usr/share/selinux/devel/Makefile NAME=${selinuxvariant}
  mv %{modulename}.pp %{modulename}.pp.${selinuxvariant}
  make -f /usr/share/selinux/devel/Makefile NAME=${selinuxvariant} clean
done
cd -

%install
cd SELinux
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 %{modulename}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
done
cd -

%clean
rm -rf %{buildroot}

%post
for selinuxvariant in %{selinux_variants}
do
    /usr/sbin/semodule -s ${selinuxvariant} -u \
	%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp &> /dev/null || :
done
if [ -n "$(readlink -e %{tagged_files})" ] ; then
  /sbin/restorecon -R $(readlink -e %{tagged_files}) || :
fi

%postun
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
     /usr/sbin/semodule -s ${selinuxvariant} -r %{modulename} &> /dev/null || :
  done
  if [ -n "$(readlink -e %{tagged_files})" ] ; then
    /sbin/restorecon -R $(readlink -e %{tagged_files}) || :
  fi
fi

%files
%defattr(-,root,root,0755)
%{_datadir}/selinux/*/%{modulename}.pp

%changelog
* Wed Nov 22 2017 Étienne BERSAC <etienne.bersac@dalibo.com> - 1.0.0-1
- Initial version
