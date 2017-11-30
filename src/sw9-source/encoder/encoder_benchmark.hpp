////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 2017 Lars Nielsen
////////////////////////////////////////////////////////////////////////////////
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
////////////////////////////////////////////////////////////////////////////////
// Encoder Benchmark for Systematic RLNC CODES
// This file contains the benchmarking code for RLNC Codes able to run
// in a systematic or non systematic form
////////////////////////////////////////////////////////////////////////////////

#include "../result.hpp"

// Kodo includes
#include <storage/storage.hpp>

// Standard library includes
#include <chrono>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <ctime>
#include <vector>
#include <cstdlib>
#include <string>
#include <iostream>
#include <fstream>

bool write_result(std::vector<result> results, std::string file_path)
{
    std::ofstream result_file;
    result_file.open(file_path);
    for (auto result : results)
    {
        result_file << result.to_string() << std::endl;
    }
    result_file.close();
    return true;
}

uint32_t random_index(uint32_t length)
{
    std::srand(std::time(0)); // use current time as seed for random generator
    return static_cast<uint32_t>(std::rand() % length - 1);  // generates a random number between 0 and length -1
}

template<typename Code>
result encoder_benchmark(uint32_t generation_size, uint32_t symbol_size,
                         uint32_t redundancy, bool systematic)
{
    // Seed for the random generator
    srand(static_cast<uint32_t>(time(0)));

    typename Code::factory factory(generation_size, symbol_size);
    auto encoder = factory.build();

    // If systematic is off, the linear combination of packets
    // will happen along the way
    if (!systematic)
    {
        encoder->set_systematic_off();
    }

    std::vector<std::vector<uint8_t>> payloads(generation_size,
                                               std::vector<uint8_t>(
                                                   encoder->payload_size()));

    std::vector<uint8_t> data(encoder->block_size());

    // fill the data vector with random data
    std::generate(data.begin(), data.end(), rand);

    // Fill the encoder with the data from the start
    // so we can start encoding
    encoder->set_const_symbols(storage::storage(data));

    ////////////////////////////////////////////////////////////////////////////
    // Begining the timed experiment                                          //
    ////////////////////////////////////////////////////////////////////////////

    auto start = std::chrono::high_resolution_clock::now();

    // Start encoding
    for (auto& payload : payloads)
    {
        encoder->write_payload(payload.data());
    }

    // If Systematic is off, some redundancy packets are need to ensure
    // all coded symbols are generated
    for (uint32_t i = 0; i < redundancy; ++i)
    {
       encoder->write_payload(payloads[random_index(payloads.size())].data());
    }
    // Encoding done
    auto end = std::chrono::high_resolution_clock::now();

    ////////////////////////////////////////////////////////////////////////////
    // Experiment complet                                                     //
    ////////////////////////////////////////////////////////////////////////////


    auto s = std::chrono::duration_cast<std::chrono::microseconds>(
        start.time_since_epoch());
    auto e = std::chrono::duration_cast<std::chrono::microseconds>(
        end.time_since_epoch());
    return result(s, e, generation_size, symbol_size);

}

template<typename Code>
std::vector<result> run_benchmark(uint32_t itterations, uint32_t generation_size,
                                  uint32_t symbol_size, uint32_t redundancy,
                                  bool systematic)
{

    std::cout << "Experiment Started " << std::endl;

    std::vector<result> results;

    for (uint32_t i = 0; i < itterations; ++i) {
        results.push_back(encoder_benchmark<Code>(generation_size,
                                                  symbol_size, redundancy,
                                                  systematic));
    }
    std::cout << "Experiment Finished" << std::endl;
    return results;
}
