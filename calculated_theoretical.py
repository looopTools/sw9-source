#!/usr/bin/env python

one_kb = 1024


def to_mega_byte(data_size):
    return (data_size * one_kb) * 1024

def calculate_symbol_size(generation_size, data_size):

    return data_size / generation_size

def encoding_calculate(generation_size, symbols_size):
    return generation_size * symbol_size
