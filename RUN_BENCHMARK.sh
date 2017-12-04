#!/usr/bin/env bash

sh actual_on_the_fly_encoder_benchmark.sh
sleep 600
sh full_vector_encoder_benchmark.sh
sleep 600
sh on_the_fly_encoder_benchmark.sh
sleep 600
sh perpetual_encoder_benchmark.sh
sleep 600
sh shallow_full_vector_encoder_benchmark.sh
sleep 600
sh shallow_perpetual_encoder_benchmark.sh
