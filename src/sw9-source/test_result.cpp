#include "test_result.hpp"

test_result::test_result(uint32_t id, uint32_t bytes,
                         std::chrono::milliseconds start_time,
                         std::chrono::milliseconds end_time) : m_id(id),
                                                               m_bytes(bytes),
                                                               m_start_time(start_time),
                                                               m_end_time(end_time)
{}

double test_result::bytes_ber_second() {
    return static_cast<double>(m_bytes / this.duration());
}

uint32_t test_result::duration() {
    auto res = m_end_time.count() - m_start_time.count();
    return static_cast<uint32_t>(res);

}

std::string test_result::test_point() {
    return "(" + m_id + "," + m_bytes + "," + m_start_time.count
}
