#!/bin/bash -eux

teardown() {
    chown --changes -R $(stat -c %u:%g $0) *

    # Ease debugging from Docker container by waiting for explicit shutdown.
    if [ -z "${CI-}" ] && ! test -t 0 ; then
        tail -f /dev/null
    fi
}

trap teardown EXIT INT TERM

srcdir=$(readlink -m $0/..)
cd $srcdir

chown --changes -R $(id -nu):$(id -ng) selinux* powa*

topdir=${PWD}/rpm
mkdir -p $topdir

yum install -y rpm-build
yum-builddep -y selinux-policy-powa.spec
rpmbuild -bb \
    --define "_topdir ${topdir}" \
    --define "_sourcedir ${srcdir}" \
    selinux-policy-powa.spec

# Test it
yum install -y rpm/RPMS/noarch/selinux-policy-powa-*.noarch.rpm
/usr/libexec/selinux/hll/pp /usr/share/selinux/targeted/powa.pp
