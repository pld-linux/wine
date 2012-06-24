Summary:	Program that lets you launch Win applications.
Summary(pl):	Program pozwalaj�cy uruchamia� aplikacje Windows.
Name:		wine
Version:	20000227
Release:	1
Copyright:	distributable
Group:		Applications/Emulators
Group(pl):	Applikacje/Emulatory
Source0:	ftp://metalab.unc.edu/pub/Linux/ALPHA/wine/development/Wine-%{version}.tar.gz
Url:		http://www.winehq.com
Exclusivearch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.  It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library that implements Windows API calls using
their Unix or X11 equivalents. The library may also be used for
porting Win32 code into native Unix executables.

%description -l pl
Wine iest programem dzi�ki kt�remu mo�na uruchamia� programy napisane
dla Microsoft Windows pod systemami unixowymi.

%package devel
Summary:        Wine - header files
Summary(pl):    Wine - pliki nag�owkowe
Group:          Development/Libraries
Group(pl):      Programowanie/Biblioteki
Requires:       %{name} = %{version}
 
%description devel
Wine - header files.

%description -l pl devel
Wine - pliki nag��wkowe.

%prep
%setup -q

%build

#automake
LDFLAGS="-s"; export LDFLAGS
%configure \
    --disable-debug \
    --disable-trace \
    --with-x

make depend
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

make install \
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
	
# there is something broken with make install 
# it expects root privileges, and if invoked by user, makes some stupid link
# instead of libs installation /by klakier

rm -f $RPM_BUILD_ROOT%{_libdir}/*.so
cp -dp libwine.so* $RPM_BUILD_ROOT%{_libdir}

cp wine.ini wine.conf.example
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/wine.conf
;
; You can find example wine.conf file in %{_docdir}/%{name}-%{version}/wine.conf.example
; More information: 'man wine.conf' or http://www.winehq.com
; 
; Przyk�adowy plik konfiguracyjny jest w %{_docdir}/%{name}-%{version}/wine.conf.example
; Wi�cej informacji: 'man wine.conf' lub na stronach WINE: http://www.winehq.com
;
EOF

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man5/*

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
%{_mandir}/man1/*
%{_mandir}/man5/*
%attr(755,root,root) %{_libdir}/*.so*
%{_libdir}/wine.sym
%config %{_sysconfdir}/wine.conf

%files devel
%defattr(644,root,root,755)
%{_includedir}/wine
