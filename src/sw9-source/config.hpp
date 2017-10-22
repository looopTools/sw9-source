#pragma once

#include <string>

class config
{
public:
    config()
    {}

    uint32_t symbol_size()
    {
        return m_symbol_size;
    }

    void set_symbol_size(uint32_t symbol_size)
    {
        m_symbol_size = symbol_size;
    }

    uint32_t generation_size()
    {
        return m_generation_size;
    }

    void set_generation_size(uint32_t generation_size)
    {
        m_generation_size = generation_size;
    }

    uint32_t redudancy()
    {
        return m_reducancy;
    }

    void set_reducancy(uint32_t reducancy)
    {
        m_reducancy = reducancy;
    }

    uint32_t itterations()
    {
        return m_itterations;
    }

    void set_itterations(uint32_t itterations)
    {
        m_itterations = itterations;
    }

    uint16_t field()
    {
        return m_field;
    }

    void set_field(uint16_t field)
    {
        m_field = field;
    }
private:
    uint32_t m_symbol_size;
    uint32_t m_generation_size;
    uint32_t m_reducancy;
    uint32_t m_itterations;
    uint16_t m_field;
};
