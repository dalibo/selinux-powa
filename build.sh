#!/bin/bash -eux

make -f /usr/share/selinux/devel/Makefile NAME=targeted
semodule -i powa.pp
