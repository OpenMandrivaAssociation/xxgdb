%define	Summary	An X Window System graphical interface for the GNU gdb debugger

Name:		xxgdb
Summary:	%{Summary}
Version:	1.12
Release:	24mdk
License:	MIT
Icon:		%{name}.xpm
Group:		Development/Other
BuildRequires:	XFree86-devel X11

Source0:	ftp://sunsite.unc.edu/pub/Linux/devel/debuggers/%{name}-%{version}.tar.bz2
Source1:	xxgdb.wmconfig
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		xxgdb-1.08-glibc.patch.bz2
Patch1:		xxgdb-1.12-sysv.patch.bz2
Patch2:		xxgdb-1.12-compat21.patch.bz2
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
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

# (fg) Menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}):\
	command="%{name}"\
	needs="X11"\
	icon="%{name}.png"\
	section="Applications/Development/Tools"\
	title="%{name}"\
	longtitle="%{Summary}"
EOF

rm -f $RPM_BUILD_ROOT%{_prefix}/X11R6/lib/X11/app-defaults

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%{_prefix}/X11R6/bin/xxgdb
%{_prefix}/X11R6/man/man1/xxgdb.1x*
%{_prefix}/X11R6/lib/X11/doc/html/xxgdb.1.html
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XDbx
%config(noreplace) %{_sysconfdir}/X11/wmconfig/xxgdb
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
