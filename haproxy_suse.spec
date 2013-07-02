#
# spec file for package haproxy (Version 1.4.24)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           haproxy
Version:        1.4.24
Release:        1
#
License:        GPL
Group:          Productivity/Networking/Web/Proxy
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  pcre-devel vim
%define pkg_name haproxy
%define pkg_home /var/lib/%{pkg_name}
#
Url:            http://haproxy.1wt.eu/
Source0:		haproxy-%{version}.tar.gz
Source1:		haproxy.init

#
Summary:        The Reliable, High Performance TCP/HTTP Load Balancer

%description
HAProxy implements an event-driven, mono-process model which enables support
for very high number of simultaneous connections at very high speeds.
Multi-process or multi-threaded models can rarely cope with thousands of
connections because of memory limits, system scheduler limits, and lock
contention everywhere. Event-driven models do not have these problems because
implementing all the tasks in user-space allows a finer resource and time
management. The down side is that those programs generally don't scale well on
multi-processor systems. That's the reason why they must be optimized to get
the most work done from every CPU cycle.


Authors:
--------
   w@1wt.eu


%debug_package
%prep
%setup -n %{pkg_name}-%{version}

%build
%{__make} TARGET=linux2628 CPU="%{_target_cpu}" REGEX=pcre DEBUG="%{optflags} -g"

%install
%{__install} -D -m 0755 %{pkg_name}              %{buildroot}%{_sbindir}/%{pkg_name}
%{__install} -D -m 0644 examples/%{pkg_name}.cfg %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.cfg
%{__install} -D -m 0755 %{S:1}                   %{buildroot}%{_sysconfdir}/init.d/%{pkg_name}
%{__ln_s} -f %{_sysconfdir}/init.d/%{pkg_name}   %{buildroot}%{_sbindir}/rc%{pkg_name}
%{__install} -d -m 0755                          %{buildroot}%{pkg_home}

%clean
%{__rm} -rf %{buildroot}

%pre
/usr/sbin/groupadd -r %{pkg_name} &>/dev/null ||:
/usr/sbin/useradd  -g %{pkg_name} -s /bin/false -r -c "user for %{pkg_name}" -d %{pkg_home} %{pkg_name} &>/dev/null ||:

%post
%fillup_and_insserv %{pkg_name}

%preun
%stop_on_removal %{pkg_name}

%postun
%restart_on_update %{pkg_name}
%{insserv_cleanup}

%files
%defattr(-,root,root,-)
%doc CHANGELOG README ROADMAP TODO
%doc doc/*.txt
%doc examples/url-switching.cfg examples/examples.cfg examples/haproxy.cfg
%dir %{_sysconfdir}/%{pkg_name}
%config(noreplace) %{_sysconfdir}/%{pkg_name}/%{pkg_name}.cfg
%config(noreplace) %{_sysconfdir}/init.d/%{pkg_name}
%{_sbindir}/haproxy
%{_sbindir}/rchaproxy
%{pkg_home}

%changelog