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


// void executed_experiment(config conf) {

//     const uint32_t generation_size = conf.genration_size();
//     const uint32_t symbol_size = conf.symbol_size();

//     if (conf.field() == finite_field.binary) {

//     }

// }



int main(int argc, char* argv[])
{



    std::vector<std::tuple<std::chrono::nanoseconds, std::chrono::nanoseconds>> results;

    std::cout << "Experiment started" << std::endl;

    for (uint32_t i = 0; i < 10000; ++i) {
        results.push_back(benchmark<kodo_rlnc::full_vector_encoder<fifi::binary8>>(42, 160, 800));
        std::cout << "...";
    }

    std::cout << std::endl << "Experiment conclude" << std::endl;

    for (auto result : results) {
        auto start = std::get<0>(result);
        auto end = std::get<0>(result);
        auto diff = end.count() - start.count();
        std::cout << "difference " << diff << std::endl;
    }

    return 0;
}
