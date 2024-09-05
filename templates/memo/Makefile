CXX= g++ 
CXX_FLAGS=-O0 -c -Igadget_headers

.PHONY: clean
clean:
	rm -f *.o *.bin *.a *.ar *.ii *.s *.out

.PHONY: tidy
tidy:
	rm -f *.o

#! FEATURES
COMPUTE=0
FS_USAGE=0
MEM_USAGE=0

c1: c1_set_feature_flags derive

c1_set_feature_flags:
	$(eval MEM_USAGE=1)

c2: c2_set_feature_flags derive

c2_set_feature_flags:
	$(eval MEM_USAGE=1)
	$(eval FS_USAGE=1)

c3: c3_set_feature_flags derive

c3_set_feature_flags:
	$(eval MEM_USAGE=1)
	$(eval COMPUTE=1)

c4: c4_set_feature_flags derive

c4_set_feature_flags:
	$(eval MEM_USAGE=1)
	$(eval COMPUTE=1)
	$(eval FS_USAGE=1)

c5: c5_set_feature_flags derive

c5_set_feature_flags:
	$(eval COMPUTE = 1)
	$(eval FS_USAGE = 1)

derive: main.cc
	$(CXX) $(CXX_FLAGS) -DCOMPUTE=$(COMPUTE) -DMEM_USAGE=$(MEM_USAGE) -DFS_USAGE=$(FS_USAGE) main.cc

make link:
	$(CXX) 