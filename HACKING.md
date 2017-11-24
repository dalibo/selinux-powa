# Hacking on selinux-powa

The `./rpm.sh` script requires only yum to build a RPM package. A
`docker-compose.yml` is shipped to help reproduce a clean target system. Run
`docker-compose run --rm rpm` to generate a RPM in `rpm/`.
