Summary:	Program that lets you launch Win applications
Summary(es):	Ejecuta programas Windows en Linux
Summary(pl):	Program pozwalaj±cy uruchamiaæ aplikacje Windows
Summary(pt_BR):	Executa programas Windows no Linux
Name:		wine
Version:	20020804
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://metalab.unc.edu/pub/Linux/ALPHA/wine/development/Wine-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.reg
Source3:	%{name}.systemreg
Source4:	%{name}.userreg
Patch0:		%{name}-fontcache.patch
URL:		http://www.winehq.com/
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
%{!?_without_arts:BuildRequires:	arts-devel}
BuildRequires:	bison
BuildRequires:	chpax
%{!?_without_cups:BuildRequires:	cups-devel}
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.5
BuildRequires:	libjpeg-devel
BuildRequires:	ncurses-devel
BuildRequires:	openjade
%{!?_without_sane:BuildRequires:	sane-backends-devel}
Requires:	OpenGL
Requires(post):	ldconfig
Requires(post,preun):chkconfig
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep		libGL.so.1 libGLU.so.1
%define		no_install_post_strip	1

%define		_prefix			/usr/X11R6
%define		_mandir			%{_prefix}/man
%define		_winedir		%{_datadir}/%{name}

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library that implements Windows API calls using
their Unix or X11 equivalents. The library may also be used for
porting Win32 code into native Unix executables.

%description -l es
Ejecuta programas Windows en Linux.

%description -l pl
Wine jest programem dziêki któremu mo¿na uruchamiaæ programy napisane
dla Microsoft Windows pod systemami unixowymi. Sk³ada siê on z
loadera, który pozwala wczytywaæ i uruchamiaæ programy w formacie
Microsoft Windows oraz z biblioteki, która implementuje API Windows
przy u¿yciu odpowiedników Unixowych oraz z X11. Biblioteka mo¿e byæ
tak¿e wykorzystana do przenoszenia aplikacji Win32 do Unixa.

%description -l pt_BR
O Wine é um programa que permite rodar programas MS-Windows no X11.
Ele consiste de um carregador de programa, que carrega e executa um
binário MS-Windows, e de uma biblioteca de emulação que traduz as
chamadas da API para as equivalentes Unix/X11.

%package devel
Summary:	Wine - header files
Summary(es):	Biblioteca de desarrollo de wine
Summary(pl):	Wine - pliki nag³owkowe
Summary(pt_BR):	Biblioteca de desenvolvimento do wine
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Wine - header files.

%description devel -l es
Biblioteca de desarrollo de wine.

%description devel -l pl
Wine - pliki nag³ówkowe.

%description devel -l pt_BR
Arquivos de inclusão e bibliotecas para desenvolver aplicações com o
WINE.

%package programs
Summary:	Wine - programs
Summary(pl):	Wine - programy
Group:		Applications
Requires:	%{name} = %{version}

%description programs
Wine - programs

%description programs -l pl
Wine - programy

%prep
%setup -q
%patch -p1

# turn off compilation of some tools
sed -e "s|winetest \\\|\\\|;s|avitools||" programs/Makefile.in > .tmp
mv -f .tmp programs/Makefile.in

%build
#aclocal
#autoconf
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS
CFLAGS="%{rpmcflags} $CPPFLAGS"
%configure \
%{!?debug:	--disable-debug} \
%{!?debug:	--disable-trace} \
	--enable-curses \
	--enable-opengl \
	--with-x

%{__make} depend
%{__make}
%{__make} -C programs

cd documentation
./db2html-winehq wine-user.sgml
./db2html-winehq wine-devel.sgml
./db2html-winehq winelib-user.sgml

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec-prefix=$RPM_BUILD_ROOT%{_exec_prefix} \
        bindir=$RPM_BUILD_ROOT%{_bindir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}/wine \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
	localstatedir=$RPM_BUILD_ROOT%{_localstatedir} \
	sharedstatedir=$RPM_BUILD_ROOT%{_sharedstatedir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	dlldir=$RPM_BUILD_ROOT%{_libdir}/wine

%{__make} -C programs install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec-prefix=$RPM_BUILD_ROOT%{_exec_prefix} \
        bindir=$RPM_BUILD_ROOT%{_bindir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}/wine \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
	localstatedir=$RPM_BUILD_ROOT%{_localstatedir} \
	sharedstatedir=$RPM_BUILD_ROOT%{_sharedstatedir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	dlldir=$RPM_BUILD_ROOT%{_libdir}/wine

install programs/winhelp/hlp2sgml	$RPM_BUILD_ROOT%{_bindir}
install tools/fnt2bdf			$RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d \
        $RPM_BUILD_ROOT%{_winedir}/windows/{system,Desktop,Favorites,Fonts} \
        "$RPM_BUILD_ROOT%{_winedir}/windows/Start Menu/Programs/Startup" \
	$RPM_BUILD_ROOT%{_winedir}/windows/{SendTo,ShellNew,system32,NetHood} \
	$RPM_BUILD_ROOT%{_winedir}/windows/{Profiles/Administrator,Recent} \
	$RPM_BUILD_ROOT%{_winedir}/{"Program Files/Common Files","My Documents"}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/wine
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT%{_winedir}/{autoexec.bat,config.sys,windows/win.ini}
touch $RPM_BUILD_ROOT%{_winedir}/windows/system/{shell.dll,shell32.dll}
touch $RPM_BUILD_ROOT%{_winedir}/windows/system/{winsock.dll,wsock32.dll}

cat >$RPM_BUILD_ROOT%{_winedir}/windows/system.ini <<EOF
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
	strip --strip-unneeded -R .note  -R .comment $elfsharedlist
fi
%endif

/sbin/chpax -p $RPM_BUILD_ROOT%{_bindir}/wine

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add wine
if [ ! -f /var/lock/subsys/wine ]; then
	echo "Run \"/etc/rc.d/init.d/wine start\" to start wine service." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/wine ]; then
		/etc/rc.d/init.d/wine stop >&2
	fi
	/sbin/chkconfig --del wine
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README DEVELOPERS-HINTS ChangeLog BUGS AUTHORS ANNOUNCE
%doc documentation/wine-user
%attr(755,root,root) %{_bindir}/widl
%attr(755,root,root) %{_bindir}/wine
%attr(755,root,root) %{_bindir}/winebuild
%attr(755,root,root) %{_bindir}/winemaker
%attr(755,root,root) %{_bindir}/wineserver
%attr(755,root,root) %{_bindir}/wineclipsrv
%attr(755,root,root) %{_bindir}/winelauncher
%attr(755,root,root) %{_bindir}/wineshelllink
%attr(755,root,root) %{_bindir}/winedump
%attr(755,root,root) %{_bindir}/wrc
%attr(755,root,root) %{_bindir}/wmc
%attr(755,root,root) %{_bindir}/fnt2bdf
%attr(755,root,root) %{_bindir}/function_grep.pl
%attr(755,root,root) %{_libdir}/*.so*
%{_libdir}/wine
%{_mandir}/man[15]/*
%config(noreplace) %{_sysconfdir}/wine.reg
%config(missingok) %{_sysconfdir}/wine.systemreg
%config(missingok) %{_sysconfdir}/wine.userreg
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/wine
%{_winedir}

%files programs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hlp2sgml
%attr(755,root,root) %{_bindir}/notepad
%attr(755,root,root) %{_bindir}/progman
%attr(755,root,root) %{_bindir}/regedit
%attr(755,root,root) %{_bindir}/regsvr32
%attr(755,root,root) %{_bindir}/uninstaller
%attr(755,root,root) %{_bindir}/wcmd
%attr(755,root,root) %{_bindir}/wineconsole
%attr(755,root,root) %{_bindir}/winedbg
%attr(755,root,root) %{_bindir}/winefile
%attr(755,root,root) %{_bindir}/winemine
%attr(755,root,root) %{_bindir}/winepath
%attr(755,root,root) %{_bindir}/winhelp

%files devel
%defattr(644,root,root,755)
%doc documentation/{wine-devel,winelib-user,HOWTO-winelib}
%{_aclocaldir}/wine.m4
%{_includedir}/wine
%{_libdir}/*.a
