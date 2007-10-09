# TODO
# - package .war
%include	/usr/lib/rpm/macros.java
Summary:	solr
Name:		apache-solr
Version:	1.2.0
Release:	0.1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://apache.zone-h.org/lucene/solr/1.2/%{name}-%{version}.tgz
# Source0-md5:	37725998228d525096ae5a887d046a9d
URL:		http://lucene.apache.org/solr/
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
ExclusiveArch:	i586 i686 pentium3 pentium4 athlon %{x8664} noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Solr is an open source enterprise search server based on the Lucene
Java search library, with XML/HTTP and JSON APIs, hit highlighting,
faceted search, caching, replication, and a web administration
interface. It runs in a Java servlet container such as Tomcat.

%prep
%setup -q

%build
required_jars="junit"
export CLASSPATH=$(build-classpath $required_jars)
%ant dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
# install jar
cp -a dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar
