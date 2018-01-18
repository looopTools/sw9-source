# sw9-source

This repository contains a benchmark suite for Random Linear Network Coding (RLNC) codes,
which are able to run experiments based on alterations to symbol size, generation size, and
amount of redundancy packets.

The goal is to enable to software developers and research to make informed decision when
choosing an RLNC code and its configuration.

This repository contains the source code developed during my 9th

This repository contains the source code used in my 9th semester project,
as part of my M.Sc Software. The source code is used for performance testing of RLNC codes

# License

This repository and the code is under the MIT software License, for further information see the LICENSE
file include in this repository

## Building

To build the project execute `python waf configure build`

## To run Benchmark

To run benchmark execute `sh RUN_BENCHMARK.sh`

## /configs
Contains the configuration files used in the project. If you want to create your own configuration
file they have the following format:

    generation_size:UINT32
    symbol_size:UINT32
    data_size:UINT32
    finit_field:UINT32


## Data Analysis using Jupyter Notebook

The benchmark tool does not come with a build in data analysis tool, however, python and the packets scipy, numpy, and matplotlib has been used to do
data analysis and visualise the data result. All this is available in a Jupyter Notbook also include in this repository. For usage of Jupyter Notbook see
[installation][:1]


## TODO

This section contains a list of elements I would like to change or improve about the benchmark suite.


# Project overview

Here a an overview of where files are locate are presented.

`/configs/` contains the configurations files used for the experiments
`/results/` contains the result files for all experiments
`/src/sw9-source/encoder` contains the source code used for the benchmarks

[:1] http://jupyter.org/install.html Jupyter Notebook installation
