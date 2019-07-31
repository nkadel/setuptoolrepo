#
# spec file for package python-pip
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

%global pypi_name pip

# Common SRPM package
Name:           python-%{pypi_name}
Version:        19.2.1
Release:        0%{?dist}
Url:            https://pip.pypa.io/
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
pip - The Python Package Installer
==================================

pip is the `package installer`_ for Python. You can use pip to install packages from the `Python Package Index`_ and other indexes.

Please take a look at our documentation for how to install and use pip:

* `Installation`_
* `Usage`_

%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        19.2.1
Release:        0%{?dist}
Url:            https://pip.pypa.io/
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
pip - The Python Package Installer
==================================

.. image:: https://img.shields.io/pypi/v/pip.svg
   :target: https://pypi.org/project/pip/

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest
   :target: https://pip.pypa.io/en/latest

pip is the `package installer`_ for Python. You can use pip to install packages from the `Python Package Index`_ and other indexes.

Please take a look at our documentation for how to install and use pip:

* `Installation`_
* `Usage`_

%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Version:        19.2.1
Release:        0%{?dist}
Url:            https://pip.pypa.io/
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
pip - The Python Package Installer
==================================

pip is the `package installer`_ for Python. You can use pip to install packages from the `Python Package Index`_ and other indexes.

Please take a look at our documentation for how to install and use pip:

* `Installation`_
* `Usage`_

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
%endif # with_python3

%if %{with_python2}
%py2_install
%endif # with_python2

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
%{python2_sitelib}/*
%{python3_sitelib}/%{pypi_name}%{py_version}
%{python3_sitelib}/%{pypi_name}2
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(-,root,root,-)
%{python3_sitelib}/%{pypi_name}%{py3_version}
%{python3_sitelib}/%{pypi_name}3
%if ! %{with_python2}
%{python3_sitelib}/%{pypi_name}
%endif
%endif # with_python3

%changelog
