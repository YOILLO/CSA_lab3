#!/bin/python

import cu

from constans import *

def load_program(filename: str, control_unit: cu.ControlUnit):
    bytes = 0
    with open(filename, 'rb') as fl:
        bytes = fl.read()

    for i in range(MEMORY_SIZE):
        control_unit.proc.commands_mem[i] = bytes[4*i] << 24 | bytes[4*i + 1] << 16 | bytes[4*i + 2] << 8 | bytes[4*i + 3]


def add_input(inp: int, control_unit: cu.ControlUnit):
    control_unit.proc.input_queue.append(inp)


if __name__ == '__main__':
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument("code", help="binary file name")
    argParser.add_argument("result", help="result file name")
    argParser.add_argument("-i", "--input", help="input file name")

    args = argParser.parse_args()

    control_unit = cu.ControlUnit()

    load_program(args.code, control_unit)

    if args.input:
        with open(args.input, 'r') as fl:
            for line in fl.readlines():
                add_input(int(line, 0), control_unit)

    trace, ticks = control_unit.work()

    with open(args.result, 'w') as f:
        f.write(str(control_unit.proc.output_queue) + " ticks: " + str(ticks) + "\n")
        f.write(trace)

