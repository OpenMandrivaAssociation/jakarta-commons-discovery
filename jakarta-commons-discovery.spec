%define gcj_support 1
%define short_name commons-discovery

Summary:        Jakarta Commons Discovery
Name:           jakarta-commons-discovery
Version:        0.4
Release:        %mkrel 2.5
Epoch:          1
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
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
%{__cp} -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
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

%clean
%{__rm} -rf %{buildroot}

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


