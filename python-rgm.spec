Summary:   RGM Python 3 environment
Name:      python-rgm
Version:   0.1
Release:   0.rgm
#BuildRoot: /tmp/%{name}-%{version}
Group:     Applications/Base
#BuildArch: noarch
License:   GPLv2
URL:       http://gitlab.budcca-demo.lab/rgm-rpms/python-rgm.git
Packager:  Eric Belhomme <ebelhomme@fr.scc.com>

Source:    %{name}-%{version}.tar.gz

Requires: rgm-base
Requires: python36

BuildRequires: rpm-macros-rgm
BuildRequires: python36-virtualenv python36-pip python3-wheel python36-setuptools


%description
RGM Python 3 Virtual Environment


%prep
    %setup -q

%build
    # create on the fly python3 venv with modules specified as requirements.txt
    python3 -m venv --copies %{name}
    ./%{name}/bin/pip3 install -r requirements.txt

    # clean and patch python3 venv root path
    find ./%{name} -name *.pyc -exec rm -f {} \;
    find ./%{name} -name *.pyo -exec rm -f {} \;
    BUILD_ENV=$(dirname $(grep ^VIRTUAL_ENV= ./%{name}/bin/activate | cut -d '"' -f 2 ))
    for FILE in $(grep -FlR "$BUILD_ENV" $BUILD_ENV); do
        sed -i "s|${BUILD_ENV}|%{rgm_path}/%{name}|g" $FILE
    done

%install
	cp -a ./%{name} ${RPM_BUILD_ROOT}%{rgm_path}/

%postun
	rm -rf %{rgm_path}/%{name}
	
%clean
	rm -rf ${RPM_BUILD_ROOT}%{rgm_path}/%{name}-%{version}


%files
%defattr(-,root,root,-)
%{rgm_path}/%{name}

%changelog
* Tue Oct 29 2019 Eric Belhomme <ebelhomme@fr.scc.com> - 0.1-0.rgm
- package creation