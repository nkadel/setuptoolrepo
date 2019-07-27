#
# spec file for package python-setuptools
#
# Copyright (c) 2019 Nico Kadel-Garcia.
#

# python3_pkgversion macro for EPEL in older RHEL
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Fedora and RHEL split python2 and python3
# Older RHEL requires EPEL and python34 or python36
%global with_python3 1

# Fedora >= 38 no longer publishes python2 by default
%if 0%{?fedora} >= 30
%global with_python2 0
%else
%global with_python2 1
%endif

# Older RHEL does not use dnf, does not support "Suggests"
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_dnf 1
%else
%global with_dnf 0
%endif

%global pypi_name setuptools

# Common SRPM package
Name:           python-%{pypi_name}
Version:        41.0.1
Release:        0%{?dist}
Url:            https://github.com/pypa/setuptools
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
License:        MIT
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.zip
BuildArch:      noarch
BuildRequires:  unzip

%description

See the `Installation Instructions
<https://packaging.python.org/installing/>`_ in the Python Packaging
User Guide for instructions on installing, upgrading, and uninstalling
Setuptools.

Questions and comments should be directed to the `distutils-sig
mailing list <http://mail.python.org/pipermail/distutils-sig/>`_.
Bug reports and especially tested patches may be
submitted directly to the `bug tracker
<https://github.com/pypa/setuptools/issues>`_.

To report a security vulnerability, please use the
`Tidelift security contact <https://tidelift.com/security>`_.
Tidelift will coordinate the fix and disclosure.


%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        41.0.1
Release:        0%{?dist}
Url:            https://github.com/pypa/setuptools
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
License:        MIT

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# Manually added
#[certs]
BuildRequires: python2-certifi >= 2016.9.26
Requires: python2-certifi >= 2016.9.26
#[ssl:sys_platform=='win32']
#wincertstore==0.2
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
See the `Installation Instructions
<https://packaging.python.org/installing/>`_ in the Python Packaging
User Guide for instructions on installing, upgrading, and uninstalling
Setuptools.

Questions and comments should be directed to the `distutils-sig
mailing list <http://mail.python.org/pipermail/distutils-sig/>`_.
Bug reports and especially tested patches may be
submitted directly to the `bug tracker
<https://github.com/pypa/setuptools/issues>`_.

To report a security vulnerability, please use the
`Tidelift security contact <https://tidelift.com/security>`_.
Tidelift will coordinate the fix and disclosure.

%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Version:        41.0.1
Release:        0%{?dist}
Url:            https://github.com/pypa/setuptools
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
License:        MIT

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# Manually added
BuildRequires: python%{python3_pkgversion}-certifi >= 2016.9.26
Requires: python%{python3_pkgversion}-certifi >= 2016.9.26
#[ssl:sys_platform=='win32']
#wincertstore==0.2
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
See the `Installation Instructions
<https://packaging.python.org/installing/>`_ in the Python Packaging
User Guide for instructions on installing, upgrading, and uninstalling
Setuptools.

Questions and comments should be directed to the `distutils-sig
mailing list <http://mail.python.org/pipermail/distutils-sig/>`_.
Bug reports and especially tested patches may be
submitted directly to the `bug tracker
<https://github.com/pypa/setuptools/issues>`_.

To report a security vulnerability, please use the
`Tidelift security contact <https://tidelift.com/security>`_.
Tidelift will coordinate the fix and disclosure.

%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with_python2}
%py2_build
%endif # with_python2

%if %{with_python3}
%py3_build
%endif # with_python3

%install
%if %{with_python3}
%py3_install

ls -al $RPM_BUILD_ROOT%{_bindir}/
%{__mv} $RPM_BUILD_ROOT%{_bindir}/easy_install $RPM_BUILD_ROOT%{_bindir}/easy_install-%{python3_version} 
%{__ln_s} -f easy_install-%{python3_version} $RPM_BUILD_ROOT%{_bindir}/easy_install
%endif # with_python3


%if %{with_python2}
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/easy_install $RPM_BUILD_ROOT%{_bindir}/easy_install-%{python2_version} 
%{__ln_s} -f easy_install-%{python2_version} $RPM_BUILD_ROOT%{_bindir}/easy_install
%endif # with_python2

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{_bindir}/easy_install-%{python2_version}
%{_bindir}/easy_install
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/easy_install-%{python3_version}
%if ! %{with_python2}
%{_bindir}/easy_install
%endif # ! with_python2
%endif # with_python3

%changelog
* Fri Jul 26 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 41.0.1-0
- Build spec file with py2pack
- Manually add dependencies
- Manually set /usr/bin/pyhton as symlink to default version
