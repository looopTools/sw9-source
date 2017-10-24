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
#include <sstream>

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
    std::string result_folder = argv[2];
    std::string benchmark_test = "full_vector_encoder";

    auto config = read_config(config_file);
    std::cout << config.symbol_size() << std::endl;

    std::vector<result> results;

    std::string field;
    if (config.field() == 0)
    {
        field = "binary";
        results = run_benchmark<kodo_rlnc::full_vector_encoder<fifi::binary>>(
            config.itterations(), config.generation_size(),
            config.symbol_size(), config.redundancy());
    } else if (config.field() == 1)
    {
        field = "binary8";
        results = run_benchmark<kodo_rlnc::full_vector_encoder<fifi::binary8>>(
            config.itterations(), config.generation_size(),
            config.symbol_size(), config.redundancy());
    } else if (config.field() == 2)
    {
        field = "binary16";
        results = run_benchmark<kodo_rlnc::full_vector_encoder<fifi::binary16>>(
            config.itterations(), config.generation_size(),
            config.symbol_size(), config.redundancy());
    } else
    {
        std::cout << "Unsupported Finit Filed" << std::endl;
        return 0;
    }

    if (results.empty()) {
        std::cout << "Something is wrong" << std::endl;
        return 0;
    }

    std::time_t time_stamp = std::time(nullptr);

    std::stringstream ss;
    ss << result_folder  << time_stamp << "_" << benchmark_test << "_"
       << config.redundancy() << "_" << config.generation_size()
       << "_" << config.symbol_size();
    auto result_path = ss.str();

    auto complete = write_result(results, result_path);
    if (complete)
    {
        std::cout << "bencmark done and result written to "
                  << result_path << std::endl;
    }

    return 0;
}
