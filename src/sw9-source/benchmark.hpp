#include <chrono>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <ctime>
#include <vector>
#include <tuple>
#include <storage/storage.hpp>

// change to return to match data
template<typename Code>
std::tuple<std::chrono::nanoseconds, std::chrono::nanoseconds> benchmark(uint32_t generation_size,
               uint32_t symbol_size,
               uint32_t data_size)
{
    // Seed random generator
    srand(static_cast<uint32_t>(time(0)));

    typename Code::factory factory(generation_size, symbol_size);
    auto encoder = factory.build();

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
    for (auto& payload : payloads)
    {
        encoder->write_payload(payload.data());
    }
    auto end = std::chrono::high_resolution_clock::now();

    return std::make_tuple(std::chrono::duration_cast<std::chrono::nanoseconds>(start.time_since_epoch()),
                           std::chrono::duration_cast<std::chrono::nanoseconds>(end.time_since_epoch()));
}
