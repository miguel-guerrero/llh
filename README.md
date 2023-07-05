## Introduction

`llh` - An experimental Low Level Hardware description language embedded in python.

Contains very simple primitives to allow creating hierarchies of harware for digital design.

Simulation is supported directly in python. 

Code generation produces synthesizable Verilog HDL that can be simulated and manipulated with standard tools externally.

## Prerequisites

    $ python3 -m pip install pyvcd

  Icarus Verilog is expected to be installed if using native verilog simulations.

## Quick start

    $ python3 tests/test_counter_nbits.py

You can inspect generated `dump.vcd`

Generated verilog files are located under `work/verilog`

## Native verilog simulation

To generate a 4 bit adder and simulate it using Icarus verilog

    $ cd vtests/counter
    $ ./run.sh


