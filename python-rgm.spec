Summary:   RGM Python 3 environment
Name:      python-rgm
Version:   1.0
Release:   7.rgm
Group:     Applications/Base
License:   GPLv2
URL:       https://gitlab.forge.rgm-cloud.io/rgm-rpms/python-rgm
Source:    %{name}-%{version}.tar.gz

Requires: rgm-base
Requires: python36

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: rpm-macros-rgm
BuildRequires: python36-virtualenv python36-pip python3-wheel python36-setuptools

# disable debuginfo package generation
%define debug_package %{nil}

# force rpmbuild to byte-compile using Python3
%global __python %{__python3}

%description
RGM Python 3.6 Virtual Environment


%prep
%setup -q


%build
# create on the fly python3 venv with modules specified as requirements.txt
python3 -m venv --copies %{name}
./%{name}/bin/pip3 install --upgrade pip
./%{name}/bin/pip3 install -r requirements.txt

# clean and patch python3 venv root path
find ./%{name} -name *.pyc -exec rm -f {} \;
find ./%{name} -name *.pyo -exec rm -f {} \;
BUILD_ENV=$(grep ^VIRTUAL_ENV= ./%{name}/bin/activate | cut -d '"' -f 2)
for FILE in $(grep -FlR "$BUILD_ENV" $BUILD_ENV); do
    sed -i "s|${BUILD_ENV}|%{rgm_path}/%{name}|g" $FILE
done


%install
install -d -o %{rgm_user_nagios} -g %{rgm_group} -m 0755 %{buildroot}%{rgm_path}
cp -a ./%{name} ${RPM_BUILD_ROOT}%{rgm_path}/


%clean
rm -rf ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}


%files
%defattr(-,root,root,-)
%{rgm_path}/%{name}


%changelog
* Wed Jul 06 2022 Christophe Cassan <ccassan@fr.scc.com> - 1.0-7.rgm
- Add tk release

* Wed Sep 29 2021 Eric Belhomme <ebelhomme@fr.scc.com> - 1.0-6.rgm
- fix bug on elasticsearch 7.14 module with OSS ES: downgrade to 7.13

* Wed Sep 15 2021 Eric Belhomme <ebelhomme@fr.scc.com> - 1.0-5.rgm
- add python dependencies : cryptography, requests, hvac

* Tue Nov 03 2020 Lucas Fueyo <lfueyo@fr.scc.com> - 1.0-4.rgm
- add jmespath python module
- add wmi-client-wrapper-py3 python module

* Wed Oct 28 2020 Samuel Ronciaux <sronciaux@fr.scc.com> - 1.0-3.rgm
- add pywebm python module

* Wed Oct 21 2020 Eric Belhomme <ebelhomme@fr.scc.com> - 1.0-2.rgm
- add elasticsearch_dsl python module

* Wed Jan 29 2020 Eric Belhomme <ebelhomme@fr.scc.com> - 1.0-1.rgm
- upgrade pip avec venv creation
- add python-dateutil module in requirements

* Tue Oct 29 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 1.0-0.rgm
- package creation