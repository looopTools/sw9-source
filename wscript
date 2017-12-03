#! /usr/bin/env python
# encoding: utf-8

APPNAME = 'rlnc-benchmark'
VERSION = '1.0.0'


def build(bld):

    bld.env.append_unique(
        'DEFINES_STEINWURF_VERSION',
        'STEINWURF_KODO_RLNC_VERSION="{}"'.format(VERSION))


    bld.program(features='cxx',
                source='./src/sw9-source/encoder/full_vector_encoder.cpp',
                target='full_vector_encoder_benchmark',
                use=['kodo_rlnc_includes'])

    bld.program(features='cxx',
                source='./src/sw9-source/encoder/on_the_fly_encoder.cpp',
                target='on_the_fly_encoder_benchmark',
                use=['kodo_rlnc_includes'])

    bld.program(features='cxx',
                source='./src/sw9-source/encoder/actual_on_the_fly_encoder.cpp',
                target='actual_on_the_fly_encoder_benchmark',
                use=['kodo_rlnc_includes'])

    bld.program(features='cxx',
                source='./src/sw9-source/encoder/perpetual_encoder.cpp',
                target='perpetual_encoder_benchmark',
                use=['kodo_rlnc_includes'])

    bld.program(features='cxx',
                source='./src/sw9-source/encoder/shallow_full_vector_encoder.cpp',
                target='shallow_full_vector_encoder_benchmark',
                use=['kodo_rlnc_includes'])

    bld.program(features='cxx',
                source='./src/sw9-source/encoder/shallow_perpetual_encoder.cpp',
                target='shallow_perpetual_encoder_benchmark',
                use=['kodo_rlnc_includes'])


    # Export kodo-rlnc includes
    # bld(name='rlnc-benchmark',
    #     includes='./src',
    #     export_includes='./src',
    #     use=['kodo_rlnc_includes'])

    # if bld.is_toplevel():

    #     # Only build tests when executed from the top-level wscript,
    #     # i.e. not when included as a dependency
    #     bld.recurse('test')

    #     bld.recurse('examples/block_encode_decode')
    #     bld.recurse('examples/block_encode_decode_with_coefficients')
    #     bld.recurse('examples/customize_partitioning_scheme')
    #     bld.recurse('examples/decode_simple')
    #     bld.recurse('examples/define_custom_generator')
    #     bld.recurse('examples/encode_decode_file')
    #     bld.recurse('examples/encode_decode_separate')
    #     bld.recurse('examples/encode_decode_simple')
    #     bld.recurse('examples/encode_decode_storage')
    #     bld.recurse('examples/encode_decode_seed')
    #     bld.recurse('examples/minimal_overhead')
    #     bld.recurse('examples/encode_decode_using_coefficients')
    #     bld.recurse('examples/encode_on_the_fly')
    #     bld.recurse('examples/encode_recode_decode_simple')
    #     bld.recurse('examples/is_symbol_pivot_counter')
    #     bld.recurse('examples/perpetual')
    #     bld.recurse('examples/pure_recode_payload_api')
    #     bld.recurse('examples/pure_recode_symbol_api')
    #     bld.recurse('examples/rank_callback')
    #     bld.recurse('examples/sliding_window')
    #     bld.recurse('examples/switch_systematic_on_off')
    #     bld.recurse('examples/symbol_status_updater')
    #     bld.recurse('examples/tutorial')
    #     bld.recurse('examples/udp_sender_receiver')
    #     bld.recurse('examples/use_cache_read_symbol')
    #     bld.recurse('examples/use_interfaces')
    #     bld.recurse('examples/use_runtime')
    #     bld.recurse('examples/use_trace_layers')

    #     bld.recurse('benchmark/count_operations')
    #     bld.recurse('benchmark/decoding_probability')
    #     bld.recurse('benchmark/overhead')
    #     bld.recurse('benchmark/throughput')
