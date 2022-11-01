#
# todo:
# libvkd3d https://wiki.winehq.org/Vkd3d
#
# Conditional build:
%bcond_with	capi		# don't build CAPI 2.0 (ISDN) support
%bcond_without	gstreamer	# don't build GStreamer filters support
%bcond_without	sane		# don't build TWAIN DLL with scanning support (through SANE)
%bcond_without	ldap		# don't build LDAP DLL
%bcond_without	cups		# without CUPS printing support in winspool,wineps DLLs
%bcond_without	netapi		# don't use the Samba NetAPI library
#
# NOTE: wine detects the following SONAMES for dlopen at build time:
#   libGL (winex11.drv.so)
#   libOSMesa (gdi32.dll.so)
#   libX11 libXcomposite libXcursor libXext libXi libXinerama libXrandr libXrender libXxf86vm (winex11.drv.so)
#   libcapi20 (capi2032.dll.so)
#   libcups (winspool.drv.so)
#   libdbus (mountmgr.sys.so)
#   libfontconfig (gdi32.dll.so)
#   libfreetype (gdi32.dll.so)
#   libgnutls (secur32.dll.so)
#   libncurses (kernel32.dll.so)
#   libodbc (odbc32.dll.so)
#   libsane (sane.ds.so)
#   libtiff (windowscodecs.dll.so)
# thus requires rebuild after change of any of the above.

# library qualifier in rpm generated deps
%ifarch %{x8664} ia64 ppc64 s390x sparc64
%define	libqual ()(64bit)
%else
%define	libqual %{nil}
%endif

%ifarch %{x8664}
%define	winelib	x86_64
%else
%define	winelib	i386
%endif

%define		gecko_ver	2.47.3
Summary:	Program that lets you launch Win applications
Summary(es.UTF-8):	Ejecuta programas Windows en Linux
Summary(pl.UTF-8):	Program pozwalający uruchamiać aplikacje Windows
Summary(pt_BR.UTF-8):	Executa programas Windows no Linux
Name:		wine
Version:	7.20
Release:	1
Epoch:		1
License:	LGPL
Group:		Applications/Emulators
Source0:	https://dl.winehq.org/wine/source/7.x/%{name}-%{version}.tar.xz
# Source0-md5:	915ad9fedfeef1dfd8b19d2e774086ec
Source1:	https://dl.winehq.org/wine/wine-gecko/%{gecko_ver}/%{name}-gecko-%{gecko_ver}-x86.msi
# Source1-md5:	e8bf0350695a633e15877684d5b97baf
Source2:	https://dl.winehq.org/wine/wine-gecko/%{gecko_ver}/%{name}-gecko-%{gecko_ver}-x86_64.msi
# Source2-md5:	ed0fa1f498a4b272b1cf8db14f71701a
Source3:	%{name}-uninstaller.desktop
Patch0:		%{name}-gphoto2_bool.patch
Patch1:		%{name}-makedep.patch
Patch2:		%{name}-ncurses.patch
Patch4:		%{name}-disable-valgrind.patch
Patch5:		%{name}-ca_certificates.patch
Patch6:		desktop.patch
Patch7:		%{name}-wine64_man.patch
URL:		http://www.winehq.org/
BuildRequires:	Mesa-libOSMesa-devel
BuildRequires:	OpenAL-devel >= 1.1
BuildRequires:	OpenCL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL2-devel
BuildRequires:	alsa-lib-devel
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake
BuildRequires:	bison
%{?with_capi:BuildRequires:	capi4k-utils-devel}
BuildRequires:	clang
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	dbus-devel
BuildRequires:	flex >= 2.5.33
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.0.5
BuildRequires:	gettext-devel
%ifarch %{x8664}
BuildRequires:	gcc >= 6:4.4
%endif
BuildRequires:	gettext-tools
BuildRequires:	gnutls-devel
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 1.0}
%{?with_gstreamer:BuildRequires:	gstreamer-plugins-base-devel >= 1.0}
# for icotool used in build
BuildRequires:	icoutils >= 0.29.0
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libcap-devel
BuildRequires:	libglvnd-libEGL-devel
BuildRequires:	libgphoto2-devel
BuildRequires:	libpcap-devel
BuildRequires:	libv4l-devel
BuildRequires:	lld
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	samba-devel
%{?with_sane:BuildRequires:	sane-backends-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildConflicts:	crossmingw32-gcc
BuildConflicts:	crossmingw64-gcc
Requires:	OpenGL
Requires:	libfreetype.so.6%{libqual}
Requires:	libpng16.so.16%{libqual}
Requires(post):	/sbin/ldconfig
Suggests:	binfmt-detector
Suggests:	ca-certificates
Suggests:	cabextract
Conflicts:	ca-certificates < 20080809-4
# for printing needs lpr
Suggests:	cups-clients
# for winelauncher
Suggests:	xorg-app-xmessage
# for ntlm_auth
Suggests:	samba-common >= 1:3.0.25
# link to wine/ntdll.dll.so, without any SONAME
Provides:	libntdll.dll.so
Obsoletes:	wine-dll-d3d < 1:7.7-2
Obsoletes:	wine-dll-gl < 1:7.7-2
Obsoletes:	wine-doc-pdf < 1:7.7-2
Obsoletes:	wine-drv-alsa < 1:7.7-2
Obsoletes:	wine-drv-arts < 1:7.7-2
Obsoletes:	wine-drv-jack < 1:7.7-2
Obsoletes:	wine-drv-nas < 1:7.7-2
Obsoletes:	wine-programs < 1:7.7-2
ExclusiveArch:	%{ix86} %{x8664} arm
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_noautoprov	elf\\\\(buildid\\\\)

%define		_winedir		%{_datadir}/%{name}

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library that implements Windows API calls using
their Unix or X11 equivalents. The library may also be used for
porting Win32 code into native Unix executables.

%description -l es.UTF-8
Ejecuta programas Windows en Linux.

%description -l pl.UTF-8
Wine jest programem dzięki któremu można uruchamiać programy napisane
dla Microsoft Windows pod systemami uniksowymi. Składa się on z
loadera, który pozwala wczytywać i uruchamiać programy w formacie
Microsoft Windows, oraz z biblioteki, która implementuje API Windows
przy użyciu odpowiedników uniksowych oraz z X11. Biblioteka może być
także wykorzystana do przenoszenia aplikacji Win32 do Uniksa.

%description -l pt_BR.UTF-8
O Wine é um programa que permite rodar programas MS-Windows no X11.
Ele consiste de um carregador de programa, que carrega e executa um
binário MS-Windows, e de uma biblioteca de emulação que traduz as
chamadas da API para as equivalentes Unix/X11.

%package devel
Summary:	Wine - header files
Summary(es.UTF-8):	Biblioteca de desarrollo de wine
Summary(pl.UTF-8):	Wine - pliki nagłowkowe
Summary(pt_BR.UTF-8):	Biblioteca de desenvolvimento do wine
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Wine - header files.

%description devel -l es.UTF-8
Biblioteca de desarrollo de wine.

%description devel -l pl.UTF-8
Wine - pliki nagłówkowe.

%description devel -l pt_BR.UTF-8
Arquivos de inclusão e bibliotecas para desenvolver aplicações com o
WINE.

%package dll-capi
Summary:	CAPI 2.0 (ISDN) implementation DLLs for Wine
Summary(pl.UTF-8):	Biblioteki DLL z implementacją CAPI 2.0 (ISDN) dla Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dll-capi
CAPI 2.0 (ISDN) implementation DLLs for Wine.

%description dll-capi -l pl.UTF-8
Biblioteki DLL z implementacją CAPI 2.0 (ISDN) dla Wine.

%package dll-twain
Summary:	TWAIN implementation DLL for Wine
Summary(pl.UTF-8):	Biblioteka DLL z implementacją TWAIN dla Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dll-twain
TWAIN implementation DLL for Wine (through SANE).

%description dll-twain -l pl.UTF-8
Biblioteka DLL z implementacją TWAIN dla Wine (poprzez SANE).

%package dll-ldap
Summary:	Win32 LDAP API DLL for Wine
Summary(pl.UTF-8):	Biblioteka DLL z implementacją API Win32 LDAP dla Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dll-ldap
Lightweight Directory Access Protocol Library for Wine.

%description dll-ldap -l pl.UTF-8
Biblioteka LDAP (Lightweight Directory Access Protocol) dla Wine.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%ifarch %{x8664}
%patch7 -p1
%endif

%build

#workaround for icon extraction error.
icotool -x -o . dlls/user32/resources/oic_winlogo.ico
mv -f oic_winlogo_*32x32x32.png %{name}.png
rm -f oic_winlogo_*.png

%{__autoconf}
%{__autoheader}
%configure \
%ifarch %{x8664}
	--enable-win64 \
%endif
	--with-alsa \
	--with-capi%{!?with_capi:=no} \
	--with-coreaudio \
	--with-cups%{!?with_cups:=no} \
	--with-dbus \
	--with-fontconfig \
	--with-freetype \
	--with-gphoto \
	--with-gnutls \
	%{__with_without gstreamer} \
	--with-ldap%{!?with_ldap:=no} \
	--with%{!?with_netapi:out}-netapi \
	--with-openal \
	--with-opencl \
	--with-opengl \
	--with-osmesa \
	--with-pcap \
	--with-pthread \
	--with-pulse \
	--with%{!?with_sane:out}-sane \
	--with-xcomposite \
	--with-xcursor \
	--with-xinerama \
	--with-xinput \
	--with-xinput2 \
	--with-xrandr \
	--with-xrender \
	--with-xshape \
	--with-xshm \
	--with-xxf86vm \
	--with-x

%{__make} depend
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_aclocaldir}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p tools/sfnt2fon/sfnt2fon $RPM_BUILD_ROOT%{_bindir}
cp -a aclocal.m4 $RPM_BUILD_ROOT%{_aclocaldir}/wine.m4

install -d \
	$RPM_BUILD_ROOT%{_winedir}/windows/{system,Desktop,Favorites,Fonts} \
	"$RPM_BUILD_ROOT%{_winedir}/windows/Start Menu/Programs/Startup" \
	$RPM_BUILD_ROOT%{_winedir}/windows/{SendTo,ShellNew,system32,NetHood} \
	$RPM_BUILD_ROOT%{_winedir}/windows/{Profiles/Administrator,Recent} \
	$RPM_BUILD_ROOT%{_winedir}/{"Program Files/Common Files","My Documents"}

touch $RPM_BUILD_ROOT%{_winedir}/{autoexec.bat,config.sys,windows/win.ini}
touch $RPM_BUILD_ROOT%{_winedir}/windows/system/{shell.dll,shell32.dll}
touch $RPM_BUILD_ROOT%{_winedir}/windows/system/{winsock.dll,wsock32.dll}

cat > $RPM_BUILD_ROOT%{_winedir}/windows/system.ini <<'EOF'
[mci]
cdaudio=mcicda.drv
sequencer=mciseq.drv
waveaudio=mciwave.drv
avivideo=mciavi.drv
videodisc=mcipionr.drv
vcr=mciviscd.drv
MPEGVideo=mciqtz.drv
EOF

# /sbin/chstk -e $RPM_BUILD_ROOT%{_bindir}/wine

for dir in $RPM_BUILD_ROOT%{_mandir}/*.UTF-8 ; do
	mv "$dir" "${dir%.UTF-8}"
done

%ifarch %{x8664}
cp -p loader/wine.man $RPM_BUILD_ROOT%{_mandir}/man1/wine64.1
for lang in de fr pl ; do
install -d $RPM_BUILD_ROOT%{_mandir}/${lang}/man1
cp -p loader/wine.${lang}.UTF-8.man $RPM_BUILD_ROOT%{_mandir}/${lang}/man1/wine64.1
done
%else
cp -p loader/wine.man $RPM_BUILD_ROOT%{_mandir}/man1/wine.1
for lang in de fr pl ; do
install -d $RPM_BUILD_ROOT%{_mandir}/${lang}/man1
cp -p loader/wine.${lang}.UTF-8.man $RPM_BUILD_ROOT%{_mandir}/${lang}/man1/wine.1
done
%endif

install -d $RPM_BUILD_ROOT%{_winedir}/gecko
%ifnarch %{x8664}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_winedir}/gecko
%else
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_winedir}/gecko
%endif

install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{name}.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database

%postun -p /sbin/ldconfig

%triggerpostun -- wine < 1:0.9.12-1.9
rm -f /var/lock/subsys/wine
if [ -x /sbin/chkconfig ]; then
	/sbin/chkconfig --del wine
fi

%files
%defattr(644,root,root,755)
%doc README AUTHORS ANNOUNCE
%lang(de) %doc documentation/README.de
%lang(es) %doc documentation/README.es
%lang(fr) %doc documentation/README.fr
%lang(hu) %doc documentation/README.hu
%lang(it) %doc documentation/README.it
%lang(ko) %doc documentation/README.ko
%lang(nb) %doc documentation/README.no
%lang(pt) %doc documentation/README.pt
%lang(pt_BR) %doc documentation/README.pt_br
%lang(ru) %doc documentation/README.ru
%lang(sv) %doc documentation/README.sv
%lang(tr) %doc documentation/README.tr
%attr(755,root,root) %{_bindir}/msidb
%attr(755,root,root) %{_bindir}/msiexec
%attr(755,root,root) %{_bindir}/notepad
%attr(755,root,root) %{_bindir}/regedit
%attr(755,root,root) %{_bindir}/regsvr32
%ifnarch %{x8664}
%attr(755,root,root) %{_bindir}/wine
%else
%attr(755,root,root) %{_bindir}/wine64
%endif
%attr(755,root,root) %{_bindir}/wineboot
%attr(755,root,root) %{_bindir}/winecfg
%attr(755,root,root) %{_bindir}/wineconsole
%attr(755,root,root) %{_bindir}/winedbg
%attr(755,root,root) %{_bindir}/winefile
%attr(755,root,root) %{_bindir}/winemine
%attr(755,root,root) %{_bindir}/winepath
%ifnarch %{x8664}
%attr(755,root,root) %{_bindir}/wine-preloader
%else
%attr(755,root,root) %{_bindir}/wine64-preloader
%endif
%attr(755,root,root) %{_bindir}/wineserver
%dir %{_libdir}/wine
%dir %{_libdir}/wine/%{winelib}-unix
%attr(755,root,root) %{_libdir}/wine/%{winelib}-unix/*.so*
%dir %{_libdir}/wine/%{winelib}-windows
%{_libdir}/wine/%{winelib}-windows/*.acm
%{_libdir}/wine/%{winelib}-windows/*.ax
%{_libdir}/wine/%{winelib}-windows/*.com
%{_libdir}/wine/%{winelib}-windows/*.cpl
%{_libdir}/wine/%{winelib}-windows/*.dll
%ifarch %{ix86}
%{_libdir}/wine/%{winelib}-windows/*.dll16
%endif
%{_libdir}/wine/%{winelib}-windows/*.drv
%ifarch %{ix86}
%{_libdir}/wine/%{winelib}-windows/*.drv16
%endif
%{_libdir}/wine/%{winelib}-windows/*.ds
%{_libdir}/wine/%{winelib}-windows/*.exe
%ifarch %{ix86}
%{_libdir}/wine/%{winelib}-windows/*.exe16
%{_libdir}/wine/%{winelib}-windows/*.mod16
%endif
%{_libdir}/wine/%{winelib}-windows/*.msstyles
%{_libdir}/wine/%{winelib}-windows/*.ocx
%{_libdir}/wine/%{winelib}-windows/*.sys
%{_libdir}/wine/%{winelib}-windows/*.tlb
%ifarch %{ix86}
%{_libdir}/wine/%{winelib}-windows/*.vxd
%endif
%if %{with capi}
%exclude %{_libdir}/wine/%{winelib}-windows/capi2032.dll
%exclude %{_libdir}/wine/%{winelib}-unix/capi2032.so
%endif
%if %{with sane}
%exclude %{_libdir}/wine/%{winelib}-unix/sane.so
%exclude %{_libdir}/wine/%{winelib}-windows/twain*.dll
%ifarch %{ix86}
%exclude %{_libdir}/wine/%{winelib}-windows/twain*.dll16
%endif
%endif
%if %{with ldap}
%exclude %{_libdir}/wine/%{winelib}-unix/wldap*.so
%exclude %{_libdir}/wine/%{winelib}-windows/wldap*.dll
%endif
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%ifnarch %{x8664}
%{_mandir}/man1/wine.1*
%lang(de) %{_mandir}/de/man1/wine.1*
%lang(fr) %{_mandir}/fr/man1/wine.1*
%lang(pl) %{_mandir}/pl/man1/wine.1*
%else
%{_mandir}/man1/wine64.1*
%lang(de) %{_mandir}/de/man1/wine64.1*
%lang(fr) %{_mandir}/fr/man1/wine64.1*
%lang(pl) %{_mandir}/pl/man1/wine64.1*
%endif
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%{_mandir}/man1/wineserver.1*
%lang(de) %{_mandir}/de/man1/wineserver.1*
%lang(fr) %{_mandir}/fr/man1/wineserver.1*
%{_winedir}
%{_desktopdir}/wine.desktop
%{_desktopdir}/wine-uninstaller.desktop
%{_pixmapsdir}/%{name}.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sfnt2fon
%attr(755,root,root) %{_bindir}/function_grep.pl
%attr(755,root,root) %{_bindir}/widl
%attr(755,root,root) %{_bindir}/winebuild
%attr(755,root,root) %{_bindir}/winedump
%attr(755,root,root) %{_bindir}/wineg++
%attr(755,root,root) %{_bindir}/winegcc
%attr(755,root,root) %{_bindir}/winemaker
%attr(755,root,root) %{_bindir}/winecpp
%attr(755,root,root) %{_bindir}/wmc
%attr(755,root,root) %{_bindir}/wrc
# no shared variants, so not separated
%{_libdir}/wine/%{winelib}-unix/lib*.a
%{_libdir}/wine/%{winelib}-windows/lib*.a
%{_includedir}/wine
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/wineg++.1*
%{_mandir}/man1/winemaker.1*
%lang(de) %{_mandir}/de/man1/winemaker.1*
%lang(fr) %{_mandir}/fr/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_aclocaldir}/*.m4

%if %{with capi}
%files dll-capi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/%{winelib}-windows/capi2032.dll
%attr(755,root,root) %{_libdir}/wine/%{winelib}-unix/capi2032.so
%endif

%if %{with sane}
%files dll-twain
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/%{winelib}-unix/sane.so
%attr(755,root,root) %{_libdir}/wine/%{winelib}-windows/twain*.dll
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/wine/%{winelib}-windows/twain*.dll16
%endif
%endif

%if %{with ldap}
%files dll-ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/%{winelib}-unix/wldap*.so
%attr(755,root,root) %{_libdir}/wine/%{winelib}-windows/wldap*.dll
%endif

# additional dependencies in *.so not separated (yet?) from main package
#   ddraw.dll.so,winex11.drv.so depend on X11 libs
#   ole2disp.dll16.so,oleaut32.dll.so,typelib.dll16.so depend on libX11
