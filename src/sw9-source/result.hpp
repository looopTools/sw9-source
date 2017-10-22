// result.hpp:
// Contains the class definition for an experimentation result
#include <cstdint>
#include <chrono>

#include <sstream>
#include <string>

class result {
public:
    result(std::chrono::microseconds start, std::chrono::microseconds end,
           uint32_t generation_size, uint32_t symbol_size) :
        m_start(start), m_end(end), m_generation_size(generation_size),
        m_symbol_size(symbol_size) {
        m_data_size = generation_size * symbol_size;
    }

    double throughput() {
        return static_cast<double>(m_data_size / this->latency());
    }

    uint32_t latency() {
        return static_cast<uint64_t>(m_end.count() - m_start.count());
    }

    std::string to_string()
    {
        std::stringstream ss;
        ss << m_start.count() << "," << m_end.count() << "," << m_data_size << ","
           << m_symbol_size << "," << m_generation_size << "," << throughput()
           << "," << latency();
        return ss.str();

    }


private:
    uint32_t m_data_size;
    uint32_t m_symbol_size;
    uint32_t m_generation_size;
    std::chrono::microseconds m_start;
    std::chrono::microseconds m_end;

};
