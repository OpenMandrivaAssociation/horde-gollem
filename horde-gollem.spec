%define	module	gollem
%define	name	horde-%{module}
%define version 1.0.4
%define release %mkrel 4

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde file manager
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Gollem is the Horde web-based File Manager, providing the ability to fully
manage a hierarchical file system stored in a variety of backends such as a SQL
database, as part of a real filesystem, or on an FTP server. It uses the
Horde's MIME_Viewer framework to identify file types, associate icons, etc.

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
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
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(-,root,root)
%config(noreplace) %{_webappconfdir}/%{name}.conf
%doc README COPYING docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
