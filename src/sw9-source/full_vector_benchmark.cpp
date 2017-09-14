#include <cstdint>
#include <iostream>

#include <chrono>

#include <storage/storage.hpp>
#include <fifi/fifi_utils.hpp>

#include <kodo_rlnc/full_vector_codes.hpp>
#include <kodo_core/set_trace_stdout.hpp>

void executed_experiment(config conf) {

    const uint32_t generation_size = conf.genration_size();
    const uint32_t symbol_size = conf.symbol_size();

    if (config.field == finite_field.binary) {

    }

}


int main()
{
    using field_type = fifi::binary8;

    const uint32_t generationSize = 3;

    const uint32_t symbol_size = 1;
    std::cout << "HELLO" << std::endl;
    return 0;
}
