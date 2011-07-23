SRC=power_meter.py
DEST=pmeter
PROG=$(BIN)/$(DEST)
CNAME=voltages
ETC=/etc
CONF=$(ETC)/$(CNAME)
BIN=/usr/local/bin

install:
	cp $(SRC) $(PROG)
	chmod 755 $(PROG)
	sed -i "s/\(^CONFIG_FILE\s*=\s*\)'.*'/\1'\/etc\/voltages'/" $(PROG)
	echo "0" > /$(CONF)
	chmod 666 $(CONF)
	echo 'Initial set-up run:'
	$(PROG)

distclean:
	rm -rf $(PROG) $(CONF)
