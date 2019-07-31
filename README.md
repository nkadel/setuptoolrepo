setuptoolrepo
=============

Wrapper for SRPM building tools for python setuptools and pip update

The python-setuptools packages for RHEL 6 and 7 are so out of date
they can no longer compile contemporary modules from
https://pypi.org. It's useful to able to install RPMs, especially to
use inside "mock", for building other RPMs of modern modules.

python-pip is also updated, but only for RHEL 7 since the RHEL 6 update
is simply impossible.

Git Checkout
===========

This repository relies on extensive git submodules. When cloneing it locally, use:

* git clone https://github.com/nkadel/setuptoolrepo

*** NOTE: The git repos at github.com do not include the tarballs ***

This is for basic security reasons: you'll need to get the tarballs
with "make getsrc" as needed.

Building setuptools
==============

These are rebuilt from Fedora rawhide releases, or using "py2pack" and
need to be built and installed in the following order.

* make cfgs # Create local .cfg configs for "mock".
* * epel-6-x86_64.cfg # Used for some Makefiles
* * epel-7-x86_64.cfg # Used for some Makefiles
* * setuptoolrepo-6-x86_64.cfg # Activates local RPM dependency repository
* * setuptoolrepo-7-x86_64.cfg # Activates local RPM dependency repository

* make repos # Creates local local yum repositories in $PWD/setuptoolrepo
* * setuptoolrepo/el/6
* * setuptoolrepo/el/7

* make # Make all distinct versions using "mock"

Building a compoenent, without "mock" and in the local working system,
can also be done for testing.

* make build

setuptool also relies on a contemporary "certifi" module

Installing setuptool
==============--====

The relevant yum repository is built locally in samba4reepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Setuptool RPM Build Security
============================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPG signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

		Nico Kadel-Garcia <nkadel@gmail.com>
