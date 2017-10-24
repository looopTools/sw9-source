#include "result.hpp"

#include <chrono>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <ctime>
#include <vector>
#include <cstdlib>

#include <storage/storage.hpp>

#include <string>

// Used for file writing
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

// change to return to match data
// data size with generation size and symbols = gen * symbs
template<typename Code>
result benchmark(uint32_t generation_size,
                 uint32_t symbol_size, uint32_t redundancy)
{
    // Seed random generator
    srand(static_cast<uint32_t>(time(0)));

    typename Code::factory factory(generation_size, symbol_size);
    auto encoder = factory.build();

    // CODING ALWAYS
    encoder->set_systematic_off();

    // https://github.com/steinwurf/kodo-rlnc/blob/master/examples/encode_decode_simple/encode_decode_simple.cpp
    // https://github.com/steinwurf/kodo-rlnc/blob/master/examples/encode_decode_separate/encode_decode_separate.cpp
    std::vector<std::vector<uint8_t>> payloads(2 * generation_size,
                                              std::vector<uint8_t>(
                                                  encoder->payload_size()));

    std::vector<uint8_t> data(encoder->block_size());

    //std::cout << encoder->block_size() << std::endl; // 6720

    std::generate(data.begin(), data.end(), rand);

    encoder->set_const_symbols(storage::storage(data));

    auto start = std::chrono::high_resolution_clock::now();

    // INCREASE IF SYS IS OFF
    for (auto& payload : payloads)
    {
         encoder->write_payload(payload.data());
    }

    for (uint32_t i = 0; i < redundancy; ++i)
    {
        encoder->write_payload(payloads[random_index(payloads.size())].data());
        // encoder->write_payload(payloads[random_index(payloads.length())];
    }


    auto end = std::chrono::high_resolution_clock::now();

    auto s = std::chrono::duration_cast<std::chrono::microseconds>(
        start.time_since_epoch());
    auto e = std::chrono::duration_cast<std::chrono::microseconds>(
        end.time_since_epoch());
    return result(s, e, generation_size, symbol_size);
}

template<typename Code>
std::vector<result> run_benchmark(uint32_t itterations, uint32_t generation_size,
                                  uint32_t symbol_size, uint32_t redundancy)
{

    std::cout << "Experiment Started " << std::endl;

    std::vector<result> results;
    for (uint32_t i = 0; i < itterations; ++i) {
        results.push_back(benchmark<Code>(generation_size,
                                          symbol_size, redundancy));
        std::cout << "...";
    }

    return results;
}
