#include "config.hpp"

#include <fstream>
#include <string>

config::config(std::string file_path) {

    std::ifstream infile(file_path);

    std::string

}

std::string config::extract_by_key(std::string data, std::string key) {

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
