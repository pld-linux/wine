Summary:	Program that lets you launch Win applications
Summary(es):	Ejecuta programas Windows en Linux
Summary(pl):	Program pozwalaj±cy uruchamiaæ aplikacje Windows
Summary(pt_BR):	Executa programas Windows no Linux
Name:		wine
Version:	20011108
Release:	4
License:	distributable
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://metalab.unc.edu/pub/Linux/ALPHA/wine/development/Wine-%{version}.tar.gz
Source1:	wine.init
Source2:	wine.reg
Source3:	wine.systemreg
Source4:	wine.userreg
Patch0:		%{name}-fontcache.patch
URL:		http://www.winehq.com/
Exclusivearch:	%{ix86}
BuildRequires:	XFree86-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	ncurses-devel
BuildRequires:	OpenGL-devel
BuildRequires:  freetype-devel >= 2.0.5
BuildRequires:	chpax
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_winedir	%{_datadir}/%{name}

%define		no_install_post_strip	1

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
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name} = %{version}
 
%description devel
Wine - header files.

%description -l es devel
Biblioteca de desarrollo de wine.

%description -l pl devel
Wine - pliki nag³ówkowe.

%description -l pt_BR devel
Arquivos de inclusão e bibliotecas para desenvolver aplicações com o
WINE.

%prep
%setup -q
%patch -p1

%build
%configure2_13 \
	--disable-debug \
	--disable-trace \
	--enable-curses \
	--with-x

%{__make} depend
%{__make}

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
	infodir=$RPM_BUILD_ROOT%{_infodir} 
	
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


gzip -9nf README WARRANTY LICENSE DEVELOPERS-HINTS ChangeLog BUGS AUTHORS ANNOUNCE

filelist=`find $RPM_BUILD_ROOT -type f ! -regex ".*ld-[0-9.]*so.*"`
elfexelist=`echo $filelist | xargs -r file | awk '/ELF.*executable/ {print $1}' | cut -d: -f1`
elfsharedlist=`echo $filelist | xargs -r file | awk '/LF.*shared object/ {print $1}' | cut -d: -f1`
if [ -n "$elfexelist" ]; then 
	strip --remove-section=.note  --remove-section=.comment $elfexelist
fi
if [ -n "$elfsharedlist" ]; then 
	strip --strip-unneeded --remove-section=.note  --remove-section=.comment $elfsharedlist
fi

/sbin/chpax -p $RPM_BUILD_ROOT/%{_bindir}/wine

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,WARRANTY,LICENSE,DEVELOPERS-HINTS,ChangeLog,BUGS,AUTHORS,ANNOUNCE}.gz
%doc documentation
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so*
%{_mandir}/man[15]/*
%config(noreplace) %{_sysconfdir}/wine.reg
%config(missingok) %{_sysconfdir}/wine.systemreg
%config(missingok) %{_sysconfdir}/wine.userreg
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/wine
%{_winedir}

%files devel
%defattr(644,root,root,755)
%{_includedir}/wine
%{_libdir}/*.a
