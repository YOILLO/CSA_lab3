from constans import *


class Processor:
    def __init__(self):
        self.r1: int = 0
        self.r2: int = 0
        self.r3: int = 0
        self.r4: int = 0

        self.cr: int = 0
        self.ip: int = 0
        self.bf: int = 0
        self.sp: int = SP_BASE
        self.sr: list = [0 for i in range(32)]

        self.dr: int = 0
        self.ar: int = 0

        self.left_op: int = 0
        self.right_op: int = 0

        self.result: int = 0

        self.data_mem: list = [0 for i in range(MEMORY_SIZE)]
        self.commands_mem: list = [0 for i in range(MEMORY_SIZE)]

        self.input_queue: list = []
        self.output_queue: list = []

    def reverse_left(self):
        self.left_op = ~self.left_op

    def reverse_right(self):
        self.right_op = ~self.right_op

    def inc(self):
        self.left_op += 1

    def set_flags(self):
        if self.result & 0x100000000:
            self.sr[SR_C] = 1
        if (not self.left_op & 0x80000000 and not self.right_op & 0x80000000 and self.result & 0x80000000) \
                or (self.left_op & 0x80000000 and self.right_op & 0x80000000 and not self.result & 0x80000000):
            self.sr[SR_V] = 1
        if self.result == 0:
            self.sr[SR_Z] = 1
        if self.result & 0x80000000:
            self.sr[SR_N] = 1

    def sum(self, set_flags: bool):
        self.left_op &= 0xFFFFFFFF
        self.right_op &= 0xFFFFFFFF
        self.result = self.left_op + self.right_op
        self.result &= 0xFFFFFFFF
        if set_flags:
            self.set_flags()

    def mul(self, set_flags: bool):
        self.left_op &= 0xFFFFFFFF
        self.right_op &= 0xFFFFFFFF
        self.result = self.left_op * self.right_op
        self.result &= 0xFFFFFFFF
        if set_flags:
            self.set_flags()

    def div(self, set_flags: bool):
        self.left_op &= 0xFFFFFFFF
        self.right_op &= 0xFFFFFFFF
        self.result = self.left_op // self.right_op
        self.result &= 0xFFFFFFFF
        if set_flags:
            self.set_flags()

    def mod(self, set_flags: bool):
        self.left_op &= 0xFFFFFFFF
        self.right_op &= 0xFFFFFFFF
        self.result = self.left_op % self.right_op
        self.result &= 0xFFFFFFFF
        if set_flags:
            self.set_flags()

    def end_tick(self):
        self.left_op = 0
        self.right_op = 0

    def get_from_data_mem(self):
        if self.ar == INPUT_ADDRESS:
            self.data_mem[self.ar] = self.input_queue.pop()
        self.dr = self.data_mem[self.ar]

    def get_from_commands_mem(self):
        self.dr = self.commands_mem[self.ar]

    def write_to_data_mem(self):
        self.data_mem[self.ar] = self.dr
        if self.ar == OUTPUT_ADDRESS:
            self.output_queue.append(self.data_mem[self.ar])

    def write_to_commands_mem(self):
        self.commands_mem[self.ar] = self.dr

    def trace(self):
        return f"{self.r1}, " \
               f"{self.r2}, " \
               f"{self.r3}, " \
               f"{self.r3}, " \
               f"{self.cr}, " \
               f"{self.ip}, " \
               f"{self.bf}, " \
               f"{self.sp}, " \
               f"0b{''.join([str(n) for n in self.sr])}"
