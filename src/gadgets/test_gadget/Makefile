#! The namespace must should correspond to the NAME part plus the target part.
#! the target parts defined here (i.e. c1, c2) should match the configuration names in the gadget registration file
CONF_NAMESPACE = test_gadget_default
#! The NAME is used to name the library, and must match with the name used in the config for gadget registration!
NAME = test_gadget
LIB_NAME = ""

FEATURE_A = 0
FEATURE_B = 0
RANDOM_KNOB = 0
###! CONFIG 1 - TEST GADGET ###
c1: c1_set_primary_namespace c1_set_lib_name c1_set_feature_flags test_gadget.o
	ar crsv $(LIB_NAME) test_gadget.o

c1_set_primary_namespace:
	$(eval CONF_NAMESPACE=test_gadget_c1)

c1_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c1.a)

c1_set_feature_flags:
	$(eval FEATURE_A=0)
	$(eval FEATURE_B=1)

###! CONFIG 2 - TEST GADGET ###
c2: c2_set_primary_namespace c2_set_lib_name c2_set_feature_flags test_gadget.o
	ar crsv $(LIB_NAME) test_gadget.o

c2_set_primary_namespace:
	$(eval CONF_NAMESPACE=test_gadget_c2)

c2_set_lib_name:
	$(eval LIB_NAME=$(NAME)_c2.a)

c2_set_feature_flags:
	$(eval FEATURE_A=1)
	$(eval FEATURE_B=0)

#This target is shared by all other targets
test_gadget.o: test_gadget.cc test_gadget.h
	g++ -c -DNS_NAME=$(CONF_NAMESPACE) -DFEATURE_A=$(FEATURE_A) -DFEATURE_B=$(FEATURE_B) -DRANDOM_KNOB=$(RANDOM_KNOB) test_gadget.cc -o test_gadget.o

.PHONY: sanity_check
sanity_check:
	rm less.txt

.PHONY: clean
clean:
	rm -f *.o *.bin *.a *.ar