%define gcj_support 1
%define short_name commons-discovery

Summary:	Jakarta Commons Discovery
Name:		jakarta-commons-discovery
Epoch:		1
Version:	0.4
Release:	3
Group:		Development/Java
License:	Apache License
Url:		https://jakarta.apache.org/commons/discovery/
Source0:	http://www.apache.org/dist/jakarta/commons/discovery/source/commons-discovery-0.4-src.tar.gz
Source1:	http://www.apache.org/dist/jakarta/commons/discovery/source/commons-discovery-0.4-src.tar.gz.asc
Source2:	http://www.apache.org/dist/jakarta/commons/discovery/source/commons-discovery-0.4-src.tar.gz.md5
%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	junit >= 0:3.7
BuildRequires:	jakarta-commons-logging >= 0:1.0.1
Requires:	jakarta-commons-logging >= 0:1.0.1

%description
The Discovery component is about discovering, or finding, implementations for
pluggable interfaces.  Pluggable interfaces are specified with the intent that
multiple implementations are, or will be, available to provide the service
described by the interface.  Discovery provides facilities for finding and
instantiating classes, and for lifecycle management of singleton (factory)
classes. 

%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -qn commons-discovery-%{version}-src
chmod u+w .

# No NOTICE.txt file in the sources
/bin/touch NOTICE.txt
sed -i -e 's/\r$//g' LICENSE.txt

%build
%ant \
	-Djunit.jar=$(find-jar junit) \
	-Dlogger.jar=$(find-jar jakarta-commons-logging) \
	test.discovery dist
if [ -z "`%{jar} tf dist/%{short_name}.jar | %{__grep} META-INF/INDEX.LIST`" ]; then
	%{jar} -i dist/%{short_name}.jar
fi

%install
# jar
install -m 0644 dist/%{short_name}.jar -D %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

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
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

