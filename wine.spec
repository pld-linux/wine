Summary:	Program that lets you launch Win applications
Summary(es):	Ejecuta programas Windows en Linux
Summary(pl):	Program pozwalaj±cy uruchamiaÊ aplikacje Windows
Summary(pt_BR):	Executa programas Windows no Linux
Name:		wine
Version:	20011108
Release:	1
License:	distributable
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://metalab.unc.edu/pub/Linux/ALPHA/wine/development/Wine-%{version}.tar.gz
Patch0:		%{name}-fontcache.patch
URL:		http://www.winehq.com/
Exclusivearch:	%{ix86}
BuildRequires:	XFree86-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	ncurses-devel
BuildRequires:	OpenGL-devel
BuildRequires:  freetype-devel >= 2.0.5
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

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
Wine jest programem dziÍki ktÛremu moøna uruchamiaÊ programy napisane
dla Microsoft Windows pod systemami unixowymi. Sk≥ada siÍ on z
loadera, ktÛry pozwala wczytywaÊ i uruchamiaÊ programy w formacie
Microsoft Windows oraz z biblioteki, ktÛra implementuje API Windows
przy uøyciu odpowiednikÛw Unixowych oraz z X11. Biblioteka moøe byÊ
takøe wykorzystana do przenoszenia aplikacji Win32 do Unixa.

%description -l pt_BR
O Wine È um programa que permite rodar programas MS-Windows no X11.
Ele consiste de um carregador de programa, que carrega e executa um
bin·rio MS-Windows, e de uma biblioteca de emulaÁ„o que traduz as
chamadas da API para as equivalentes Unix/X11.

%package devel
Summary:	Wine - header files
Summary(es):	Biblioteca de desarrollo de wine
Summary(pl):	Wine - pliki nag≥owkowe
Summary(pt_BR):	Biblioteca de desenvolvimento do wine
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}
 
%description devel
Wine - header files.

%description -l es devel
Biblioteca de desarrollo de wine.

%description -l pl devel
Wine - pliki nag≥Ûwkowe.

%description -l pt_BR devel
Arquivos de inclus„o e bibliotecas para desenvolver aplicaÁıes com o
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
	
cp -f documentation/samples/config wine.conf.example
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/wine.conf
;
; You can find example wine.conf file in %{_docdir}/%{name}-%{version}/wine.conf.example
; More information: 'man wine.conf' or http://www.winehq.com
; 
; Przyk≥adowy plik konfiguracyjny jest w %{_docdir}/%{name}-%{version}/wine.conf.example
; WiÍcej informacji: 'man wine.conf' lub na stronach WINE: http://www.winehq.com
;
EOF

gzip -9nf README WARRANTY LICENSE DEVELOPERS-HINTS ChangeLog BUGS AUTHORS ANNOUNCE

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,WARRANTY,LICENSE,DEVELOPERS-HINTS,ChangeLog,BUGS,AUTHORS,ANNOUNCE}.gz
%doc documentation wine.conf.example
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so*
%{_mandir}/man[15]/*
%config(noreplace) %{_sysconfdir}/wine.conf

%files devel
%defattr(644,root,root,755)
%{_includedir}/wine
%{_libdir}/*.a
