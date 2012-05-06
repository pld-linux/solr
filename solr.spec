# TODO
# - build from source, external deps
# NOTES:
# - http://wiki.apache.org/solr/SolrTomcat
#
# Conditional build:
%bcond_without	tests		# don't build and run tests
%bcond_with		source		# don't build source jar

%include	/usr/lib/rpm/macros.java
Summary:	Solr - open source enterprise search server
Summary(pl.UTF-8):	Solr - profesjonalny serwer wyszukiwarki o otwartych źródłach
Name:		solr
Version:	3.6.0
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/lucene/solr/%{version}/apache-%{name}-%{version}.tgz
# Source0-md5:	ac11ef4408bb015aa3a5eefcb1047aec
Source1:	%{name}-context.xml
URL:		https://lucene.apache.org/solr/
#BuildRequires:	java-junit
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Requires:	tomcat
Obsoletes:	apache-solr < 3.6.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		webappdir %{_datadir}/%{name}
%define		libdir    %{webappdir}/WEB-INF/lib
%define		logdir    %{_var}/log/%{name}

%description
Solr is an open source enterprise search server based on the Lucene
Java search library, with XML/HTTP and JSON APIs, hit highlighting,
faceted search, caching, replication, and a web administration
interface. It runs in a Java servlet container such as Tomcat.

%description -l pl.UTF-8
Solr to profesjonalny serwer wyszukiwarki o otwartych źródłach oparty
na bibliotece wyszukiwarki Lucene w Javie z API XML/HTTP i JSON,
podświetlaniem dopasowań, pamięcią podręczną, replikacją i interfejsem
administracyjnym WWW. Działa w kontenerze serwletowym Javy, takim jak
Tomcat.

%prep
%setup -q -n apache-%{name}-%{version}

%if %{with source}
# remove bindist
rm -rf dist/*
%endif

%build
required_jars="junit"
export CLASSPATH=$(build-classpath $required_jars)
%if %{with source}
%ant dist \
	-Dversion=%{version}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if 0
# TODO: java-solr package
install -d $RPM_BUILD_ROOT%{_javadir}
for jar in dist/*.jar; do
	cp -a $jar $RPM_BUILD_ROOT%{_javadir}
	basejar=$(basename $jar -%{version}.jar).jar
	ln -s $(basename $jar) $RPM_BUILD_ROOT%{_javadir}/$basejar
done
# FIXME: where?
cp -a dist/solrj-lib $RPM_BUILD_ROOT%{_javadir}
%endif

install -d $RPM_BUILD_ROOT%{webappdir}
cp -p dist/apache-solr-%{version}.war $RPM_BUILD_ROOT%{webappdir}/%{name}.war

# Install tomcat context descriptor
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_sharedstatedir}/%{name}/data,%{_tomcatconfdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml

cp -a example/solr/conf/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s %{_sysconfdir}/%{name} $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/conf

%clean
rm -rf $RPM_BUILD_ROOT

%postun
%tomcat_clear_cache %{name}

%files
%defattr(644,root,root,755)
%doc CHANGES.txt NOTICE.txt README.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%dir %{_sysconfdir}/%{name}/lang
%{_sysconfdir}/%{name}/lang/*.txt
%dir %{_sysconfdir}/%{name}/velocity
%{_sysconfdir}/%{name}/velocity/*.css
%{_sysconfdir}/%{name}/velocity/*.js
%{_sysconfdir}/%{name}/velocity/*.vm
%dir %{_sysconfdir}/%{name}/xslt
%{_sysconfdir}/%{name}/xslt/*.xsl

%{_tomcatconfdir}/%{name}.xml
%dir %{webappdir}
%{webappdir}/*.war
%dir %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/conf
%attr(2775,root,servlet) %dir %{_sharedstatedir}/%{name}/data

# -n java-solr
#%{_javadir}/apache-solr-*.jar
#%{_javadir}/solrj-lib
