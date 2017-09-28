#include <string>

enum finite_field {binary, binary8}; // TODO: Extend
class config
{
public:
    config(std::string file_path);
    uint32_t symbol_size();
    uint32_t generation_size();
    finite_field field();
private:
    std::string extract_by_key(std::string data, std::string key);
private:
    uint32_t m_symbol_size;
    uint32_t m_generation_size;
    finite_field m_field;
};
