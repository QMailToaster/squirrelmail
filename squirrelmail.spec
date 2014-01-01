Name:      squirrelmail
Summary:   SquirrelMail webmail client
Version:   1.4.22
Release:   0%{?dist}
License:   GPL
Group:     Applications/Internet
Vendor:    QmailToaster
Packager:  Eric Shubert <qmt-build@datamatters.us>
URL:       http://www.squirrelmail.org/
Source0:   http://downloads.sourceforge.net/project/squirrelmail/stable/1.4.22/%{name}-webmail-%{version}.tar.gz
Source1:   http://www.squirrelmail.org/plugins/quota_usage-1.3.1-1.2.7.tar.gz
Source2:   http://www.squirrelmail.org/plugins/unsafe_image_rules.0.8-1.4.tar.gz
Source3:   http://www.squirrelmail.org/plugins/notes.1.2-1.4.0.tar.gz
Source4:   http://www.squirrelmail.org/plugins/qmailadmin_login-1.1-1.4.3.tar.gz
Source5:   config_local.php
Source6:   squirrelmail.conf
Patch0:	   squirrelmail-toaster-02052009.patch
Requires:  httpd
Requires:  php
Requires:  perl
Requires:  aspell
Obsoletes: squirrelmail-toaster
BuildRoot: %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define debug_package %{nil}
%define apachedir     /etc/httpd/conf/
%define apacheuser    apache
%define apachegroup   apache
%define httpdconf     httpd.conf
%define sdir          %{_datadir}/squirrelmail
%define pdir          %{sdir}/plugins
%define lcdir         %{_sysconfdir}/squirrelmail/
%define hcpath        %{apachedir}%{httpdconf}

#------------------------------------------------------------------------------
%description
#------------------------------------------------------------------------------
SquirrelMail is a standards-based webmail package written in PHP4. It
includes built-in pure PHP support for the IMAP and SMTP protocols, and
all pages render in pure HTML 4.0 (with no Javascript) for maximum
compatibility across browsers.  It has very few requirements and is very
easy to configure and install. SquirrelMail has all the functionality
you would want from an email client, including strong MIME support,
address books, and folder manipulation.

#------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------

%setup -q -n %{name}-webmail-%{version}

%patch0 -p0

# install plugins
tar -C plugins -xvzf %{SOURCE1}
tar -C plugins -xvzf %{SOURCE2}
tar -C plugins -xvzf %{SOURCE3}
tar -C plugins -xvzf %{SOURCE4}

%{__rm} -f plugins/make_archive.pl

%{__mv} themes/README.themes doc/

for f in `find plugins -name "README*" -or -name INSTALL \
    -or -name CHANGES -or -name HISTORY`; do
  %{__mkdir_p} doc/`dirname $f`
  %{__mv} $f $_
done

%{__mv} doc/plugins/squirrelspell/doc/README doc/plugins/squirrelspell
%{__rm} -rf doc/plugins/squirrelspell/doc
%{__mv} plugins/squirrelspell/doc/* doc/plugins/squirrelspell
%{__rm} -f doc/plugins/squirrelspell/index.php
%{__rm} -rf plugins/squirrelspell/doc

# Fixup various files
echo "left_refresh=300" >> data/default_pref
for f in contrib/RPM/squirrelmail.cron contrib/RPM/config.php.redhat; do
    %{__perl} -pi \
        -e "s|__ATTDIR__|%{_localstatedir}/spool/squirrelmail/attach/|g;" \
        -e "s|__PREFSDIR__|%{_localstatedir}/lib/squirrelmail/prefs/|g;" $f
done

# Fix the version
%{__perl} -pi -e "s|^(\s*\\\$version\s*=\s*).*|\1'%{version}-%{release}';|g"\
    functions/strings.php

#------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------
rm -rf %{buildroot}
[ -n %{buildroot} ] && rm -rf %{buildroot}

%{__mkdir_p} -m 755 %{buildroot}%{_sysconfdir}/squirrelmail
%{__mkdir_p} -m 755 %{buildroot}%{_localstatedir}/lib/squirrelmail/prefs
%{__mkdir_p} -m 755 %{buildroot}%{_localstatedir}/spool/squirrelmail/attach
%{__mkdir_p} -m 755 %{buildroot}%{sdir}

# install default_pref
%{__install} -m 644 data/default_pref \
    %{buildroot}%{_localstatedir}/lib/squirrelmail/prefs/

# install the config files
%{__mkdir_p} -m 755 %{buildroot}%{sdir}/config
%{__install} -m 644 contrib/RPM/config.php.redhat \
    %{buildroot}%{_sysconfdir}/squirrelmail/config.php
%{__ln_s} %{_sysconfdir}/squirrelmail/config.php \
    %{buildroot}%{sdir}/config/config.php
%{__install} -m 644 config/config_local.php \
    %{buildroot}%{_sysconfdir}/squirrelmail/config_local.php
%{__ln_s} %{_sysconfdir}/squirrelmail/config_local.php \
    %{buildroot}%{sdir}/config/config_local.php
%{__rm} -f config/config_local.php config/config.php
%{__install} -m 644 config/*.php %{buildroot}%{sdir}/config/
%{__install} -m 755 config/*.pl  %{buildroot}%{sdir}/config/

# install index.php
%{__install} -m 644 index.php %{buildroot}%{sdir}

# Copy over the rest
for DIR in class functions help images include locale plugins src themes; do
    %{__cp} -rp $DIR %{buildroot}%{sdir}/
done

%{__mv} -f %{buildroot}%{lcdir}/config_local.php \
                         %{buildroot}%{lcdir}/config_local.php.dist
%{__install} %{SOURCE5}  %{buildroot}%{lcdir}/.

# install the cron script
%{__install} -Dp contrib/RPM/squirrelmail.cron \
      %{buildroot}/%{_sysconfdir}/cron.daily/squirrelmail.cron

%{__install} -Dp %{SOURCE6} %{buildroot}%{apachedir}squirrelmail.conf

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
rm -rf %{_builddir}/%{name}-%{version}
rm -rf %{buildroot}

#------------------------------------------------------------------------------
%files
#------------------------------------------------------------------------------
%defattr(-,root,root)
%config %dir %{_sysconfdir}/squirrelmail
%config(noreplace) %{_sysconfdir}/squirrelmail/*
%config(noreplace) %{apachedir}*.conf
%doc doc/*

%dir %{sdir}
%{sdir}/index.php
%{sdir}/class
%{sdir}/functions
%{sdir}/help
%{sdir}/images
%{sdir}/include
%{sdir}/locale
%{sdir}/src
%{sdir}/themes
%{sdir}/config

%dir %{sdir}/plugins
%{sdir}/plugins/*

%dir %{_localstatedir}/lib/squirrelmail
%dir %{_localstatedir}/spool/squirrelmail
%attr(0770, root, %{apachegroup}) %dir %{_localstatedir}/lib/squirrelmail/prefs
%attr(0730, root, %{apachegroup}) %dir %{_localstatedir}/spool/squirrelmail/attach
%{_localstatedir}/lib/squirrelmail/prefs/default_pref
%{_sysconfdir}/cron.daily/squirrelmail.cron

#-------------------------------------------------------------------------------
%preun
#-------------------------------------------------------------------------------
if [ "$1" = 0 ]; then
  # Remove squirrelmail.conf
  grep -v 'Include %{apachedir}squirrelmail.conf' %{hcpath} > %{hcpath}.new
  mv -f %{hcpath}.new %{hcpath}
fi

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------
if [ $1 = "1" ]; then

grep -i 'Include.*squirrelmail.conf$' %{hcpath} >/dev/null 2>&1

if [ $? -eq 0 ]; then
  perl -pi -e 's/^#+// if (/Include.*squirrelmail.conf$/i);' %{hcpath}
else
  echo "Include %{apachedir}squirrelmail.conf" >>%{hcpath}
fi

echo ""
echo " A new include directive was added:"
echo ""
echo "    %{apachedir}squirrelmail.conf"
echo ""
echo " Configuration:"
echo "    If you plan to use it in a VirtualDomain please delete"
echo "    the include directive from %{httpdconf} and  add it  in"
echo "    your VirtualDomain"
echo ""

fi

#------------------------------------------------------------------------------
%changelog
#------------------------------------------------------------------------------
* Wed Nov 13 2013 Eric Shubert <eric@datamatters.us> 1.4.22-1.5.0
- Migrated to repoforge
- Added CentOS 6 support
- Removed unsupported cruft
* Fri Sep 28 2012 Eric Shubert <eric@datamatters.us> 1.4.22-1.4.0
- Updated Squirrelmail source to 1.4.22
* Tue Apr 06 2010 Jake Vickers <jake@qmailtoaster.com> 1.4.20-1.3.17
- Updated Squirrelmail source to 1.4.20
* Sat Dec 05 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.19-1.3.16
- Added Fedora 12 and Fedora 12 x86_64 support
* Mon Nov 30 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.19-1.3.16
- Added Mandriva 2010 and Mandriva 2010 x86_64 support
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.19-1.3.15
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.19-1.3.15
- Updated Squirrelmail to 1.4.19
- Added Mandriva 2009 support
* Wed May 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.18-1.3.14
- Updated Squirrelmail to version 1.4.18
- No longer move some files (README, AUTHORS, etc.) to the doc/ dir
- since they are already there as of this new release
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.17-1.3.13
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Mon Feb 16 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.17-1.3.12
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.17-1.3.12
- Added support for Fedora Core 6 and Fedora 9
* Thu Feb 05 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.17-1.3.12
- Added support for Fedora 10
* Fri Jul 11 2008 Erik A. Espinoza <espinoza@kabewm.com> 1.4.15-1.3.10
- Upgraded to SquirrelMail 1.4.15
* Thu Dec 20 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.4.13-1.3.9
- Upgraded to SquirrelMail 1.4.13
* Mon Oct 01 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.4.11-1.3.8
- Upgraded to SquirrelMail 1.4.11
* Mon May 21 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.4.10a-1.3.7
- Upgraded to SquirrelMail 1.4.10a
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.4.9a-1.3.6
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Sun Jan 07 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.4.9a-1.3.5
- Upgraded to SquirrelMail 1.4.9a
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.8-1.3.4
- Added Fedora Core 6 support
* Tue Aug 22 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.8-1.3.3
- Upgraded to SquirrelMail 1.4.8
* Wed Jul 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.7-1.3.2
- Upgraded SquirrelMail to 1.4.7
- Upgraded qmailadmin_plugin to 1.1-1.4.3
- Upgraded quota_usage to 1.3.1-1.2.7
- Upgraded unsafe_image_rules to 0.8-1.4
- Upgraded notes to 1.2-1.4.0
- Defaulted SquirrelMail config to hide version attributes
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.15
- Add Fedora Core 5 support
* Fri Mar 03 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.6-1.2.14
- Upgraded to Squirrelmail 1.4.6
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.13
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.12
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.11
- Add CentOS 4 x86_64 support
* Thu Jul 14 2005 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.5-1.2.10
- Update to squirrelmail 1.4.5
* Thu Jul 14 2005 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.4-1.2.9
- Added QmailAdmin_Login plugin
* Mon Jul 04 2005 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.4-1.2.8
- Added XSS Patch for CVE CAN-2005-1769
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.7
- Add Fedora Core 4 support
* Wed Jun 08 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.4-1.2.6
- Update to squirrelmail-1.4.4
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.4.2-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
- Move install dir for mdk
- Fix some problems wiith access rights and such
* Tue May 31 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.4
- Update quota-usage and add unsafe_image_rules
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.3
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.2
- Add Fedora Core 2 support
- Add notes plugin
* Fri May 14 2004 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.2.1
- Add sasql and quota_usage plugins
- Add squirrelmail.conf to httpd.conf
* Sun Oct 12 2003 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.0.2
- Removed symlink for apache-1.3.x users
* Tue Oct 7 2003 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-1.0.1
- Hack to squirrelmail-toaster-1.4.2-1.0.1
* Mon Oct 6 2003 Nick Hemmesch <nick@ndhsoft.com> 1.4.2-2
- This version is configured to only work with Qmail Toaster from
  http://www.qmailtoaster.com using SpamAssassin user based prefs

* Wed Oct 01 2003 Konstantin Riabitsev <icon@duke.edu> 1.4.2-1
- The release was uncoordinated with the admin team, so this revision is
  not in the CVS, and the RPM cannot be built from the distribution
  tarball. Parties responsible will be chastised.
- Version 1.4.2.

* Thu Jul 03 2003 Konstantin Riabitsev <icon@duke.edu> 1.4.1-1
- Build for 1.4.1
- Prefixing the release with "0" so the RPM upgrades cleanly when going to
  rht > 7.x.

* Tue Mar 26 2003 Konstantin Riabitsev <icon@duke.edu> 1.4.0-1
- Build for 1.4.0

* Thu Feb 13 2003 Konstantin Riabitsev <icon@duke.edu> 1.4.0-0.2pre
- Initial release for 1.4.0 prerelease

* Tue Feb 04 2003 Konstantin Riabitsev <icon@duke.edu> 1.2.11-1
- Upping version number.

* Tue Oct 29 2002 Konstantin Riabitsev <icon@duke.edu> 1.2.9-1
- Upping version number.

* Sat Sep 14 2002 Konstantin Riabitsev <icon@duke.edu> 1.2.8-1
- adopted RH's spec file so we don't duplicate effort. 
- Removed rh'ized splash screen.
- Adding fallbacks for building rhl7 version as well with the same 
  specfile. Makes the spec file not as clean, but hey.
- remove workarounds for #68669 (rh bugzilla), since 1.2.8 works with
  register_globals = Off.
- Hardwiring localhost into the default config file. Makes sense.
- No more such file MIRRORS.
- Adding aspell as one of the req's, since squirrelspell is enabled by
  default
- Added Vendor: line to distinguish ourselves from RH.
- Doing the uglies with the release numbers.

* Tue Aug  6 2002 Preston Brown <pbrown@redhat.com> 1.2.7-4
- replacement splash screen.

* Mon Jul 22 2002 Gary Benson <gbenson@redhat.com> 1.2.7-3
- get rid of long lines in the specfile.
- remove symlink in docroot and use an alias in conf.d instead.
- work with register_globals off (#68669)

* Tue Jul 09 2002 Gary Benson <gbenson@redhat.com> 1.2.7-2
- hardwire the hostname (well, localhost) into the config file (#67635)

* Mon Jun 24 2002 Gary Benson <gbenson@redhat.com> 1.2.7-1
- hardwire the locations into the config file and cron file.
- install squirrelmail-cleanup.cron as squirrelmail.cron.
- make symlinks relative.
- upgrade to 1.2.7.
- more dependency fixes.

* Fri Jun 21 2002 Gary Benson <gbenson@redhat.com>
- summarize the summary, fix deps, and remove some redundant stuff.
- tidy up the prep section.
- replace directory definitions with standard RHL ones.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.2.6-3
- automated rebuild

* Wed Jun 19 2002 Preston Brown <pbrown@redhat.com> 1.2.6-2
- adopted Konstantin Riabitsev <icon@duke.edu>'s package for Red Hat
  Linux.  Nice job Konstantin!
