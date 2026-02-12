Name:       avm-libzip
Version:    @PROJECT_VERSION_MAJOR@.@PROJECT_VERSION_MINOR@.@PROJECT_VERSION_PATCH@
Release:    1%{?dist}
Summary:    ZipLib for AVM-Energo projects

License:    GPLv3
URL:        https://git.avmenergo.ru/avm-energo/libzip.git
Source0:    https://git.avmenergo.ru/avm-energo/libzip.git

BuildArch:  ${arch}
BuildRequires:  cmake
Requires:
Provides:   avm-libzip

%description
LibZip library for AVM-Energo projects

%prep
%{__rm} -rf
%{__tar} -xzvf %{SOURCE0} -C rpmbuild/BUILD --strip-components 1

%build
cd rpmbuild/BUILD
%cmake -DBUILD_SHARED_LIBS:BOOL=ON -DCMAKE_TOOLCHAIN_FILE=../../../cmake/arch/${arch}.cmake -DCMAKE_INSTALL_PREFIX=rpmbuild/BUILDROOT
%cmake_build

%install
%cmake_install

%package devel

%description devel
LibZip library development files for AVM-Energo projects

%files
%license add-license-file-here
rpmbuild/BUILDROOT/avm-libzip.so*

%changelog
* Tue Dec 30 2025 anton <vao@asu-vei.ru>
- initial rpm build
