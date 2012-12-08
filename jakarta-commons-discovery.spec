%define gcj_support 1
%define short_name commons-discovery

Summary:        Jakarta Commons Discovery
Name:           jakarta-commons-discovery
Version:        0.4
Release:        2.12
Epoch:          1
Group:          Development/Java
License:        Apache License
URL:            http://jakarta.apache.org/commons/discovery/
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Source0:        http://www.apache.org/dist/jakarta/commons/discovery/source/commons-discovery-0.4-src.tar.gz
Source1:        http://www.apache.org/dist/jakarta/commons/discovery/source/commons-discovery-0.4-src.tar.gz.asc
Source2:        http://www.apache.org/dist/jakarta/commons/discovery/source/commons-discovery-0.4-src.tar.gz.md5
#Vendor:        JPackage Project
#Distribution:  JPackage
BuildRequires:  ant
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  junit >= 0:3.7
BuildRequires:  jakarta-commons-logging >= 0:1.0.1
Requires:       jakarta-commons-logging >= 0:1.0.1

%description
The Discovery component is about discovering, or finding, implementations for
pluggable interfaces.  Pluggable interfaces are specified with the intent that
multiple implementations are, or will be, available to provide the service
described by the interface.  Discovery provides facilities for finding and
instantiating classes, and for lifecycle management of singleton (factory)
classes. 

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n commons-discovery-%{version}-src
%{__chmod} u+w .

# No NOTICE.txt file in the sources
/bin/touch NOTICE.txt
%{__perl} -pi -e 's/\r$//g' LICENSE.txt

%build
%{ant} \
  -Djunit.jar=$(find-jar junit) \
  -Dlogger.jar=$(find-jar jakarta-commons-logging) \
  test.discovery dist
if [ -z "`%{jar} tf dist/%{short_name}.jar | %{__grep} META-INF/INDEX.LIST`" ]; then
  %{jar} -i dist/%{short_name}.jar
fi

%install
%{__rm} -rf %{buildroot}

# jar
%{__install} -m 0644 dist/%{short_name}.jar -D %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-2.10mdv2011.0
+ Revision: 665801
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-2.9mdv2011.0
+ Revision: 606052
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-2.8mdv2010.1
+ Revision: 522970
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:0.4-2.7mdv2010.0
+ Revision: 425434
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1:0.4-2.6mdv2009.1
+ Revision: 351273
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 1:0.4-2.5mdv2009.0
+ Revision: 167940
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 1:0.4-2.5mdv2008.1
+ Revision: 120908
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 1:0.4-2.4mdv2008.0
+ Revision: 87406
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 1:0.4-2.3mdv2008.0
+ Revision: 82872
- rebuild


* Tue Mar 06 2007 David Walluck <walluck@mandriva.org> 0.4-2.2mdv2007.1
+ Revision: 133849
- rebuild
- rebuild

* Tue Feb 20 2007 David Walluck <walluck@mandriva.org> 1:0.4-1.1mdv2007.1
+ Revision: 123157
- fix rebuild-gcj-db call in %%post and %%postun
  fix gcj directory ownership
  0.4

* Mon Feb 19 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1:0.3-2.4mdv2007.1
+ Revision: 122855
- cleanups
- fix one-line-command-in-*
- index jar file

* Sat Nov 04 2006 David Walluck <walluck@mandriva.org> 1:0.3-2.3mdv2007.1
+ Revision: 76402
- fix macro
- rebuild
- Import jakarta-commons-discovery

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 1:0.3-2.1mdv2007.0
- bump release

* Sat Jun 03 2006 David Walluck <walluck@mandriva.org> 1:0.3-1.3mdv2007.0
- rebuild for libgcj.so.7

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 1:0.3-1.2mdk
- add post scripts

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 1:0.3-1.1mdk
- 0.3

* Sat May 21 2005 David Walluck <walluck@mandriva.org> 1:0.2-2.1mdk
- release

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 1:1:0.2-2jpp
- Rebuild with ant-1.6.2

