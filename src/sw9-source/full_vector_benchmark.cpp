// Full Vector Benchmark

#include "config.hpp"
#include "benchmark.hpp"

#include <chrono>
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <vector>
#include <tuple>
#include <storage/storage.hpp>
#include "config.hpp"
#include "config_reader.hpp"

#include <fifi/fifi_utils.hpp>

#include <kodo_rlnc/full_vector_codes.hpp>
#include <kodo_core/set_trace_stdout.hpp>

#include <iostream>

int main(int argc, char* argv[])
{

    if (argc < 2)
    {
        std::cout << "file path must be provided" << std::endl;
        return -1;
    }

    std::string config_file = argv[1];

    auto config = read_config(config_file);
    std::cout << config.symbol_size() << std::endl;

    if (config.field() == 0)
    {
        run_benchmark<kodo_rlnc::full_vector_encoder<fifi::binary>>(
            config.itterations(), config.generation_size(),
            config.symbol_size(), config.data_size());
    } else if (config.field() == 1)
    {
        run_benchmark<kodo_rlnc::full_vector_encoder<fifi::binary8>>(
            config.itterations(), config.generation_size(),
            config.symbol_size(), config.data_size());
    }

    return 0;
}
