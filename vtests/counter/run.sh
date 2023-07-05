#!/bin/bash

pushd ../..
python3 tests/test_counter_nbits.py
popd

rm a.out > /dev/null 2>&1

if [ x$(which iverilog) == x ]; then
    echo "Please install Icarus verilog (iverilog) or set it in the path"
    exit 1
fi

PREFIX=../.. iverilog \
    -y ../../prims/verilog \
    -f ../../work/verilog/filelist.f \
    tb.v  &&  vvp a.out

rm -f a.out
