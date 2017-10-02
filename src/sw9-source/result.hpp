// result.hpp:
// Contains the class definition for an experimentation result
#include <cstdint>
#include <chrono>

class result {
public:
    result(std::chrono::microseconds start, std::chrono::microseconds end, uint32_t data_size) :
        m_start(start), m_end(end), m_data_size(data_size) {

    }

    double throughput() {
        return static_cast<double>(m_data_size / this->latency());
    }

    uint32_t latency() {
        return static_cast<uint64_t>(m_end.count() - m_start.count());
    }

private:
    uint32_t m_data_size;
    std::chrono::microseconds m_start;
    std::chrono::microseconds m_end;

};
