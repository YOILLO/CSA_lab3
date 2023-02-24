#!/bin/python

from constans import *

def is_integer(n):
    try:
        int(n, 0)
        return True
    except ValueError:
        return False


commands = [['halt', 0, 0],
            ['add', 2, 2],
            ['sub', 2, 2],
            ['mul', 2, 2],
            ['div', 2, 2],
            ['mod', 2, 2],
            ['mov', 2, 2],
            ['sv', 2, 1],
            ['ld', 2, 1],
            ['test', 1, 0],
            ['jmp', 1, 1],
            ['jz', 1, 1],
            ['jn', 1, 1],
            ['jc', 1, 1],
            ['jv', 1, 1],
            ['clz', 0, 0],
            ['cln', 0, 0],
            ['clv', 0, 0],
            ['clc', 0, 0],
            ['push', 1, 0],
            ['pop', 1, 0],
            ['call', 1, 1],
            ['ret', 0, 0]]

def compile_error(line_num, message, code):
    print(f'Строка: {line_num}: {message}')
    exit(code)

def from_str_to_reg_or_op_arg(str: str, num):
    if str == 'r1':
        return 0, 1
    if str == 'r2':
        return 0, 2
    if str == 'r3':
        return 0, 3
    if str == 'r4':
        return 0, 4

    if str[0] == 'o':
        if not is_integer(str[1:]):
            compile_error(num, 'Ошибка, операнд не число', 5)
        return 1, int(str[1:], 0)

    if not is_integer(str):
        compile_error(num, 'Адресс не число', 6)

    return 2, int(str, 0)

def from_str_to_op_arg(str: str, num):
    if str[0] == 'o':
        if not is_integer(str[1:]):
            compile_error(num, 'Ошибка, операнд не число', 5)
        return 1, int(str[1:], 0)

    if not is_integer(str):
        compile_error(num, 'Адресс не число', 6)

    return 2, int(str, 0)

def from_str_to_reg_arg(str: str, num):
    if str == 'r1':
        return 0, 1
    if str == 'r2':
        return 0, 2
    if str == 'r3':
        return 0, 3
    if str == 'r4':
        return 0, 4

    compile_error(num, 'Указан не регистр', 7)

def from_str_to_addr_arg(str:str, labels, num):
    if is_integer(str):
        return int(str, 0)

    for lab in labels:
        if lab[0] == str:
            return lab[1]

    compile_error(num, 'Ошибочный адрес или метка', 8)



def compile(input_file: str, output_file: str):
    lines = []

    with open(input_file, 'r') as inp_f:
        for line in inp_f.readlines():
            lines.append(line)

    line_without_comments = []
    for line in lines:
        line_without_comments.append(line.split(';')[0])

    counted_lines = []
    for n in range(len(line_without_comments)):
        counted_lines.append([n + 1, line_without_comments[n].strip()])

    labels = []
    coms = []
    current_addr = 0
    for num, str in counted_lines:
        splited_str = str.split()
        for n in range(len(splited_str)):
            if splited_str[n][-1] == ':':
                if len(splited_str[n]) == 1:
                    if n == 0:
                        compile_error(num, 'Пропущено название метки', 1)

                    labels.append([splited_str[n - 1], current_addr])
                else:
                    labels.append([splited_str[n][0:-1], current_addr])

            for com in commands:
                if splited_str[n].lower() == com[0]:
                    if len(splited_str) <= n + com[1]:
                        compile_error(num, 'Недостаточно аргументов', 2)

                    if com[1] == 0:
                        coms.append([num, current_addr, com[0]])
                        current_addr += 1
                    elif com[1] == 1:
                        coms.append([num, current_addr, com[0], splited_str[n + 1]])
                        current_addr += 1 + com[2]
                    elif com[1] == 2:
                        coms.append([num, current_addr, com[0], splited_str[n + 1], splited_str[n + 2]])
                        current_addr += 1
                        current_addr += 1 if from_str_to_reg_or_op_arg(splited_str[n + 1], num)[0] != 0 else 0
                        current_addr += 1 if from_str_to_reg_or_op_arg(splited_str[n + 2], num)[0] != 0 else 0
                    break

            if splited_str[n].lower() == 'org':
                if len(splited_str) <= n + 1:
                    compile_error(num, 'ОRG неуказан адресс', 3)

                if not is_integer(splited_str[n + 1]):
                    compile_error(num, 'адресс не номер', 4)

                current_addr = int(splited_str[n + 1], 0)

    mem = [0 for i in range(MEMORY_SIZE)]

    for com in coms:
        if com[2] == 'halt':
            mem[com[1]] = 0
        elif com[2] == 'add':
            mem[com[1]] = 1 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_reg_or_op_arg(com[4], com[0])
            if code == 0:
                mem[com[1]] |= data
            elif code == 1:
                mem[com[1]] |= 5
                mem[com[1] + 1] = data
            elif code == 2:
                mem[com[1]] |= 6
                mem[com[1] + 1] = data

        elif com[2] == 'sub':
            mem[com[1]] = 2 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_reg_or_op_arg(com[4], com[0])
            if code == 0:
                mem[com[1]] |= data
            elif code == 1:
                mem[com[1]] |= 5
                mem[com[1] + 1] = data
            elif code == 2:
                mem[com[1]] |= 6
                mem[com[1] + 1] = data
        elif com[2] == 'mul':
            mem[com[1]] = 3 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_reg_or_op_arg(com[4], com[0])
            if code == 0:
                mem[com[1]] |= data
            elif code == 1:
                mem[com[1]] |= 5
                mem[com[1] + 1] = data
            elif code == 2:
                mem[com[1]] |= 6
                mem[com[1] + 1] = data
        elif com[2] == 'div':
            mem[com[1]] = 4 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_reg_or_op_arg(com[4], com[0])
            if code == 0:
                mem[com[1]] |= data
            elif code == 1:
                mem[com[1]] |= 5
                mem[com[1] + 1] = data
            elif code == 2:
                mem[com[1]] |= 6
                mem[com[1] + 1] = data
        elif com[2] == 'mod':
            mem[com[1]] = 5 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_reg_or_op_arg(com[4], com[0])
            if code == 0:
                mem[com[1]] |= data
            elif code == 1:
                mem[com[1]] |= 5
                mem[com[1] + 1] = data
            elif code == 2:
                mem[com[1]] |= 6
                mem[com[1] + 1] = data
        elif com[2] == 'mov':
            mem[com[1]] = 6 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_reg_arg(com[4], com[0])
            mem[com[1]] |= data
        elif com[2] == 'sv':
            mem[com[1]] = 7 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data
            data = from_str_to_addr_arg(com[4], [], com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'ld':
            mem[com[1]] = 8 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
            code, data = from_str_to_op_arg(com[4], com[0])
            if code == 1:
                mem[com[1]] |= 5
                mem[com[1] + 1] = data
            if code == 2:
                mem[com[1]] |= 6
                mem[com[1] + 1] = data
        elif com[2] == 'test':
            mem[com[1]] = 9 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data
        elif com[2] == 'jmp':
            mem[com[1]] = 10 << 16
            data = from_str_to_addr_arg(com[3], labels, com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'jz':
            mem[com[1]] = 11 << 16
            data = from_str_to_addr_arg(com[3], labels, com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'jn':
            mem[com[1]] = 12 << 16
            data = from_str_to_addr_arg(com[3], labels, com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'jc':
            mem[com[1]] = 13 << 16
            data = from_str_to_addr_arg(com[3], labels, com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'jv':
            mem[com[1]] = 14 << 16
            data = from_str_to_addr_arg(com[3], labels, com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'clz':
            mem[com[1]] = 15 << 16
        elif com[2] == 'cln':
            mem[com[1]] = 16 << 16
        elif com[2] == 'clv':
            mem[com[1]] = 17 << 16
        elif com[2] == 'clc':
            mem[com[1]] = 18 << 16
        elif com[2] == 'push':
            mem[com[1]] = 20 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data
        elif com[2] == 'pop':
            mem[com[1]] = 21 << 16
            code, data = from_str_to_reg_arg(com[3], com[0])
            mem[com[1]] |= data << 8
        elif com[2] == 'call':
            mem[com[1]] = 22 << 16
            data = from_str_to_addr_arg(com[3], labels, com[0])
            mem[com[1] + 1] = data
        elif com[2] == 'ret':
            mem[com[1]] = 23 << 16

    with open(output_file, 'wb') as f:
        for i in mem:
            byt = [0, 0, 0, 0]
            byt[0] = (i >> 24) & 0xFF
            byt[1] = (i >> 16) & 0xFF
            byt[2] = (i >> 8) & 0xFF
            byt[3] = i & 0xFF
            f.write(bytes(byt))


if __name__ == '__main__':
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument("source", help="source asm file")
    argParser.add_argument("compiled", help="result file")

    args = argParser.parse_args()

    compile(args.source, args.compiled)
