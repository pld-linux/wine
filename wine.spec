Summary:	Program that lets you launch Win applications
Summary(pl):	Program pozwalaj±cy uruchamiaæ aplikacje Windows
Name:		wine
Version:	20001202
Release:	2
License:	Distributable
Group:		Applications/Emulators
Group(de):	Applikationen/Emulators
Group(pl):	Aplikacje/Emulatory
Source0:	ftp://metalab.unc.edu/pub/Linux/ALPHA/wine/development/Wine-%{version}.tar.gz
URL:		http://www.winehq.com/
Exclusivearch:	%{ix86}
BuildRequires:	XFree86-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library that implements Windows API calls using
their Unix or X11 equivalents. The library may also be used for
porting Win32 code into native Unix executables.

%description -l pl
Wine jest programem dziêki któremu mo¿na uruchamiaæ programy napisane
dla Microsoft Windows pod systemami unixowymi. Sk³ada siê on z
loadera, który pozwala wczytywaæ i uruchamiaæ programy w formacie
Microsoft Windows oraz z biblioteki, która implementuje API Windows
przy u¿yciu odpowiedników Unixowych oraz z X11. Biblioteka mo¿e byæ
tak¿e wykorzystana do przenoszenia aplikacji Win32 do Unixa.

%package devel
Summary:	Wine - header files
Summary(pl):	Wine - pliki nag³owkowe
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
 
%description devel
Wine - header files.

%description -l pl devel
Wine - pliki nag³ówkowe.

%prep
%setup -q

%build
%configure \
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
	
cp wine.ini wine.conf.example
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/wine.conf
;
; You can find example wine.conf file in %{_docdir}/%{name}-%{version}/wine.conf.example
; More information: 'man wine.conf' or http://www.winehq.com
; 
; Przyk³adowy plik konfiguracyjny jest w %{_docdir}/%{name}-%{version}/wine.conf.example
; Wiêcej informacji: 'man wine.conf' lub na stronach WINE: http://www.winehq.com
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
%{_mandir}/man[15]/*
%attr(755,root,root) %{_libdir}/*.so*
#%{_libdir}/wine.sym
%config(noreplace) %{_sysconfdir}/wine.conf

%files devel
%defattr(644,root,root,755)
%{_includedir}/wine
#%attr(755,root,root) %{_libdir}/lib*.so
