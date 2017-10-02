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
#include <fifi/fifi_utils.hpp>

#include <kodo_rlnc/full_vector_codes.hpp>
#include <kodo_core/set_trace_stdout.hpp>

int main(int argc, char* argv[])
{



    std::vector<std::tuple<std::chrono::microseconds, std::chrono::microseconds>> results;

    std::cout << "Experiment started" << std::endl;

    for (uint32_t i = 0; i < 10000; ++i) {
        results.push_back(benchmark<kodo_rlnc::full_vector_encoder<fifi::binary8>>(42, 160, 800));
        std::cout << "...";
    }

    std::cout << std::endl << "Experiment conclude" << std::endl;

    for (auto result : results) {
        auto start = std::get<0>(result);
        auto end = std::get<1>(result);
        auto diff = end.count() - start.count();
        std::cout << "difference " << diff << std::endl;
    }

    return 0;
}
