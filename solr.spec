#
# Conditional build:
%bcond_without	tests		# don't build and run tests
%bcond_without	source		# don't build source jar

# TODO
#get-colt:
#      [get] Getting: http://repo1.maven.org/maven2/colt/colt/1.2.0/colt-1.2.0.jar
#get-pcj:
#      [get] Getting: http://repo1.maven.org/maven2/pcj/pcj/1.2/pcj-1.2.jar
#get-nni:
#      [get] Getting: http://download.carrot2.org/maven2/org/carrot2/nni/1.0.0/nni-1.0.0.jar
#get-simple-xml:
#      [get] Getting: http://mirrors.ibiblio.org/pub/mirrors/maven2/org/simpleframework/simple-xml/1.7.3/simple-xml-1.7.3.jar
# - package .war
%include	/usr/lib/rpm/macros.java
Summary:	Solr - open source enterprise search server
Summary(pl.UTF-8):	Solr - profesjonalny serwer wyszukiwarki o otwartych źródłach
Name:		solr
Version:	1.4.1
Release:	0.2
License:	Apache
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/lucene/solr/%{version}/apache-%{name}-%{version}.tgz
# Source0-md5:	258a020ed8c3f44e13b09e8ae46a1c84
URL:		http://lucene.apache.org/solr/
BuildRequires:	java-junit
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
Obsoletes:	apache-solr
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
install -d $RPM_BUILD_ROOT%{_javadir}
for jar in dist/*.jar; do
	cp -a $jar $RPM_BUILD_ROOT%{_javadir}
	basejar=$(basename $jar -%{version}.jar).jar
	ln -s $(basename $jar) $RPM_BUILD_ROOT%{_javadir}/$basejar
done
# FIXME: where?
cp -a dist/solrj-lib $RPM_BUILD_ROOT%{_javadir}

# war? where
#cp -a dist/apache-solr-%{version}.war

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/apache-solr-*.jar
%{_javadir}/solrj-lib
