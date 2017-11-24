# Hacking on selinux-powa

## Updating policy

A `Makefile` provides useful targets to help the REPL of SELinux policy
maintainance.


``` bash
# Switch to permissive
setenforce 0

# Build and load current policy
make load

# Now test it, browse powa, etc.
make test
systemctl stop powa-main

# Update the policy with audit2allow
make powa.te

# Test it again with enforcing.
setenforce 1
make load test
```

You should now refine policy manually and commit it.


## Building rpm

The `./rpm.sh` script requires only yum to build a RPM package. A
`docker-compose.yml` is shipped to help reproduce a clean target system. Run
`docker-compose run --rm rpm` to generate a RPM in `rpm/`.


## References

- [Fedora Howto](https://fedoraproject.org/wiki/SELinux/IndependentPolicy)
- [SELinux Policy reference](http://oss.tresys.com/docs/refpolicy/api/).
- [Packaging SELinux policy for
  RPM](https://fedoraproject.org/wiki/SELinux_Policy_Modules_Packaging_Draft).
- [Fedora SELinux policies](https://github.com/fedora-selinux/selinux-policy)
- `#selinux` at `irc.freenode.net` . People here are very helpful.
