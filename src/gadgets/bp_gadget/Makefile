CXX= g++
CXX_FLAGS= -c -O0

CONF_NAMESPACE = bp_gadget_default
NAME = bp_gadget
LIB_NAME = ""

#! SYS_CONFIGS
#=> Loading such configs during runtime will hinder the Gadget's impact. Therefore it should be handled beforehands
BTB_SIZE=4096

#! FEATURES -> 5 configurations
TOKENIZED=0
TAIL=0
BAD_SORT=0
IMPROVE_CPI=0
BRUTE_FORCE=0
TRUE_RND=0
CUSTOM_RNG=0
#! KNOBS
LOPSIDE=0
ALLOC_SCALER=2
OPS_SCALER=1

####### Configuration 1 #####
c1: c1_set_primary_namespace c1_set_lib_name c1_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c1_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c1)

c1_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c1.a)

c1_set_feature_flags:
	$(eval TOKENIZED=1)

####### Configuration 2 #####
c2: c2_set_primary_namespace c2_set_lib_name c2_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c2_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c2)

c2_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c2.a)

c2_set_feature_flags:
	$(eval TAIL=1)

####### Configuration 3 #####
c3: c3_set_primary_namespace c3_set_lib_name c3_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c3_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c3)

c3_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c3.a)

c3_set_feature_flags:
	$(eval BAD_SORT=1)

####### Configuration 4 #####
c4: c4_set_primary_namespace c4_set_lib_name c4_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c4_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c4)

c4_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c4.a)

c4_set_feature_flags:
	$(eval TOKENIZED=1)
	$(eval IMPROVE_CPI=1)

####### Configuration 5 #####
c5: c5_set_primary_namespace c5_set_lib_name c5_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c5_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c5)

c5_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c5.a)

c5_set_feature_flags:
	$(eval TAIL=1)
	$(eval IMPROVE_CPI=1)

####### Configuration 6 #####
c6: c6_set_primary_namespace c6_set_lib_name c6_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c6_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c6)

c6_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c6.a)

c6_set_feature_flags:
	$(eval BRUTE_FORCE=1)

####### Configuration 7 #####
c7: c7_set_primary_namespace c7_set_lib_name c7_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c7_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c7)

c7_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c7.a)

c7_set_feature_flags:
	$(eval TOKENIZED=1)
	$(eval TRUE_RND=1)

####### Configuration 8 #####
c8: c8_set_primary_namespace c8_set_lib_name c8_set_feature_flags bp_gadget.o
	ar crsv $(LIB_NAME) bp_gadget.o

c8_set_primary_namespace:
	$(eval CONF_NAMESPACE=bp_gadget_c8)

c8_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c8.a)

c8_set_feature_flags:
	$(eval BRUTE_FORCE=1)
	$(eval CUSTOM_RNG=1)

##################### COMMON ########################
bp_gadget.o: bp_gadget.cc bp_gadget.h
	$(CXX) $(CXX_FLAGS) -DNS_NAME=$(CONF_NAMESPACE) -DCUSTOM_RNG=$(CUSTOM_RNG) -DBRUTE_FORCE=$(BRUTE_FORCE) -DTRUE_RND=$(TRUE_RND) -DTAIL=$(TAIL) -DBAD_SORT=$(BAD_SORT) -DTOKENIZED=$(TOKENIZED) -DIMPROVE_CPI=$(IMPROVE_CPI) -DBTB_SIZE=$(BTB_SIZE) -DLOPSIDE=$(LOPSIDE) -DALLOC_SCALER=$(ALLOC_SCALER) -DOPS_SCALER=$(OPS_SCALER) bp_gadget.cc -o bp_gadget.o

.PHONY: clean
clean:
	rm -f *.o *.bin *.a *.ar *.ii *.s