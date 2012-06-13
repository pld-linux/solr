# TODO
# - build from source, external deps
# - split libs in java-solr package to subpackages depending on their usage
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
Release:	2
License:	Apache v2.0
Group:		Development/Languages/Java
#Source0:	http://www.apache.org/dist/lucene/solr/%{version}/apache-%{name}-%{version}-src.tgz
Source0:	http://www.apache.org/dist/lucene/solr/%{version}/apache-%{name}-%{version}.tgz
# Source0-md5:	ac11ef4408bb015aa3a5eefcb1047aec
Source1:	%{name}-context.xml
Source2:	%{name}.xml
URL:		https://lucene.apache.org/solr/
#BuildRequires:	java-ivy >= 2.2.0
#BuildRequires:	java-junit
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-%{name} = %{version}-%{release}
Requires:	jpackage-utils
Requires:	tomcat
Obsoletes:	apache-solr < 3.6.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		webappdir %{_datadir}/%{name}

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

%package -n java-%{name}
Summary:	Solr libraries
Group:		Libraries/Java
Requires:	jpackage-utils

%description -n java-%{name}
Solr libraries:
- analysis-extras
- cell
- clustering
- core
- dataimporthandler
- dataimporthandler-extras
- langid
- solrj
- test-framework
- uima
- velocity

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

# install .jars
install -d $RPM_BUILD_ROOT%{_javadir}
for a in dist/apache-solr-*.jar; do
	jar=${a##*/}
	cp -p dist/$jar $RPM_BUILD_ROOT%{_javadir}
	ln -s $jar $RPM_BUILD_ROOT%{_javadir}/${jar%%-%{version}.jar}.jar
done

# install webapp
install -d $RPM_BUILD_ROOT%{webappdir}
cp -p dist/apache-solr-%{version}.war $RPM_BUILD_ROOT%{webappdir}/%{name}.war

# install tomcat context descriptor
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_tomcatconfdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml

# setup cores configuration
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/solr.xml
ln -s %{_sysconfdir}/%{name}/solr.xml $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}

# setup sample instance
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/example/data
cp -a example/solr/conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/example
ln -s %{_sysconfdir}/%{name}/example $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/example/conf

%clean
rm -rf $RPM_BUILD_ROOT

%postun
%tomcat_clear_cache %{name}

%files
%defattr(644,root,root,755)
%doc CHANGES.txt NOTICE.txt README.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/tomcat-context.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/solr.xml
%{_tomcatconfdir}/%{name}.xml
%dir %{webappdir}
%{webappdir}/solr.war
%dir %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/solr.xml

# sample instance configuration
%attr(750,root,servlet) %dir %{_sharedstatedir}/%{name}/example
%attr(2775,root,servlet) %dir %{_sharedstatedir}/%{name}/example/data
%{_sharedstatedir}/%{name}/example/conf
%dir %{_sysconfdir}/%{name}/example
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/example/*.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/example/*.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/example/*.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/example/*.conf
%dir %{_sysconfdir}/%{name}/example/lang
%{_sysconfdir}/%{name}/example/lang/*.txt
%dir %{_sysconfdir}/%{name}/example/velocity
%{_sysconfdir}/%{name}/example/velocity/*.css
%{_sysconfdir}/%{name}/example/velocity/*.js
%{_sysconfdir}/%{name}/example/velocity/*.vm
%dir %{_sysconfdir}/%{name}/example/xslt
%{_sysconfdir}/%{name}/example/xslt/*.xsl

%files -n java-%{name}
%defattr(644,root,root,755)
%{_javadir}/apache-solr-*.jar
#%{_javadir}/solrj-lib
