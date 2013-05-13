Name:		xxgdb
Summary:	An X Window System graphical interface for the GNU gdb debugger
Version:	1.12
Release:	32
License:	MIT
Group:		Development/Other
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	imake
Source0:	ftp://sunsite.unc.edu/pub/Linux/devel/debuggers/%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		xxgdb-1.08-glibc.patch
Patch1:		xxgdb-1.12-sysv.patch
# From Debian (008-unix98-ptys.dpatch): Support Unix98 PTYs - AdamW
# 2008/09
Patch3:		xxgdb-1.12-debian-pty.patch
# From Debian: fix a build failure - AdamW 2008/09
Patch4:		xxgdb-1.12-debian-filemenu.patch
Patch5:		xxgdb-1.12-mandriva.patch
Requires:	gdb
Requires:	xedit

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
%patch3 -p1 -b .pty
%patch4 -p1 -b .build
%patch5 -p1

%build
xmkmf
%make CDEBUGFLAGS="%{optflags} -DUNIX98=1" CXXDEBUGFLAGS="%{optflags} -DUNIX98=1"

%install
rm -rf %{buildroot}
%{makeinstall_std} install.man

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
mkdir -p %{buildroot}%{_datadir}/X11/app-defaults
mv -f %{buildroot}%{_sysconfdir}/X11/app-defaults/XDbx %{buildroot}%{_datadir}/X11/app-defaults

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
%{_datadir}/X11/app-defaults/XDbx
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.12-31mdv2011.0
+ Revision: 615754
- the mass rebuild of 2010.1 packages

* Fri May 07 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.12-30mdv2010.1
+ Revision: 543087
+ rebuild (emptylog)

* Wed May 05 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.12-29mdv2010.1
+ Revision: 542612
- Make package functional again

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Mar 29 2009 Funda Wang <fwang@mandriva.org> 1.12-26mdv2009.1
+ Revision: 362092
- rediff filemenu patch

* Wed Sep 10 2008 Adam Williamson <awilliamson@mandriva.org> 1.12-26mdv2009.0
+ Revision: 283425
- drop legacy icons
- s,$RPM_OPT_FLAGS,%%{optflags} and s,$RPM_BUILD_ROOT,%%{buildroot}
- add debian-filemenu.patch from Debian (fixes a build issue)
- add debian-pty.patch from Debian (adds support for Unix98 PTYs, #21825)
- one buildrequires per line
- drop unnecessary defines

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'
    - fix man pages extension

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Jun 18 2007 Adam Williamson <awilliamson@mandriva.org> 1.12-25mdv2008.0
+ Revision: 40758
- new X layout; XDG menu; fd.o icons; trim buildrequires; rebuild for new era
- Import xxgdb



* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.12-24mdk
- Rebuild

* Sat Dec 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.12-23mdk
- fix buildrequires

* Mon Aug 16 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.12-22mdk
- Rebuild with new menu

* Tue Jun 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.12-21mdk
- fix unpackaged files
- cleanups

* Sat Jul 12 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.12-20mdk
- macroize
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install
- rebuild
- fix unpackaged files

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 1.12-19mdk
- Use %%_tmppath for BuildRoot
- Use %%update_menus and %%clean_menus macros
- Let spec_helper do its job (bzip2 man pages and strip binaries)

* Thu Sep 14 2000 Florin Grad <florin@mandrakesoft.com> 1.12-18mdk
- eliminating some more warnings from rpmlint
- adding large icon and made all icons transparent

* Wed Aug 30 2000 Florin Grad <florin@mandrakesoft.com> 1.12-17mdk
- adding some macros

* Tue Aug 08 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.12-16mdk
- automatically added BuildRequires

* Wed Apr  5 2000 Denis Havlik <denis@mandrakesoft.com> 1.12-15mdk
- group: Development/Other
- menu + icons ( need beter ones!) 
- spechelper

* Wed Dec 1 1999 Florent Villard <warly@mandrakesoft.com>
- built in new environment

* Tue Oct 19 1999 - David BAUDENS <baudens@mandrakesoft.com>
- Fix incorrect paths in patch #1 (xxgdb-1.12-sysv.patch.bz2)

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Wed Mar 23 1999 Michael Maher <mike@redhat.com>
- added requires for gdb

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- patch around i386 wchar_t glibc-2.1 typedef.

* Wed Jul 29 1998 Jeff Johnson <jbj@redhat.com>
- change wmconfig group to utilities
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Feb  9 1998 Otto Hammersmith <otto@redhat.com>
- fixed wmconfig entry

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- fixed src url
- added wmconfig entries
- removed prefix line ... can't have it with wmconfig file :(

* Fri Aug 22 1997 Erik Troan <ewt@redhat.com>
- built against glibc
