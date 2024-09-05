CXX= g++ 
CXX_FLAGS=-O0 -c -Igadget_headers

.PHONY: clean
clean:
	rm -f *.o *.bin *.a *.ar *.ii *.s

.PHONY: tidy
tidy:
	rm -f *.o

#! FEATURES
DFT=0
PI_GEN=0
FACTORIAL=0
FIBO=0

c1: c1_set_feature_flags derive

c1_set_feature_flags:
	$(eval DFT=1)

c2: c2_set_feature_flags derive

c2_set_feature_flags:
	$(eval DFT=1)
	$(eval PI_GEN=1)

c3: c3_set_feature_flags derive

c3_set_feature_flags:
	$(eval DFT=1)
	$(eval FACTORIAL=1)

c4: c4_set_feature_flags derive

c4_set_feature_flags:
	$(eval FIBO=1)

c5: c5_set_feature_flags derive

c5_set_feature_flags:
	$(eval FIBO=1)
	$(eval PI_GEN=1)

c6: c6_set_feature_flags derive

c6_set_feature_flags:
	$(eval FIBO=1)
	$(eval FACTORIAL=1)

c7: c7_set_feature_flags derive

c7_set_feature_flags:
	$(eval FACTORIAL=1)

derive: main.cc
	$(CXX) $(CXX_FLAGS) -DDFT=$(DFT) -DPI_GEN=$(PI_GEN) -DFACTORIAL=$(FACTORIAL) -DFIBO=$(FIBO) main.cc

