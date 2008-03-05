%define name	xxgdb
%define version	1.12

Name:		%{name}
Summary:	An X Window System graphical interface for the GNU gdb debugger
Version:	%{version}
Release:	%mkrel 26
License:	MIT
Group:		Development/Other
BuildRequires:	libx11-devel libxext-devel libxaw-devel libxmu-devel libxt-devel imake

Source0:	ftp://sunsite.unc.edu/pub/Linux/devel/debuggers/%{name}-%{version}.tar.bz2
Source1:	xxgdb.wmconfig
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		xxgdb-1.08-glibc.patch
Patch1:		xxgdb-1.12-sysv.patch
Patch2:		xxgdb-1.12-compat21.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	gdb

%description
Xxgdb is an X Window System graphical interface to the GNU gdb debugger.
Xxgdb provides visual feedback and supports a mouse interface for the
user who wants to perform debugging tasks like the following:  controlling
program execution through breakpoints, examining and traversing the
function call stack, displaying values of variables and data structures,
and browsing source files and functions.

Install the xxgdb package if you'd like to use a graphical interface with
the GNU gdb debugger.  You'll also need to have the gdb package installed.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .compat21

%build
xmkmf
%make CDEBUGFLAGS="$RPM_OPT_FLAGS" CXXDEBUGFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} install.man

install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmconfig/xxgdb

# icons
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Xxgdb
Comment=Graphical interface to gdb debugger
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Development;Debugger;
EOF

rm -f $RPM_BUILD_ROOT%{_prefix}/lib/X11/app-defaults

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/xxgdb.1*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XDbx
%config(noreplace) %{_sysconfdir}/X11/wmconfig/xxgdb
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
