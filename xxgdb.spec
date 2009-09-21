Name:		xxgdb
Summary:	An X Window System graphical interface for the GNU gdb debugger
Version:	1.12
Release:	%mkrel 27
License:	MIT
Group:		Development/Other
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxmu-devel
BuildRequires:	libxt-devel
BuildRequires:	imake
Source0:	ftp://sunsite.unc.edu/pub/Linux/devel/debuggers/%{name}-%{version}.tar.bz2
Source1:	xxgdb.wmconfig
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		xxgdb-1.08-glibc.patch
Patch1:		xxgdb-1.12-sysv.patch
Patch2:		xxgdb-1.12-compat21.patch
# From Debian (008-unix98-ptys.dpatch): Support Unix98 PTYs - AdamW
# 2008/09
Patch3:		xxgdb-1.12-debian-pty.patch
# From Debian: fix a build failure - AdamW 2008/09
Patch4:		xxgdb-1.12-debian-filemenu.patch
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
%patch3 -p1 -b .pty
%patch4 -p1 -b .build

%build
xmkmf
%make CDEBUGFLAGS="%{optflags}" CXXDEBUGFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
%{makeinstall_std} install.man

install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/X11/wmconfig/xxgdb

# icons
install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

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

rm -f %{buildroot}%{_prefix}/lib/X11/app-defaults

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/xxgdb.1*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XDbx
%config(noreplace) %{_sysconfdir}/X11/wmconfig/xxgdb
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
