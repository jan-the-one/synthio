CXX= g++
CXX_FLAGS= -c -O0

CONF_NAMESPACE = cache_gadget_default
NAME = cache_gadget
LIB_NAME = ""

#! SYS_CONFIGS
#=> Loading such configs during runtime will hinder the Gadget's impact. Therefore it should be handled beforehands
L1_CACHE_SIZE=0
L2_CACHE_SIZE=0
L3_CACHE_SIZE=0

#! FEATURES
READS_WORKLOAD = 0
WRITES_WORKLOAD = 0
REDUCE_CACHEING = 0
WRECK_L2 = 0
WRECK_L3 = 0
IMPROVE_L1_RATE = 0
BIG_WRITES = 0

#! KNOBS
WORKING_SET_SCALER = 1
ALLOC_SCALER = 1
OPS_SCALER = 1

####### Configuration 1 #####
c1: c1_set_primary_namespace c1_set_lib_name c1_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c1_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c1)

c1_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c1.a)

c1_set_feature_flags:
	$(eval READS_WORKLOAD=1)

####### Configuration 2 #####
c2: c2_set_primary_namespace c2_set_lib_name c2_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c2_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c2)

c2_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c2.a)

c2_set_feature_flags:
	$(eval READS_WORKLOAD=1)
	$(eval REDUCE_CACHEING=1)
####### Configuration 3 #####
c3: c3_set_primary_namespace c3_set_lib_name c3_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c3_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c3)

c3_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c3.a)

c3_set_feature_flags:
	$(eval READS_WORKLOAD=1)
	$(eval WRECK_L2=1)

####### Configuration 4 #####
c4: c4_set_primary_namespace c4_set_lib_name c4_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c4_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c4)

c4_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c4.a)

c4_set_feature_flags:
	$(eval READS_WORKLOAD=1)
	$(eval WRECK_L2=1)
	$(eval IMPROVE_L1_RATE=1)
####### Configuration 5 #####
c5: c5_set_primary_namespace c5_set_lib_name c5_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c5_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c5)

c5_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c5.a)

c5_set_feature_flags:
	$(eval READS_WORKLOAD=1)
	$(eval WRECK_L3=1)
####### Configuration 6 #####
c6: c6_set_primary_namespace c6_set_lib_name c6_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c6_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c6)

c6_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c6.a)

c6_set_feature_flags:
	$(eval READS_WORKLOAD=1)
	$(eval IMPROVE_L1_RATE=1)
	$(eval WRECK_L3=1)

##############################
####### Configuration 7 #####
c7: c7_set_primary_namespace c7_set_lib_name c7_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c7_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c7)

c7_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c7.a)

c7_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
	$(eval WRECK_L3=1)
####### Configuration 8 #####
c8: c8_set_primary_namespace c8_set_lib_name c8_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c8_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c8)

c8_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c8.a)

c8_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
	$(eval REDUCE_CACHEING=1)
####### Configuration 9 #####
c9: c9_set_primary_namespace c9_set_lib_name c9_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c9_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c9)

c9_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c9.a)

c9_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
####### Configuration 10 #####
c10: c10_set_primary_namespace c10_set_lib_name c10_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c10_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c10)

c10_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c10.a)

c10_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
	$(eval WRECK_L2=1)

####### Configuration 11 #####
c11: c11_set_primary_namespace c11_set_lib_name c11_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c11_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c11)

c11_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c11.a)

c11_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
	$(eval BIG_WRITES=1)

####### Configuration 12 #####
c12: c12_set_primary_namespace c12_set_lib_name c12_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c12_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c12)

c12_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c12.a)

c12_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
	$(eval WRECK_L2=1)
	$(eval BIG_WRITES=1)

####### Configuration 11 #####
c13: c13_set_primary_namespace c13_set_lib_name c13_set_feature_flags cache_gadget.o
	ar crsv $(LIB_NAME) cache_gadget.o

c13_set_primary_namespace:
	$(eval CONF_NAMESPACE=cache_gadget_c13)

c13_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c13.a)

c13_set_feature_flags:
	$(eval WRITES_WORKLOAD=1)
	$(eval WRECK_L3=1)
	$(eval BIG_WRITES=1)


####### TODO: Configuration XX ##############

#! We should add a case when we have zero-paging hits, but still a lot of TLB misses.
#! This should be added to the "READS" part.

##################### COMMON ########################
cache_gadget.o: load_sys_configs cache_gadget.cc cache_gadget.h
	$(CXX) $(CXX_FLAGS) -DNS_NAME=$(CONF_NAMESPACE) -DREADS_WORKLOAD=$(READS_WORKLOAD) -DWRITES_WORKLOAD=$(WRITES_WORKLOAD) -DWRECK_L2=$(WRECK_L2) -DWRECK_L3=$(WRECK_L3) -DREDUCE_CACHEING=$(REDUCE_CACHEING) -DIMPROVE_L1_RATE=$(IMPROVE_L1_RATE) -DBIG_WRITES=$(BIG_WRITES) -DL1_CACHE_SIZE=$(L1_CACHE_SIZE) -DL2_CACHE_SIZE=$(L2_CACHE_SIZE) -DL3_CACHE_SIZE=$(L3_CACHE_SIZE) -DWORKING_SET_SCALER=$(WORKING_SET_SCALER) -DALLOC_SCALER=$(ALLOC_SCALER) -DOPS_SCALER=$(OPS_SCALER) cache_gadget.cc -o cache_gadget.o

load_sys_configs:
	$(eval L1_CACHE_SIZE= $(shell getconf 'LEVEL1_DCACHE_SIZE'))
	$(eval L2_CACHE_SIZE= $(shell getconf 'LEVEL2_CACHE_SIZE'))
	$(eval L3_CACHE_SIZE= $(shell getconf 'LEVEL3_CACHE_SIZE'))

.PHONY: clean
clean:
	rm -f *.o *.bin *.a *.ar