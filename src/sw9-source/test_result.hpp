#include <cstdint>
#include <chrono>
#include <string>
#include <fifi/fifi_utils.hpp>

template<typename FiniteField>
class test_result {

public:
    test_result(uint32_t id, uint32_t bytes,
                std::chrono::milliseconds start_time,
                std::chrono::milliseconds end_time);
    double bytes_per_second();
    uint32_t duration();
    uint32_t id();
    std::string test_point();

private:
    uint32_t m_id;
    uint32_t m_bytes; // Amount of bytes encoded
    FiniteField field;
    std::chrono::milliseconds m_start_time;
    std::chrono::milliseconds m_end_time;
};
