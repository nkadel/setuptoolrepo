#
# Makefile - build wrapper for setuptool on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	SETUPTOOLPKGS below
#
#	Set up local 

# Rely on local nginx service poingint to file://$(PWD)/setuptoolrepo
REPOBASE = file://$(PWD)
#EPOBASE = http://localhost

# Placeholder RPMs for python2-foo packages to include python-foo
EPELPKGS+=python-certifi-srpm/

SETUPPKGS+=python-setuptool-srpm/

REPOS+=setuptoolrepo/el/6
REPOS+=setuptoolrepo/el/7

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=setuptoolrepo-6-x86_64.cfg
CFGS+=setuptoolrepo-7-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-6-x86_64.cfg
MOCKCFGS+=epel-7-x86_64.cfg

all:: $(CFGS) $(MOCKCFGS)
all:: $(REPODIRS)
all:: $(EPELPKGS)
all:: $(SETUPTOOLPKGS)

all install clean:: FORCE
	@for name in $(EPELPKGS) $(SETUPTOOLPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

epel:: $(EPELPKGS)

# Build for locacl OS
build:: FORCE
	@for name in $(SETUPTOOLPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done

# Dependencies
python-setuptool-srpm::

python-linecacwe-srpm:: python-fixtures-srpm
python-linecacwe-srpm:: python-unittest2-srpm

# Actually build in directories
$(EPELPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

$(SETUPPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo `dirname $@`


.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

setuptoolrepo-6-x86_64.cfg: epel-6-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-6-x86_64/setuptoolrepo-6-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[setuptoolrepo]' >> $@
	@echo 'name=setuptoolrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/setuptoolrepo/el/6/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@~
	@mv $@~ $@

setuptoolrepo-7-x86_64.cfg: epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/setuptoolrepo-7-x86_64/g' $@
	@echo '"""' >> $@
	@echo >> $@
	@echo '[setuptoolrepo]' >> $@
	@echo 'name=setuptoolrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=$(REPOBASE)/setuptoolrepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@
	@uniq -u $@ > $@~
	@mv $@~ $@

$(MOCKCFGS)::
	ln -sf --no-dereference /etc/mock/$@ $@

repo: setuptoolrepo.repo
setuptoolrepo.repo:: Makefile setuptoolrepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

setuptoolrepo.repo:: FORCE
	cmp -s /etc/yum.repos.d/$@ $@       


nginx:: nginx/default.d/setuptoolrepo.conf

nginx/default.d/setuptoolrepo.conf:: FORCE nginx/default.d/setuptoolrepo.conf.in
	cat $@.in | \
		sed "s|@REPOBASEDIR@;|$(PWD)/;|g" | tee $@;

nginx/default.d/setuptoolrepo.conf:: FORCE
	cmp -s $@ /etc/$@ || \
	    diff -u $@ /etc/$@

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	rm -f nginx/default.d/*.conf
	@for name in $(SETUPPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(SETUPPKGS)

FORCE::
