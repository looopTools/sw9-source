#pragma once

#include "config.hpp"

#include <fstream>
#include <sstream>
#include <string>

#include <iostream>

int extract_config(std::string line)
{

    std::stringstream ss;
    ss.str(line);
    std::string temp;
    int i = 0;
    int setting;
    while (std::getline(ss, temp, ':'))
    {
        if (i != 0)
        {
            setting = std::stoi(temp);
        }
        ++i;
    }
    return setting;
}

void set_parameter(config* conf, int setting, int line_number)
{

    if (line_number == 0)
    {
        conf->set_generation_size(setting);
    } else if (line_number == 1) {
        conf->set_symbol_size(setting);
    } else if (line_number == 2) {
        conf->set_redundancy(setting);
    } else if (line_number == 3){
        conf->set_field(setting);
    } else {
        conf->set_itterations(setting);
    }

}

config read_config(std::string file_path)
{

    std::ifstream file(file_path);
    std::string line;
    int line_number = 0;

    auto conf = config();

    while (std::getline(file, line))
    {
        set_parameter(&conf, extract_config(line), line_number);
        ++line_number;

    }

    return conf;

}
