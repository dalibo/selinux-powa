default:

CHECKPOINT=audit.checkpoint
audit.te: /var/log/audit/audit.log $(CHECKPINT)
	ausearch --checkpoint $(CHECKPOINT) -m avc,user_avc,selinux_err -ts checkpoint -i | audit2allow -RM $(basename $@);

powa.te: audit.te
	sed -i '/^# START AUDIT2ALLOW/,$$d' $@
	@echo -e '# START AUDIT2ALLOW\n' >> $@
	sed -n '/^require/,$$p' $< >> $@

.PHONY: powa.pp
powa.pp:
	make -f /usr/share/selinux/devel/Makefile NAME=targeted $@

load: powa.pp
	semodule -i $<
	restorecon -RvF $$(readlink -e /usr/bin/powa* /etc/powa* /etc/postgresql /var/log/po*)
	ausearch --checkpoint $(CHECKPOINT) -ts recent >/dev/null

UNIT?=powa-main
test:
	systemctl stop $(UNIT)
	systemctl start $(UNIT)
	systemctl status $(UNIT)
	ps -efZ | grep powa-main
	getenforce
	journalctl -fu $(UNIT)

clean:
	rm -f powa.pp
