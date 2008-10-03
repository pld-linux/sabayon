# TODO
# - nonstandard in (in pld means) %config in files
Summary:	Tool to maintain user profiles in a GNOME desktop
Summary(pl.UTF-8):	Narzędzie do zarządzania profilami użytkowników w środowisku GNOME
Name:		sabayon
Version:	2.22.0
Release:	6
License:	GPL
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sabayon/2.22/%{name}-%{version}.tar.bz2
# Source0-md5:	39159282db60bfdfcd8569ecb5a992f5
Patch0:		%{name}-pld.patch
Patch1:		%{name}-pythonpath.patch
URL:		http://www.gnome.org/projects/sabayon
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk+2-devel >= 2:2.8.17
BuildRequires:	intltool >= 0.36.2
BuildRequires:	python-devel
BuildRequires:	python-pygtk-devel >= 2:2.8.6
Requires(post,postun):	gtk+2 >= 2.8.17
%pyrequires_eq  python-modules
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires:	python-gamin
Requires:	python-gnome-gconf >= 2.12.4
Requires:	python-ldap
Requires:	python-libxml2
Requires:	python-pygtk-gtk >= 2:2.8.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sabayon is a tool to help sysadmins and user change and maintain the
default behaviour of the GNOME desktop.

%description -l pl.UTF-8
Sabayon to narzędzie pomagające administratorom i użytkownikom
zmieniać i utrzymywać domyślne zachowanie środowiska GNOME.

%package admin
Summary:	Graphical tools for Sabayon profile management
Summary(pl.UTF-8):	Graficzne narzędzia do zarządzania profilami Sabayon
Group:		Applications/System
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires:	%{name} = %{version}-%{release}
Requires:	pwdutils
Requires:	xorg-xserver-Xnest

%description admin
The sabayon-admin package contains the graphical tools which a
sysadmin should use to manage Sabayon profiles.

%description admin -l pl.UTF-8
Ten pakiet zawiera graficzne narzędzia dla administratora do
zarządzania profilami Sabayon.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__intltoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-prototype-user=sabayon \
	--with-distro=pld

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

echo 'include "$(HOME)/.gconf.path.defaults"'  > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-defaults.path
echo 'include "$(HOME)/.gconf.path.mandatory"' > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-mandatory.path

desktop-file-install --vendor gnome --delete-original \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{name}/xlib.la
rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{name}/xlib.a

%py_postclean
%find_lang sabayon

%clean
rm -rf $RPM_BUILD_ROOT

%pre admin
%groupadd -g 225 sabayon
%useradd -u 225 -d %{_datadir}/empty -c "Sabayon user" -g sabayon sabayon

%post admin
%update_desktop_database_post
%update_icon_cache hicolor

%postun admin
%update_desktop_database_postun
%update_icon_cache hicolor

if [ "$1" -eq 0 ]; then
	%userremove sabayon
	%groupremove sabayon
fi

%files -f sabayon.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO ISSUES sabayon.schema
%config(noreplace) %{_sysconfdir}/gconf/2/local-defaults.path
%config(noreplace) %{_sysconfdir}/gconf/2/local-mandatory.path
%config(noreplace) %{_sysconfdir}/X11/xinit/xinitrc.d/%{name}*
%{_sysconfdir}/desktop-profiles
%attr(755,root,root) %{_sbindir}/sabayon-apply
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.py[co]
%dir %{py_sitedir}/%{name}/sources
%{py_sitedir}/%{name}/sources/*.py[co]
%dir %{py_sitedir}/%{name}/lockdown
%{py_sitedir}/%{name}/lockdown/*.py[co]

%files admin
%defattr(644,root,root,755)
%doc doc/index.html doc/testing.html doc/helping.html doc/developing.html
%doc doc/sabayon.css doc/*.jpg doc/*.gif
%attr(755,root,root) %{_bindir}/sabayon
%attr(755,root,root) %{_libexecdir}/sabayon-session
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/glade
%{_datadir}/%{name}/glade/*.glade
%{_desktopdir}/gnome-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%attr(755,root,root) %{py_sitedir}/%{name}/xlib.so
