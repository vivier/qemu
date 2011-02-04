-include ../config-host.mak
-include $(SRC_PATH)/rules.mak

# TODO: duplicate from Makefile, to be removed once Makefile.objs lands.
libcacard-y = cac.o event.o passthru.o vcard.o vreader.o vcard_emul_nss.o \
              vcard_emul_type.o card_7816.o

$(call set-vpath, $(SRC_PATH):$(SRC_PATH)/libcacard)

vscclient: $(libcacard-y) vscclient.o
	$(call quiet-command,$(CC) $(libcacard_libs) -o $@ $^,"  LINK  $(TARGET_DIR)$@")

all: vscclient

clean:
	rm -f *.o */*.o *.d */*.d *.a */*.a *~ */*~ vscclient
