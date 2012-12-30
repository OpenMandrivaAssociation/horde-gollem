%define	module	gollem
%define	name	horde-%{module}

%if %{_use_internal_dependency_generator}
%define __noautoreq 'pear\\(Horde.*\\)'
%else
%define _requires_exceptions pear(Horde.*)
%endif

Name:		%{name}
Version:	1.1.2
Release:	1
Summary:	The Horde file manager
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org:21/pub/gollem/gollem-h3-%{version}.tar.gz
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
BuildArch:	noarch

%description
Gollem is the Horde web-based File Manager, providing the ability to fully
manage a hierarchical file system stored in a variety of backends such as a SQL
database, as part of a real filesystem, or on an FTP server. It uses the
Horde's MIME_Viewer framework to identify file types, associate icons, etc.

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Gollem Horde configuration file
//
 
$this->applications['gollem'] = array(
    'fileroot' => $this->applications['horde']['fileroot'] . '/gollem',
    'webroot'  => $this->applications['horde']['webroot'] . '/gollem',
    'name'     => _("File Manager"),
    'status'   => 'active',
    'menu_parent' => 'myaccount',
    'provides' => 'files',
);

$this->applications['gollem-menu'] = array(
    'status' => 'block',
    'app' => 'gollem',
    'blockname' => 'tree_menu',
    'menu_parent' => 'gollem',
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

%clean

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_webappconfdir}/%{name}.conf
%doc README COPYING docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.0.4-7mdv2011.0
+ Revision: 565211
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.4-6mdv2010.1
+ Revision: 493344
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.4-4mdv2010.0
+ Revision: 446017
- new setup (simpler is better)

* Wed Aug 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.4-3mdv2010.0
+ Revision: 418311
- fix registry file (fix #52696)

* Wed Nov 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.4-2mdv2009.1
+ Revision: 304681
- fix automatic dependencies

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.4-1mdv2009.1
+ Revision: 295309
- import horde-gollem


* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.4-1mdv2009.1
- first mdv release

