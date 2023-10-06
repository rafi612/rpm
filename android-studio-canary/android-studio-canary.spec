# setting some global constants
%global appname studio

# disable debuginfo subpackage
%global debug_package %{nil}
# Disable build-id symlinks to avoid conflicts
%global _build_id_links none
# don't strip bundled binaries because pycharm checks length (!!!) of binary fsnotif
# and if you strip debug stuff from it, it will complain
%global __strip /bin/true
# dont repack jars
%global __jar_repack %{nil}
# disable rpath checks
%define __brp_check_rpaths %{nil}
# there are some python 2 and python 3 scripts so there is no way out to bytecompile them ^_^
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
# do not automatically detect and export provides and dependencies on bundled libraries and executables
%global __provides_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*
%global __requires_exclude_from %{_javadir}/%{name}/jbr/.*|%{_javadir}/%{name}/lib/.*|%{_javadir}/%{name}/plugins/.*

Name:          android-studio-canary
Version:       2023.2.1.7
Release:       1%{?dist}
Summary:       Integrated development environment for Google's Android platform - Canary branch
License:       Proprietary
URL:           https://developer.android.com/%{appname}/

Source0:       https://dl.google.com/android/studio/ide-zips/%{version}/android-studio-%{version}-linux.tar.gz

Source101:     %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: librsvg2-tools
BuildRequires: python3-devel
BuildRequires: javapackages-filesystem

Requires:      hicolor-icon-theme
Requires:      javapackages-filesystem

%description
Official Integrated Development Environment (IDE) for developing
applications. The IDE is based on IntelliJ IDEA, and provides
features on top of its powerful code editor and developer tools
to enhance the productivity of the Android application developers

%package doc
Summary:       Documentation for Android Studio Canary
BuildArch:     noarch

%description doc
This package contains documentation for Android Studio Canary

%prep
%setup -q -n android-studio

# Patching shebangs...
%if 0%{?fedora}
%py3_shebang_fix bin
%else
find bin -type f -name "*.py" -exec sed -e 's@/usr/bin/env python.*@%{__python3}@g' -i "{}" \;
%endif

%install
# Installing application...
install -d %{buildroot}%{_javadir}/%{name}
cp -arf ./{bin,jbr,lib,plugins,build.txt,product-info.json} %{buildroot}%{_javadir}/%{name}/

# Installing icons...
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 -p bin/%{appname}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -m 0644 -p bin/%{appname}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Creating additional PNG icons on the fly...
for size in 16 22 24 32 48 64 128 256; do
    dest=%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
    install -d ${dest}
    rsvg-convert -w ${size} -h ${size} bin/%{appname}.svg -o ${dest}/%{name}.png
    chmod 0644 ${dest}/%{name}.png
    touch -r bin/%{appname}.svg ${dest}/%{name}.png
done

# Installing launcher...
install -d %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/bin/%{appname}.sh %{buildroot}%{_bindir}/%{name}

# Installing desktop file...
install -d %{buildroot}%{_datadir}/applications
install -m 0644 -p %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license license/*
%{_javadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files doc
%doc *.txt

%changelog
* Fri Oct 06 2023 M3DZIK <me@medzik.dev> - 2023.2.1.7
- Update to 2023.2.1.7

* Fri Sep 29 2023 M3DZIK <me@medzik.dev> - 2023.2.1.6
- Update to 2023.2.1.6

* Fri Sep 22 2023 M3DZIK <me@medzik.dev> - 2023.2.1.5
- Update to 2023.2.1.5

* Sat Sep 16 2023 M3DZIK <me@medzik.dev> - 2023.2.1.4
- Update to 2023.2.1.4

* Fri Sep 08 2023 M3DZIK <me@medzik.dev> - 2023.2.1.3
- Update to 2023.2.1.3

* Thu Sep 07 2023 M3DZIK <me@medzik.dev> - 2023.2.1.2
- Update to 2023.2.1.2

* Sun Sep 03 2023 M3DZIK <me@medzik.dev> - 2023.2.1.1
- Initial release
