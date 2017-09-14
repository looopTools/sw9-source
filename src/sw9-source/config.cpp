#include "config.hpp"

config::config(std::string file_path) {


}

uint32_t config::symbol_size() {
    return m_symbol_size;
}

uint32_t config::generation_size() {
    return m_generation_size;
}

finite_field field() {
    return m_field;
}
