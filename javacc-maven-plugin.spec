Name:           javacc-maven-plugin
Version:        2.6
Release:        7
Summary:        JavaCC Maven Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://mojo.codehaus.org/javacc-maven-plugin/ 
#svn export http://svn.codehaus.org/mojo/tags/javacc-maven-plugin-2.6
#tar cjf javacc-maven-plugin-2.6.tar.bz2 javacc-maven-plugin-2.6
Source0:        javacc-maven-plugin-2.6.tar.bz2
Patch0:         javacc-maven-plugin-pom.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: maven2
BuildRequires: javacc >= 5.0
BuildRequires: plexus-utils
BuildRequires: maven-doxia
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-compiler-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: mojo-parent
BuildRequires: plexus-containers-component-javadoc
BuildRequires: junit
Requires: javacc >= 5.0
Requires: plexus-utils
Requires: jpackage-utils
Requires: mojo-parent
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
Maven 2 Plugin for processing JavaCC grammar files.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q 
%patch0 -b .sav

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        package javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.codehaus.mojo javacc-maven-plugin %{version} JPP javacc-maven-plugin

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%doc src/main/resources/NOTICE

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

