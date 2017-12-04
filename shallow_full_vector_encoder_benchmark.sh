#!/usr/bin/env bash

##################################################################################
#                                                                                #
# This file contains the executin instructions for the Shallow Full Vector       #
# benchmark.                                                                     #
#                                                                                #
##################################################################################

##########################################################################
#                                                                        #
# Generation size 8 benchmark                                            #
#                                                                        #
##########################################################################

./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-1 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-2 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-3 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-4 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-5 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-6 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-7 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-8 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/8-config-9 ./results/encoder/thousand/
sleep 300

##########################################################################
#                                                                        #
# Generation size 16 benchmark                                           #
#                                                                        #
##########################################################################

./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-1 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-2 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-3 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-4 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-5 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-6 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-7 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-8 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/16-config-9 ./results/encoder/thousand/
sleep 300

##########################################################################
#                                                                        #
# Generation size 32 benchmark                                           #
#                                                                        #
##########################################################################

./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-1 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-2 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-3 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-4 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-5 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-6 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-7 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-8 ./results/encoder/thousand/
sleep 300
./build/linux/shallow_full_vector_encoder_benchmark configs/32-config-9 ./results/encoder/thousand/
