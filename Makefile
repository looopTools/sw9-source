CC = gcc
includes = -I./kodo./storage
all:
	$(CC) $(includes) ./src/sw9-source/full_rlnc_benchmark.cpp -o ./build/full_rlnc_benchmark
