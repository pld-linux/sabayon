# TODO
# - useradd/groupadd broken (no uid/gid)
# - xorg-x11-devel doesn't exist
Summary:	Tool to maintain user profiles in a GNOME desktop
Summary(pl.UTF-8):	Narzędzie do zarządzania profilami użytkowników w środowisku GNOME
Name:		sabayon
Version:	2.20.1
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sabayon/2.20/%{name}-%{version}.tar.bz2
# Source0-md5:	1d3217ddffa413651d918844e5f5a7d9
URL:		http://www.gnome.org/projects/sabayon
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gtk+2-devel >= 2:2.8.17
BuildRequires:	python-devel
BuildRequires:	python-pygtk-devel >= 2.8.6
BuildRequires:	usermode
BuildRequires:	xorg-x11-devel
Requires(post,preun):	shadow-utils
Requires(post,postun):	gtk+2 >= 2.8.17
%pyrequires_eq  python-modules
Requires:	gamin-python
Requires:	libxml2-python
Requires:	python-gnome-gconf >= 2.12.4
Requires:	python-ldap
Requires:	python-pygtk >= 2.8.6
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
Requires:	%{name} = %{version}-%{release}
Requires:	shadow
Requires:	xorg-xserver-Xnest

%description admin
The sabayon-admin package contains the graphical tools which a
sysadmin should use to manage Sabayon profiles.

%description admin -l pl.UTF-8
Ten pakiet zawiera graficzne narzędzia dla administratora do
zarządzania profilami Sabayon.

%prep
%setup -q

%build
%configure \
	--enable-consolehelper=yes \
	--with-prototype-user=%{name}-admin

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PAM_PREFIX=$RPM_BUILD_ROOT%{_sysconfdir}

echo 'include "$(HOME)/.gconf.path.defaults"'  > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-defaults.path
echo 'include "$(HOME)/.gconf.path.mandatory"' > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-mandatory.path

desktop-file-install --vendor gnome --delete-original \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	--add-category X-Fedora-Extra \
	$RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# We don't want these
rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{name}/xlib.la
rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{name}/xlib.a

%find_lang sabayon

%clean
rm -rf $RPM_BUILD_ROOT

%pre admin
%groupadd -r %{name}-admin
%useradd -r -s /sbin/nologin -c "Sabayon user" -g %{name}-admin %{name}-admin
/usr/sbin/usermod -d "" %{name}-admin >/dev/null 2>&1 || :

%post admin
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun admin
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

if [ $1 -eq 0 ]; then
	%userremove %{name}-admin
	%groupremove %{name}-admin
fi

%files -f sabayon.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO ISSUES sabayon.schema
%config(noreplace) %{_sysconfdir}/gconf/2/local-defaults.path
%config(noreplace) %{_sysconfdir}/gconf/2/local-mandatory.path
%config(noreplace) %{_sysconfdir}/X11/xinit/xinitrc.d/%{name}*
%{_sysconfdir}/desktop-profiles
%attr(755,root,root) %{_sbindir}/%{name}-apply
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/__init__.py*
%{py_sitedir}/%{name}/config.py*
%{py_sitedir}/%{name}/cache.py*
%{py_sitedir}/%{name}/dirmonitor.py*
%{py_sitedir}/%{name}/mozilla_bookmarks.py*
%{py_sitedir}/%{name}/storage.py*
%{py_sitedir}/%{name}/userdb.py*
%{py_sitedir}/%{name}/userprofile.py*
%{py_sitedir}/%{name}/util.py*

%files admin
%defattr(644,root,root,755)
%doc doc/index.html doc/testing.html doc/helping.html doc/developing.html
%doc doc/sabayon.css doc/*.jpg doc/*.gif
%config(noreplace) /etc/pam.d/%{name}
%config(noreplace) /etc/security/console.apps/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{_libexecdir}/%{name}*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/glade
%{_datadir}/%{name}/glade/*.glade
%{_desktopdir}/gnome-%{name}.desktop
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%attr(755,root,root) %{py_sitedir}/%{name}/xlib.so
%{py_sitedir}/%{name}/aboutdialog.py*
%{py_sitedir}/%{name}/changeswindow.py*
%{py_sitedir}/%{name}/editorwindow.py*
%{py_sitedir}/%{name}/fileviewer.py*
%{py_sitedir}/%{name}/gconfviewer.py*
%{py_sitedir}/%{name}/profilesdialog.py*
%{py_sitedir}/%{name}/protosession.py*
%{py_sitedir}/%{name}/saveconfirm.py*
%{py_sitedir}/%{name}/sessionwidget.py*
%{py_sitedir}/%{name}/sessionwindow.py*
%{py_sitedir}/%{name}/usermod.py*
%{py_sitedir}/%{name}/usersdialog.py*
%{py_sitedir}/%{name}/lockdownappliersabayon.py*
%{py_sitedir}/%{name}/lockdown
