#
# Build mock and local RPM versions of python modules
#

# Assure that sorting is case sensitive
LANG=C

# Ignore ownership and group,
RSYNCOPTS=-a --no-owner --no-group
# Skip existing files to avoid binary churn in yum repos
#RSYNCSAFEOPTS=$(RSYNCOPTS) --ignore-existing 

# "mock" configurations to build with, activate only as needed
# Some RHEL dependencies are supplied locally in awsclirepo
MOCKS+=epel-7-x86_64

# Local yum compatible RPM repository
REPOBASEDIR="`/bin/pwd | xargs dirname`/awsclirepo"

# Deduce local package names and .spec files, for universe Makefile use
SPEC := `ls *.spec | head -1`
PKGNAME := "`ls *.spec | head -1 | sed 's/.spec$$//g'`"

# Needed for yum repo updates
all:: /usr/bin/createrepo
all:: $(MOCKS)

# Get any tarballes as describe by .spec
getsrc:
	spectool -g $(SPEC)

srpm:: FORCE
	@echo "Building $(SPEC) SRPM"
	rm -rf rpmbuild
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		--define '_sourcedir $(PWD)' \
		-bs $(SPEC) --nodeps

# Needed for python27 compatible compilation
build:: srpm FORCE
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		--rebuild rpmbuild/SRPMS/*.src.rpm

$(MOCKS):: srpm FORCE
	@if [ -n "`find $@ -name \*.rpm ! -name \*.src.rpm 2>/dev/null`" ]; then \
		echo "	Skipping $(SPEC) in $@ with RPMS"; \
	else \
		echo "Storing " rpmbuild/SRPMS/*.src.rpm "as $@.src.rpm"; \
		install rpmbuild/SRPMS/*.src.rpm $@.src.rpm; \
		echo "Building $@.src.rpm in $@"; \
		rm -rf $@; \
		mock -q -r $(PWD)/../$@.cfg \
		    --resultdir=$(PWD)/$@ \
		    $@.src.rpm; \
	fi

mock:: $(MOCKS)

clean::
	rm -rf $(MOCKS)
	rm -rf rpmbuild
	rm -rf */
	rm -f *.rpm
	rm -f *~
	rm -f *.out

realclean distclean:: clean

FORCE:
