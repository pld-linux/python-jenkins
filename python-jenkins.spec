#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"

%define 	module	jenkins
Summary:	Python bindings for the remote Jenkins API
Name:		python-%{module}
Version:	0.2.1
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	https://launchpad.net/python-jenkins/0.2/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	4e9ff3c2e6b0ae8da59a6c46080df898
URL:		http://launchpad.net/python-jenkins
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-nose
%endif
%if %{with doc}
BuildRequires:	python-Sphinx
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python Jenkins is a library for the remote API of the Jenkins
continuous integration server. It is useful for creating and managing
jobs as well as build nodes.

%prep
%setup -q

# Remove env from __init__.py
sed -i '/^#!\%{_prefix}\/bin\/env python$/d' jenkins/__init__.py

%build
%{__python} setup.py build

%if %{with tests}
PYTHONPATH=. nosetests-%{py_ver} -w tests
%endif

%{__make} -C doc html man
rm -f doc/build/html/.buildinfo

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -D doc/build/man/pythonjenkins.1 $RPM_BUILD_ROOT%{_mandir}/man1/pythonjenkins.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING doc/build/html
%dir %{py_sitescriptdir}/jenkins
%{py_sitescriptdir}/jenkins/*.py[co]
%{py_sitescriptdir}/python_jenkins-%{version}-py*.egg-info
# this should be .3?
%{_mandir}/man1/pythonjenkins.1*
