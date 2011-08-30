%define		plugin	colorpicker
Summary:	A simple component to select color in the same way you select color in Adobe Photoshop
Name:		jquery-%{plugin}
Version:	2009.05.23
Release:	1
License:	MIT / GPL
Group:		Applications/WWW
Source0:	http://www.eyecon.ro/colorpicker/colorpicker.zip
# Source0-md5:	d420dbce14507a13417d88f6c955429c
URL:		http://www.eyecon.ro/colorpicker/
BuildRequires:	js
BuildRequires:	rpmbuild(macros) > 1.268
BuildRequires:	yuicompressor
Requires:	jquery >= 1.3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
A simple component to select color in the same way you select color in
Adobe Photoshop.

%package demo
Summary:	Demo for jQuery ColorPicker
Group:		Development
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for jQuery ColorPicker.

%prep
%setup -qc

%{__rm} images/Thumbs.db

# separate demo files
install -d demo
mv index.html images js css demo
install -d images css js

mv demo/js/%{plugin}.js js
mv demo/css/%{plugin}.css css

for img in $(sed -ne 's/.*url(\.\.\/images\/\(.*\)).*/\1/p' css/colorpicker.css); do
	mv demo/images/$img images
done
%{__rm} demo/js/jquery.js
ln -s %{_datadir}/jquery/jquery.js demo/js/jquery.js
ln -s %{_appdir}/%{plugin}.js demo/js/%{plugin}.js
ln -s %{_appdir}/css/%{plugin}.css demo/css/%{plugin}.css
for img in images/*; do
	ln -s %{_appdir}/$img demo/$img
done

%build
install -d build/css
# compress .js
yuicompressor --charset UTF-8 js/%{plugin}.js -o build/%{plugin}.js
js -C -f build/%{plugin}.js

# compress .css
yuicompressor --charset UTF-8 css/%{plugin}.css -o build/css/%{plugin}.css

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_examplesdir}/%{name}-%{version}}
cp -a build/* $RPM_BUILD_ROOT%{_appdir}
cp -a images $RPM_BUILD_ROOT%{_appdir}

cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_appdir}

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
