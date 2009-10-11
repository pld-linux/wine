#
# Conditional build:
%bcond_without	alsa		# don't build ALSA mm driver
%bcond_without	jack		# don't build JACK mm driver
%bcond_without	nas		# don't build NAS mm driver
%bcond_without	sane		# don't build TWAIN DLL with scanning support (through SANE)
%bcond_without	cups		# without CUPS printing support in winspool,wineps DLLs
#
# TODO:
# - support for CAPI (ISDN support; --with-capi)
#
# NOTE: wine detects the following SONAMES for dlopen at build time:
#   libcrypto,libssl (wininet.dll)
#   libcups (winspool.dll.so,wineps.dll.so)
#   libcurses/libncurses (wineconsole program)
#   libfontconfig (gdi32.dll.so)
#   libfreetype (wineps.dll.so,gdi32.dll.so)
#   libGL (x11drv.dll.so,ddraw.dll.so)
#   libjack (winejack.drv.so - explicit dependency in subpackage)
#   libX11, libXext, libXi, libXrender (x11drv.dll.so)
# thus requires rebuild after change of any of the above.
#
# JACK requires ALSA
%if %{without alsa}
%undefine	with_jack
%endif
Summary:	Program that lets you launch Win applications
Summary(es.UTF-8):	Ejecuta programas Windows en Linux
Summary(pl.UTF-8):	Program pozwalający uruchamiać aplikacje Windows
Summary(pt_BR.UTF-8):	Executa programas Windows no Linux
Name:		wine
Version:	1.1.31
Release:	1
Epoch:		1
License:	LGPL
Group:		Applications/Emulators
Source0:	http://ibiblio.org/pub/linux/system/emulators/wine/%{name}-%{version}.tar.bz2
# Source0-md5:	87fb94c218e52dd67c75b4ae5ef50c0e
Source1:	%{name}-uninstaller.desktop
Patch0:		%{name}-fontcache.patch
Patch1:		%{name}-makedep.patch
Patch2:		%{name}-ncurses.patch
Patch4:		%{name}-disable-valgrind.patch
Patch5:		%{name}-ca_certificates.patch
Patch6:		%{name}-notarget.patch
Patch7:		%{name}-manpaths.patch
#PatchX:	%{name}-dga.patch
URL:		http://www.winehq.org/
BuildRequires:	OpenGL-GLU-devel
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%{?with_arts:BuildRequires:	artsc-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	fontforge
BuildRequires:	freetype-devel >= 2.0.5
BuildRequires:	giflib-devel
BuildRequires:	gnutls-devel
BuildRequires:	hal-devel
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	lcms-devel
BuildRequires:	libgphoto2-devel
BuildRequires:	libgsm-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmpg123-devel
BuildRequires:	libtool
BuildRequires:	libxslt-devel
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	ncurses-devel
# db2* failed previously - probably openjade or opensp bug
BuildRequires:	openjade >= 1:1.3.3-0.pre1
BuildRequires:	openldap-devel
BuildRequires:	opensp >= 1:1.5.1
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
%{?with_sane:BuildRequires:	sane-backends-devel}
BuildRequires:	unixODBC-devel >= 2.2.12-2
#BuildRequires:	valgrind
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXxf86dga-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
Requires:	libfreetype.so.6
Suggests:	binfmt-detector
Suggests:	ca-certificates
Conflicts:	ca-certificates < 20080809-4
# for winelauncher
Suggests:	xorg-app-xmessage
# for ntlm_auth
Suggests:	samba-common >= 1:3.0.25
# link to wine/ntdll.dll.so, without any SONAME
Provides:	libntdll.dll.so
Obsoletes:	wine-doc-pdf
Obsoletes:	wine-drv-arts
ExclusiveArch:	%{ix86}
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep		libGL.so.1 libGLU.so.1
%define		no_install_post_strip	1

%define		_winedir		%{_datadir}/%{name}

%define		getsoname()	%((objdump -p %{1} 2>/dev/null || echo SONAME ERROR) | awk '/SONAME/ { print $2; s=1 }; END { if(s==0) print "ERROR" }')

%undefine	debuginfocflags

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

%package programs
Summary:	Wine - programs
Summary(pl.UTF-8):	Wine - programy
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description programs
Wine - programs.

%description programs -l pl.UTF-8
Wine - programy.

%package dll-d3d
Summary:	Direct3D implementation DLLs for Wine
Summary(pl.UTF-8):	Biblioteki DLL z implementacją Direct3D dla Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	OpenGL

%description dll-d3d
Direct3D implementation DLLs for Wine (through OpenGL).

%description dll-d3d -l pl.UTF-8
Biblioteki DLL z implementacją Direct3D dla Wine (poprzez OpenGL).

%package dll-gl
Summary:	OpenGL implementation DLLs for Wine
Summary(pl.UTF-8):	Biblioteki DLL z implementacją OpenGL dla Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	OpenGL

%description dll-gl
OpenGL implementation DLLs for Wine.

%description dll-gl -l pl.UTF-8
Biblioteki DLL z implementacją OpenGL dla Wine.

%package dll-twain
Summary:	TWAIN implementation DLL for Wine
Summary(pl.UTF-8):	Biblioteka DLL z implementacją TWAIN dla Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dll-twain
TWAIN implementation DLL for Wine (through SANE).

%description dll-twain -l pl.UTF-8
Biblioteka DLL z implementacją TWAIN dla Wine (poprzez SANE).

%package drv-alsa
Summary:	ALSA driver for WINE mm.dll implementation
Summary(pl.UTF-8):	Sterownik ALSA dla implementacji mm.dll w Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description drv-alsa
ALSA driver for WINE mm.dll (multimedia system) implementation.

%description drv-alsa -l pl.UTF-8
Sterownik ALSA dla implementacji mm.dll (systemu multimediów) w Wine.

%package drv-jack
Summary:	JACK driver for WINE mm.dll implementation
Summary(pl.UTF-8):	Sterownik JACK-a dla implementacji mm.dll w Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	jack-audio-connection-kit
# dlopened by SONAME detected at build time
%{?with_jack:Requires:	%{getsoname /usr/%{_lib}/libjack.so}}

%description drv-jack
JACK driver for WINE mm.dll (multimedia system) implementation.

%description drv-jack -l pl.UTF-8
Sterownik JACK-a dla implementacji mm.dll (systemu multimediów) w
Wine.

%package drv-nas
Summary:	NAS driver for WINE mm.dll implementation
Summary(pl.UTF-8):	Sterownik NAS dla implementacji mm.dll w Wine
Group:		Applications/Emulators
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description drv-nas
NAS driver for WINE mm.dll (multimedia system) implementation.

%description drv-nas -l pl.UTF-8
Sterownik NAS dla implementacji mm.dll (systemu multimediów) w Wine.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# turn off compilation of some tools
sed -i -e "s|winetest \\\|\\\|;s|avitools||" programs/Makefile.in
#sed -i -e "s|avitools||" programs/Makefile.in

%build
%{__autoconf}
%{__autoheader}
%configure \
	--with%{!?with_alsa:out}-alsa \
	--with-audioio \
	--without-capi \
	--with-cms \
	--with-coreaudio \
	--with%{!?with_cups:out}-cups \
	--with-curses \
	--with-esd \
	--with-fontconfig \
	--with-freetype \
	--with-glu \
	--with-gnutls \
	--with-gphoto \
	--with-gsm \
	--with-hal \
	--with%{!?with_jack:out}-jack \
	--with-jpeg \
	--with-ldap \
	--with-mpg123 \
	--with%{!?with_nas:out}-nas \
	--with-opengl \
	--with-openssl \
	--with-oss \
	--with-png \
	--with-pthread \
	--with%{!?with_sane:out}-sane \
	--with-xcomposite \
	--with-xcursor \
	--with-xinerama \
	--with-xinput \
	--with-xml \
	--with-xrandr \
	--with-xrender \
	--with-xshape \
	--with-xshm \
	--with-xslt \
	--with-xxf86vm \
	--with-x
%{__make} depend
%{__make}
%{__make} -C programs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_aclocaldir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C programs install \
	DESTDIR=$RPM_BUILD_ROOT

install tools/fnt2bdf			$RPM_BUILD_ROOT%{_bindir}

install aclocal.m4 $RPM_BUILD_ROOT%{_aclocaldir}/wine.m4

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

%if %{?debug:0}%{!?debug:1}
echo "Strip executable binaries and shared object files."
filelist=`find $RPM_BUILD_ROOT -type f ! -regex ".*ld-[0-9.]*so.*"`
elfexelist=`echo $filelist | xargs -r file | \
	awk '/ELF.*executable/ {print $1}' | cut -d: -f1`
elfsharedlist=`echo $filelist | xargs -r file | \
	awk '/LF.*shared object/ {print $1}' | cut -d: -f1`; \
if [ -n "$elfexelist" ]; then \
	strip -R .note -R .comment $elfexelist
fi
if [ -n "$elfsharedlist" ]; then
	strip --strip-unneeded -R .note -R .comment $elfsharedlist
fi
%endif

# /sbin/chstk -e $RPM_BUILD_ROOT%{_bindir}/wine

programs="msiexec notepad regedit regsvr32 wineboot winecfg wineconsole winedbg winefile winemine winepath"

BZZZ=`pwd`
rm -f files.so;		touch files.so
rm -f files.programs;	touch files.programs
cd $RPM_BUILD_ROOT%{_libdir}/wine
for f in *.so; do
	case $f in
		d3d8.dll.so|d3d9.dll.so|d3dx8.dll.so|glu32.dll.so|opengl32.dll.so|sane.ds.so|twain.dll.so|twain_32.dll.so|winealsa.drv.so|winejack.drv.so|winenas.drv.so)
			;;
		*)
			echo "%attr(755,root,root) %{_libdir}/wine/$f" >>$BZZZ/files.so
	esac
done
cd -
for p in $programs; do
	echo "%attr(755,root,root) %{_bindir}/$p" >> files.programs
	echo "%attr(755,root,root) %{_libdir}/wine/$p.exe.so" >> files.programs
	grep -v "$p\.exe\.so$" files.so > files.so.
	mv -f files.so. files.so
done

install -d $RPM_BUILD_ROOT%{_pixmapsdir}/wine.svg
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install programs/winetest/winetest.svg $RPM_BUILD_ROOT%{_pixmapsdir}/wine.svg

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%triggerpostun -- wine < 1:0.9.12-1.9
rm -f /var/lock/subsys/wine
if [ -x /sbin/chkconfig ]; then
	/sbin/chkconfig --del wine
fi

%files -f files.so
%defattr(644,root,root,755)
%doc README documentation/ChangeLog* AUTHORS ANNOUNCE
%lang(de) %doc documentation/README.de
%lang(es) %doc documentation/README.es
%lang(fr) %doc documentation/README.fr
%lang(it) %doc documentation/README.it
%lang(ko) %doc documentation/README.ko
%lang(nb) %doc documentation/README.no
%lang(pt) %doc documentation/README.pt
%lang(pt_BR) %doc documentation/README.pt_br
%attr(755,root,root) %{_bindir}/msiexec
%attr(755,root,root) %{_bindir}/wine
%attr(755,root,root) %{_bindir}/wineboot
%attr(755,root,root) %{_bindir}/winecfg
%attr(755,root,root) %{_bindir}/winedbg
#%attr(755,root,root) %{_bindir}/wine-kthread
#%attr(755,root,root) %{_bindir}/winelauncher
%attr(755,root,root) %{_bindir}/wineprefixcreate
%attr(755,root,root) %{_bindir}/wine-preloader
#%attr(755,root,root) %{_bindir}/wine-pthread
%attr(755,root,root) %{_bindir}/wineserver
%attr(755,root,root) %{_libdir}/*.so*
%dir %{_libdir}/wine
%{_libdir}/wine/*.dll16
#%{_libdir}/wine/*.drv16
%{_libdir}/wine/*.exe16
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/fakedlls/*.acm
%{_libdir}/wine/fakedlls/*.cpl
%{_libdir}/wine/fakedlls/*.dll
%{_libdir}/wine/fakedlls/*.dll16
%{_libdir}/wine/fakedlls/*.drv
%{_libdir}/wine/fakedlls/*.drv16
%{_libdir}/wine/fakedlls/*.ds
%{_libdir}/wine/fakedlls/*.exe
%{_libdir}/wine/fakedlls/*.exe16
%{_libdir}/wine/fakedlls/*.mod16
%{_libdir}/wine/fakedlls/*.ocx
%{_libdir}/wine/fakedlls/*.sys
%{_libdir}/wine/fakedlls/*.tlb
%{_libdir}/wine/fakedlls/*.vxd
%{_mandir}/man1/wine.1*
%lang(de) %{_mandir}/de/man1/wine.1*
%lang(fr) %{_mandir}/fr/man1/wine.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineprefixcreate.1*
%{_mandir}/man1/wineserver.1*
%lang(fr) %{_mandir}/fr/man1/wineserver.1*
%{_winedir}
%{_desktopdir}/wine.desktop
%{_desktopdir}/wine-uninstaller.desktop
%{_pixmapsdir}/wine.svg

%files programs -f files.programs
%defattr(644,root,root,755)

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fnt2bdf
%attr(755,root,root) %{_bindir}/function_grep.pl
%attr(755,root,root) %{_bindir}/widl
%attr(755,root,root) %{_bindir}/winebuild
%attr(755,root,root) %{_bindir}/winedump
%attr(755,root,root) %{_bindir}/wineg++
%attr(755,root,root) %{_bindir}/winegcc
%attr(755,root,root) %{_bindir}/winemaker
%attr(755,root,root) %{_bindir}/winecpp
#%attr(755,root,root) %{_bindir}/winewrap
%attr(755,root,root) %{_bindir}/wmc
%attr(755,root,root) %{_bindir}/wrc
%{_libdir}/wine/lib*.def
# no shared variants, so not separated
%{_libdir}/wine/lib*.def.a
%{_libdir}/wine/libadsiid.a
%{_libdir}/wine/libdx*.a
%{_libdir}/wine/libstrmiids.a
%{_libdir}/wine/libuuid.a
%{_libdir}/wine/libwinecrt0.a
%{_includedir}/wine
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/wineg++.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_aclocaldir}/*.m4

%files dll-d3d
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/d3d8.dll.so
%attr(755,root,root) %{_libdir}/wine/d3d9.dll.so
%attr(755,root,root) %{_libdir}/wine/wined3d.dll.so

%files dll-gl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/glu32.dll.so
%attr(755,root,root) %{_libdir}/wine/opengl32.dll.so

%if %{with sane}
%files dll-twain
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/sane.ds.so
%attr(755,root,root) %{_libdir}/wine/twain*.dll.so
%endif

%if %{with alsa}
%files drv-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/winealsa.drv.so
%endif

%if %{with jack}
%files drv-jack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/winejack.drv.so
%endif

%if %{with nas}
%files drv-nas
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/wine/winenas.drv.so
%endif

# additional dependencies in *.so not separated (yet?) from main package
#   ddraw.dll.so,x11drv.dll.so depend on X11 libs
#   ole2disp.dll.so,oleaut32.dll.so,typelib.dll.so depend on lib(un)gif,libjpeg,libX11
#   ttydrv.dll.so depends on ncurses
