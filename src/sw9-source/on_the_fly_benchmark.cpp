// On the fly benchmark
#include <chrono>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <vector>

#include <storage/storage.hpp>
#include <fifi/fifi_utils.hpp>

#include <kodo_rlnc/on_the_fly_codes.hpp>
#include <kodo_core/set_trace_stdout.hpp>



int main()
{
    srand(static_cast<uint32_t>(time(0)));

    using field_type = fifi::binary8;

    const uint32_t generation_size = 42;
    const uint32_t symbol_size = 160;

    using rlnc_encoder = kodo_rlnc::on_the_fly_encoder<field_type>;
    rlnc_encoder::factory factory(generation_size, symbol_size);
    auto encoder = factory.build();

     std::vector<std::vector<uint8_t>> payloads(2 * generation_size,
                                              std::vector<uint8_t>(
                                                  encoder->payload_size()));

    std::vector<uint8_t> data(encoder->block_size());

    std::cout << encoder->block_size() << std::endl; // 6720

    std::generate(data.begin(), data.end(), rand);

    encoder->set_const_symbols(storage::storage(data));

    auto start = std::chrono::high_resolution_clock::now();
    for (auto& payload : payloads)
    {
        encoder->write_payload(payload.data());
    }
    auto end = std::chrono::high_resolution_clock::now();

    auto diff =
        std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

    std::cout << "Differens " << diff.count() << std::endl;

    std::cout << "HELLO" << std::endl;
    return 0;
}
