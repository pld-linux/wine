#
# Conditional build:
%bcond_without arts     # without arts support
%bcond_without cups     # without CUPS printing support
%bcond_without sane     # without TWAIN scanning support (through SANE)
%bcond_with    pdf_docs # build pdf docs (missing BR)
%bcond_with    html_docs # build html docs (jade fault ?)
#
# maybe TODO: alsa,jack,nas BRs/checks (see dlls/winmm/wine*)
Summary:	Program that lets you launch Win applications
Summary(es):	Ejecuta programas Windows en Linux
Summary(pl):	Program pozwalaj±cy uruchamiaæ aplikacje Windows
Summary(pt_BR):	Executa programas Windows no Linux
Name:		wine
Version:	20030911
Release:	0.2
License:	GPL
Group:		Applications/Emulators
Source0:	http://dl.sf.net/wine/Wine-%{version}.tar.gz
# Source0-md5:	81521fe47d540427183e88d02d5c5f88
Source1:	%{name}.init
Source2:	%{name}.reg
Source3:	%{name}.systemreg
Source4:	%{name}.userreg
Patch0:		%{name}-fontcache.patch
Patch1:		%{name}-destdir.patch
Patch2:		%{name}-ncurses.patch
Patch3:		%{name}-ac-ksh.patch
Patch4:		%{name}-binutils.patch
Patch5:		%{name}-makedep.patch
Patch6:		%{name}-dga.patch
Patch7:		%{name}-winebuild.patch
Patch8:		%{name}-cdrom-segv.patch
URL:		http://www.winehq.com/
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
%{?with_arts:BuildRequires:	arts-devel}
BuildRequires:	bison
BuildRequires:	chpax >= 0.20020901-2
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.5
BuildRequires:	libjpeg-devel
BuildRequires:	ncurses-devel
%if %{with html_docs} || %{with pdf_docs}
BuildRequires:	openjade
%endif
%if %{with pdf_docs}
BuildRequires:	tetex-metafont
BuildRequires:	tetex-fonts-pazo
BuildRequires:	tetex-fonts-stmaryrd
BuildRequires:	tetex-fonts-type1-urw
%endif
%{?with_sane:BuildRequires:	sane-backends-devel}
Requires:	OpenGL
Requires(post):	/sbin/ldconfig
Requires(post,preun):/sbin/chkconfig
# link to wine/ntdll.dll.so, without any SONAME
Provides:	libntdll.dll.so
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep		libGL.so.1 libGLU.so.1
%define		no_install_post_strip	1

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
Wine - programs.

%description programs -l pl
Wine - programy.

%package doc-pdf
Summary:	Wine documentation in PDF
Summary(pl):	Dokumentacja Wine w formacie PDF
Group:		Documentation

%description doc-pdf
Wine documentation in PDF format.

%description doc-pdf -l pl
Dokumentacja Wine w formacie PDF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# turn off compilation of some tools
#sed -e "s|winetest \\\|\\\|;s|avitools||" programs/Makefile.in > .tmp
sed -e "s|avitools||" programs/Makefile.in > .tmp
mv -f .tmp programs/Makefile.in

%build
%{__aclocal}
%{__autoconf}
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS
CFLAGS="%{rpmcflags} $CPPFLAGS"
%configure \
	%{!?debug:--disable-debug} \
	%{!?debug:--disable-trace} \
	--enable-curses \
	--enable-opengl \
	--with-x
%{__make} depend
%{__make}
%{__make} -C programs
%{__make} -C programs/regapi

cd documentation
%if %{with html_docs}
db2html wine-user.sgml
db2html wine-devel.sgml
db2html wine-faq.sgml
db2html winelib-user.sgml
%endif

%if %{with pdf_docs}
db2pdf 	wine-user.sgml
db2pdf  wine-devel.sgml
db2pdf  wine-faq.sgml
db2pdf  winelib-user.sgml
%endif
cd -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_aclocaldir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__make} -C programs install DESTDIR=$RPM_BUILD_ROOT

install programs/winhelp/hlp2sgml	$RPM_BUILD_ROOT%{_bindir}
install tools/fnt2bdf			$RPM_BUILD_ROOT%{_bindir}

install aclocal.m4 $RPM_BUILD_ROOT%{_aclocaldir}/wine.m4
#mv -f $RPM_BUILD_ROOT{/usr/X11R6/share/aclocal,%{_aclocaldir}}/wine.m4

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d \
        $RPM_BUILD_ROOT%{_winedir}/windows/{system,Desktop,Favorites,Fonts} \
        "$RPM_BUILD_ROOT%{_winedir}/windows/Start Menu/Programs/Startup" \
	$RPM_BUILD_ROOT%{_winedir}/windows/{SendTo,ShellNew,system32,NetHood} \
	$RPM_BUILD_ROOT%{_winedir}/windows/{Profiles/Administrator,Recent} \
	$RPM_BUILD_ROOT%{_winedir}/{"Program Files/Common Files","My Documents"}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/wine
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

/sbin/chstk -e $RPM_BUILD_ROOT%{_bindir}/wine

programs="notepad progman regedit regsvr32 uninstaller wineconsole winefile winemine winepath winhelp wcmd"

BZZZ=`pwd`
rm -f files.so;		touch files.so
rm -f files.programs;	touch files.programs
cd $RPM_BUILD_ROOT%{_libdir}/wine
for f in *.so; do
	echo "%attr(755,root,root) %{_libdir}/wine/$f" >>$BZZZ/files.so
done
cd -
for p in $programs; do
	echo "%attr(755,root,root) %{_bindir}/$p" >> files.programs
	echo "%attr(755,root,root) %{_libdir}/wine/$p.exe.so" >> files.programs
	grep -v "$p\.exe\.so$" files.so > files.so.
	mv -f files.so. files.so
done

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

%files -f files.so
%defattr(644,root,root,755)
%doc README DEVELOPERS-HINTS ChangeLog BUGS AUTHORS ANNOUNCE
%doc documentation/{samples,status}
%if %{with html_docs}
%doc documentation/wine-{faq,user}
%endif
%attr(755,root,root) %{_bindir}/wine
%attr(755,root,root) %{_bindir}/wineboot
%attr(755,root,root) %{_bindir}/winecfg
%attr(755,root,root) %{_bindir}/wineclipsrv
%attr(755,root,root) %{_bindir}/winedbg
%attr(755,root,root) %{_bindir}/winelauncher
%attr(755,root,root) %{_bindir}/wineserver
%attr(755,root,root) %{_bindir}/wineshelllink
%attr(755,root,root) %{_libdir}/*.so*
%dir %{_libdir}/wine
%{_mandir}/man1/wine.*
%{_mandir}/man5/wine.conf.*
%config(noreplace) %{_sysconfdir}/wine.reg
%config(missingok) %{_sysconfdir}/wine.systemreg
%config(missingok) %{_sysconfdir}/wine.userreg
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/wine
%{_winedir}

%files programs -f files.programs
%defattr(644,root,root,755)

%files devel
%defattr(644,root,root,755)
%if %{with html_docs}
%doc documentation/{wine-devel,winelib-user,HOWTO-winelib}
%endif
%attr(755,root,root) %{_bindir}/fnt2bdf
%attr(755,root,root) %{_bindir}/function_grep.pl
%attr(755,root,root) %{_bindir}/hlp2sgml
%attr(755,root,root) %{_bindir}/widl
%attr(755,root,root) %{_bindir}/winebuild
%attr(755,root,root) %{_bindir}/winedump
%attr(755,root,root) %{_bindir}/wineg++
%attr(755,root,root) %{_bindir}/winegcc
%attr(755,root,root) %{_bindir}/winemaker
%attr(755,root,root) %{_bindir}/winewrap
%attr(755,root,root) %{_bindir}/wmc
%attr(755,root,root) %{_bindir}/wrc
%{_includedir}/wine
%{_libdir}/*.a
%{_mandir}/man1/winemaker.*
%{_mandir}/man1/winebuild.*
%{_mandir}/man1/wmc.*
%{_mandir}/man1/wrc.*
%{_aclocaldir}/*.m4

%if %{with pdf_docs}
%files doc-pdf
%defattr(644,root,root,755)
%doc documentation/*.pdf
%endif
