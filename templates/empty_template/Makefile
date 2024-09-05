CXX=g++ 
CXX_FLAGS=-O0 -c -Igadget_headers

.PHONY: clean
clean:
	rm -f *.o *.bin *.a *.ar *.ii *.s

.PHONY: tidy
tidy:
	rm -f *.o

#! FEATURES
TEST=0

c9: c9_set_feature_flags derive

c9_set_feature_flags:
	$(eval TEST=1)

derive: main.cc
	$(CXX) $(CXX_FLAGS) -DTEST=$(TEST) main.cc
