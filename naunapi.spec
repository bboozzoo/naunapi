Name:           naunapi
Version:        0.1
Release:        1%{?dist}
Summary:        Integration of pynapi with Nautilus

License:        GPLv3
URL:            
Source0:        naunapi.py

Requires:       nautilus-python
Requires:       gtk2-devel

%define _extension_dir %{_datadir}/nautilus-python/extensions
%description
Nautilus extension for integration with pynapi.

%prep
%setup -q -c -T

%install
install -d %{buildroot}/%{_extension_dir}
install -t %{buildroot}/%{_extension_dir} %{SOURCE0} 

%clean
rm -rf %{buildroot}

%files
%doc


%changelog
* Sat Mar  9 2013 maciek <maciek.borzecki@gmail.com> - 0.1-1
- Initial packaging of version 0.1

