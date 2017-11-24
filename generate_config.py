#!/usr/bin/env python
import math

one_kb = 1024
one_mb = one_kb * one_kb
ten_mb = 10 * one_mb
twenty_mb = 2 * ten_mb
thirdtwo_mb = 32 * one_mb
six = 64 * one_mb
oneh = 128 * one_mb
twof = 256 * one_mb
fivet = 512 * one_mb

one_gb = 1024 * one_mb
two_gb = 2 * one_gb

sizes = [one_kb, one_mb, ten_mb, twenty_mb, thirdtwo_mb, six, oneh, twof, fivet, one_gb, two_gb]
PATH = './configs/'
def write_to_config(config, number, generation_size):
    config_file = '{}{}-config-{}'.format(PATH,generation_size, number)
    f = open(config_file, 'w')
    f.write(config)
    f.close()



def create_config(data_size, generation_size, itterations,
                  finite_field, redundancy):

    symbol_size = int(math.floor(data_size / generation_size))
    return """generation_size:{}
symbol_size:{}
redundancy:{}
finite_field:{}
itterations:{}""".format(generation_size, symbol_size, redundancy,
                                      finite_field, itterations)

def main():


    generation_size = int(input('Generation Size: '))
    finite_field = input('finite_field(1,2,3): ')
    itterations = input('itterations(std=10k): ')
    redundancy = input('redundancy(std=0): ')



    # if len(itterations) == 'std':
    #     itterations = 10000
    # if len(redundancy) == 'std':
    #     redundancy = 0

    x = 1
    for i in sizes:
        config = create_config(i, generation_size, itterations,
                  finite_field, redundancy)
        write_to_config(config, x, generation_size)
        x = x + 1




if __name__ == "__main__":
    main()
