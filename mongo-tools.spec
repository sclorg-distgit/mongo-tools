%{?scl:%scl_package mongo-tools}

%global with_devel 1
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         mongodb
%global repo            mongo-tools
# https://github.com/mongodb/mongo-tools
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          4d4d96583c40a25a4ee7e2d038d75181a300ec3c
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

# Git hash in https://github.com/mongodb/mongo which corresponds to Version
%global mongohash a14d55980c2cdc565d4704a7e3ad37e4e535c1b2

%global gopath %{_datadir}/gocode

%global golangscl go-toolset-7
%global golangprefix %{golangscl}-
%global buildscls %{golangscl} %{?scl}

Name:           %{?scl_prefix}%{repo}
Version:        3.4.5
Release:        0.3.git%{shortcommit}%{?dist}
Summary:        MongoDB Tools
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
# Mongo-tools does not contain man files yet
# - see https://groups.google.com/forum/#!topic/mongodb-dev/t6Sd2Bki12I
Source1:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/bsondump.1
Source2:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongodump.1
Source3:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongoexport.1
Source4:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongofiles.1
Source5:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongoimport.1
Source6:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongooplog.1
Source7:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongorestore.1
Source8:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongostat.1
Source9:        https://github.com/mongodb/mongo/raw/%{mongohash}/debian/mongotop.1
Source10:       https://github.com/mongodb/mongo/raw/%{mongohash}/APACHE-2.0.txt

Patch0:         change-import-path.patch
Patch1:         use-dup3-on-linux.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 ppc64le s390x
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?golangprefix}golang

BuildRequires:  openssl-devel
BuildRequires:  libpcap-devel

%if ! 0%{?with_bundled}
BuildRequires:  %{?scl_prefix}golang(github.com/howeyc/gopass)
BuildRequires:  %{?scl_prefix}golang(github.com/jessevdk/go-flags)
BuildRequires:  %{?scl_prefix}golang(github.com/smartystreets/goconvey/convey)
BuildRequires:  %{?scl_prefix}golang(github.com/10gen/openssl)
BuildRequires:  %{?scl_prefix}golang(golang.org/x/crypto/ssh/terminal)
BuildRequires:  %{?scl_prefix}golang(gopkg.in/mgo.v2)
BuildRequires:  %{?scl_prefix}golang(gopkg.in/mgo.v2/bson)
BuildRequires:  %{?scl_prefix}golang(gopkg.in/tomb.v2)
%endif

%{?scl:Requires:%scl_runtime}

#Conflicts:      mongodb < 3.0.0

%description
The MongoDB tools provides import, export, and diagnostic capabilities.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if ! 0%{?with_bundled}
%if 0%{?with_check}
BuildRequires: %{?scl_prefix}golang(github.com/howeyc/gopass)
BuildRequires: %{?scl_prefix}golang(github.com/jessevdk/go-flags)
BuildRequires: %{?scl_prefix}golang(github.com/smartystreets/goconvey/convey)
BuildRequires: %{?scl_prefix}golang(github.com/10gen/openssl)
BuildRequires: %{?scl_prefix}golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: %{?scl_prefix}golang(gopkg.in/mgo.v2)
BuildRequires: %{?scl_prefix}golang(gopkg.in/mgo.v2/bson)
BuildRequires: %{?scl_prefix}golang(gopkg.in/tomb.v2)
%endif

Requires:      %{?scl_prefix}golang(github.com/howeyc/gopass)
Requires:      %{?scl_prefix}golang(github.com/jessevdk/go-flags)
Requires:      %{?scl_prefix}golang(github.com/smartystreets/goconvey/convey)
Requires:      %{?scl_prefix}golang(github.com/10gen/openssl)
Requires:      %{?scl_prefix}golang(golang.org/x/crypto/ssh/terminal)
Requires:      %{?scl_prefix}golang(gopkg.in/mgo.v2)
Requires:      %{?scl_prefix}golang(gopkg.in/mgo.v2/bson)
Requires:      %{?scl_prefix}golang(gopkg.in/tomb.v2)
%endif

Provides:      %{?scl_prefix}golang(%{import_path}/bsondump) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/archive) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/auth) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/bsonutil) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/db) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/db/kerberos) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/db/openssl) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/intents) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/json) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/log) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/options) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/password) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/progress) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/signals) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/testutil) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/text) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/common/util) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongodump) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongoexport) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongofiles) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongoimport) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongoimport/csv) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongooplog) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongorestore) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongostat) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongotop) = %{version}-%{release}
Provides:      %{?scl_prefix}golang(%{import_path}/mongoreplay) = %{version}-%{release}

%{?scl:Requires:%scl_runtime}

%description devel
This package contains library source intended for
building other packages which use %{project}/%{repo}.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test
Summary:         Unit tests for %{name} package
BuildRequires:  %{?golangprefix}golang

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

# syspath subpackages
%if 0%{?scl:1}
%scl_syspaths_package -d
%endif

%prep
%setup -q -n %{repo}-%{commit}
%if ! 0%{?with_bundled}
%patch0 -p1
%endif
pushd vendor/src/github.com/spacemonkeygo/spacelog/
%patch1 -p1
popd

%build
%{?scl:scl enable %{buildscls} - << "SCLEOF"}
set -ex
# Make link for etcd itself
mkdir -p src/github.com/mongodb
ln -s ../../../  src/github.com/mongodb/mongo-tools

%if 0%{?with_bundled}
export GOPATH=$(pwd):$(pwd)/vendor:%{gopath}
%else
export GOPATH=$(pwd):%{gopath}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
%endif

mkdir bin
binaries=(bsondump mongostat mongofiles mongoexport mongoimport mongorestore mongodump mongotop mongooplog mongoreplay)
for bin in "${binaries[@]}"; do
  %gobuild -o bin/${bin} \-tags ssl ${bin}/main/${bin}.go
done

# Copy Apache license
cp %{SOURCE10} $(basename %{SOURCE10})

%{?scl:SCLEOF}
%install
%{?scl:scl enable %{buildscls} - << "SCLEOF"}
set -ex
# main package binary
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/* %{buildroot}%{_bindir}

install -d -m 755            %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE5} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE6} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE7} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE8} %{buildroot}%{_mandir}/man1/
install -p -m 644 %{SOURCE9} %{buildroot}%{_mandir}/man1/

%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
cp -r mongorestore/testdata %{buildroot}/%{gopath}/src/%{import_path}/mongorestore/testdata
echo "%%{gopath}/src/%%{import_path}/mongorestore/testdata" >> unit-test.file-list
cp -r mongostat/test_data %{buildroot}/%{gopath}/src/%{import_path}/mongostat/test_data
echo "%%{gopath}/src/%%{import_path}/mongostat/test_data" >> unit-test.file-list
%endif

%if 0%{?with_devel}
olddir=$(pwd)
pushd %{buildroot}/%{gopath}/src/%{import_path}
for file in $(find . -type d) ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$file" >> ${olddir}/devel.file-list
done
popd
echo "%%dir %%{gopath}/src/%{provider}.%{provider_tld}/%{project}" >> devel.file-list
echo "%%dir %%{gopath}/src/%{provider}.%{provider_tld}" >> devel.file-list

sort -u -o devel.file-list devel.file-list
%endif

# syspath subpackages
%if 0%{?scl:1}
binaries='bsondump mongostat mongofiles mongoexport mongoimport mongorestore mongodump mongotop mongooplog'
binaries_no_man='mongoreplay'
mans= ; for bin in $binaries; do mans+="${sep}man1/$bin.1.gz" ; sep=' '; done
%scl_syspaths_install_wrappers -n %{pkg_name} -m script -p bin $binaries
%scl_syspaths_install_wrappers -n %{pkg_name} -m link -p man $mans
%scl_syspaths_install_wrappers -n %{pkg_name} -m script -p bin $binaries_no_man
%endif
%{?scl:SCLEOF}

%check
%{?scl:scl enable %{buildscls} - << "SCLEOF"}
set -ex
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/common/bsonutil
%gotest %{import_path}/common/db
# upstream bug, removed field from Intents struct
#%%gotest %{import_path}/common/intents
# redeclaration of C
#gotest {import_path}/common/json
# import cycle not allowed in test
#gotest {import_path}/common/log
%gotest %{import_path}/common/progress
%gotest %{import_path}/common/text
%gotest %{import_path}/common/util
%gotest %{import_path}/mongodump
%gotest %{import_path}/mongoexport
%gotest %{import_path}/mongofiles
#gotest {import_path}/mongoimport
%gotest %{import_path}/mongooplog
%gotest %{import_path}/mongorestore
%gotest %{import_path}/mongostat
#%gotest %{import_path}/mongoreplay
%endif
%{?scl:SCLEOF}

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE.md APACHE-2.0.txt
%doc Godeps README.md CONTRIBUTING.md THIRD-PARTY-NOTICES
%{_bindir}/*
%{_mandir}/man1/*

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE.md
%doc Godeps README.md CONTRIBUTING.md THIRD-PARTY-NOTICES
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test -f unit-test.file-list
%license LICENSE.md
%doc Godeps README.md CONTRIBUTING.md THIRD-PARTY-NOTICES
%endif

# syspath subpackages
%if 0%{?scl:1}
%scl_syspaths_files
%endif

%changelog
* Fri Jun 23 2017 Marek Skalický <mskalick@redhat.com> - 3.4.5-0.3.git4d4d965
- Add -syspath subpackage

* Thu Jun 22 2017 Marek Skalický <mskalick@redhat.com> - 3.4.5-0.2.git4d4d965
- Build also mongoreplay
- patch vendored dependency github.com/spacemonkeygo/spacelog to use syscall.Dup3

* Thu Jun 22 2017 Marek Skalický <mskalick@redhat.com> - 3.4.5-0.1.git4d4d965
- Update to 3.4.5

* Wed Jun 21 2017 Marek Skalický <mskalick@redhat.com> - 3.2.1-0.7.git17a5573
- Use bundled dependencies
- Use go-toolset-7 for building

* Fri Feb 12 2016 Marek Skalicky <mskalick@redhat.com> - 3.1.1-0.3.git17a5573
- Removed conflict with old versions of mongodb

* Wed Feb 3 2016 Marek Skalicky <mskalick@redhat.com> - 3.1.1-0.2.git17a5573
- Fixed directory ownership

* Wed Jan 27 2016 jchaloup <jchaloup@redhat.com> - 3.1.1-0.1.git17a5573
- Update to 3.2.1
  resolves: #1282650

* Mon Nov 09 2015 jchaloup <jchaloup@redhat.com> - 3.0.4-0.2.gitefe71bf
- Update to spec-2.1
  resolves: #1279140

* Mon Jun 22 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.4-1
- Repacked by using gofed tool (thanks to jchaloup@redhat.com)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.3-1
- Upgrade to version 3.0.3
- Add Apache license

* Mon May 4 2015 Marek Skalicky <mskalick@redhat.com> - 3.0.2-1
- Initial packaging
