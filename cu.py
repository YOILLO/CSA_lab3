import proc


class ControlUnit:
    def __init__(self):
        self.proc: proc.Processor = proc.Processor()
        self.ticks: int = 0
        self.trace: str = "r1, " \
                          "r2, " \
                          "r3, " \
                          "r3, " \
                          "cr, " \
                          "ip, " \
                          "bf, " \
                          "sp, " \
                          "sr\n"

    def chose_operands(self):
        if (self.proc.cr >> 8 & 0xFF) == 1:
            self.proc.left_op = self.proc.r1
        elif (self.proc.cr >> 8 & 0xFF) == 2:
            self.proc.left_op = self.proc.r2
        elif (self.proc.cr >> 8 & 0xFF) == 3:
            self.proc.left_op = self.proc.r3
        elif (self.proc.cr >> 8 & 0xFF) == 4:
            self.proc.left_op = self.proc.r4

        if self.proc.cr & 0xFF == 1:
            self.proc.right_op = self.proc.r1
        elif self.proc.cr & 0xFF == 2:
            self.proc.right_op = self.proc.r2
        elif self.proc.cr & 0xFF == 3:
            self.proc.right_op = self.proc.r3
        elif self.proc.cr & 0xFF == 4:
            self.proc.right_op = self.proc.r4
        elif self.proc.cr & 0xFF == 5:
            self.proc.ar = self.proc.ip
            self.proc.ip += 1
            self.proc.get_from_commands_mem()
            self.proc.right_op = self.proc.dr
        elif self.proc.cr & 0xFF == 6:
            self.proc.ar = self.proc.ip
            self.proc.ip += 1
            self.proc.get_from_commands_mem()
            self.proc.ar = self.proc.dr
            self.proc.get_from_data_mem()
            self.proc.right_op = self.proc.dr

    def chose_one_operand_registers(self):
        if self.proc.cr & 0xFF == 1:
            self.proc.right_op = self.proc.r1
        elif self.proc.cr & 0xFF == 2:
            self.proc.right_op = self.proc.r2
        elif self.proc.cr & 0xFF == 3:
            self.proc.right_op = self.proc.r3
        elif self.proc.cr & 0xFF == 4:
            self.proc.right_op = self.proc.r4

    def chose_one_operand_mem(self):
        if self.proc.cr & 0xFF == 5:
            self.proc.ar = self.proc.ip
            self.proc.ip += 1
            self.proc.get_from_commands_mem()
            self.proc.right_op = self.proc.dr
        elif self.proc.cr & 0xFF == 6:
            self.proc.ar = self.proc.ip
            self.proc.ip += 1
            self.proc.get_from_commands_mem()
            self.proc.ar = self.proc.dr
            self.proc.get_from_data_mem()
            self.proc.right_op = self.proc.dr

    def write_result(self):
        if (self.proc.cr >> 8 & 0xFF) == 1:
            self.proc.r1 = self.proc.result
        elif (self.proc.cr >> 8 & 0xFF) == 2:
            self.proc.r2 = self.proc.result
        elif (self.proc.cr >> 8 & 0xFF) == 3:
            self.proc.r3 = self.proc.result
        elif (self.proc.cr >> 8 & 0xFF) == 4:
            self.proc.r4 = self.proc.result

    def write_mem(self):
        self.proc.ar = self.proc.ip
        self.proc.ip += 1
        self.proc.get_from_commands_mem()
        self.proc.ar = self.proc.dr
        self.proc.dr = self.proc.result
        self.proc.write_to_data_mem()

    def write_stack(self):
        self.proc.sp -= 1
        self.proc.ar = self.proc.sp
        self.proc.dr = self.proc.result
        self.proc.write_to_data_mem()

    def read_stack(self):
        self.proc.ar = self.proc.sp
        self.proc.get_from_data_mem()
        self.proc.right_op = self.proc.dr
        self.proc.sp += 1

    def jmp(self):
        self.proc.ar = self.proc.ip
        self.proc.get_from_commands_mem()
        self.proc.ip = self.proc.dr

    def work(self):
        while True:
            self.ticks += 1
            self.trace += self.proc.trace() + "\n"

            self.proc.left_op = self.proc.ip
            self.proc.ar = self.proc.ip
            self.proc.inc()
            self.proc.sum(False)
            self.proc.ip = self.proc.result
            self.proc.end_tick()

            self.proc.get_from_commands_mem()
            self.proc.left_op = self.proc.dr
            self.proc.sum(False)
            self.proc.cr = self.proc.result
            self.proc.end_tick()

            if self.proc.cr == 0:
                # COMMAND HALT
                return self.trace, self.ticks
            elif self.proc.cr >> 16 == 1:
                # COMMAND ADD
                self.chose_operands()
                self.proc.sum(True)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 2:
                # COMMAND SUB
                self.chose_operands()
                self.proc.inc()
                self.proc.reverse_right()
                self.proc.sum(True)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 3:
                # COMMAND MUL
                self.chose_operands()
                self.proc.mul(True)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 4:
                # COMMAND DIV
                self.chose_operands()
                self.proc.div(True)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 5:
                # COMMAND MOD
                self.chose_operands()
                self.proc.mod(True)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 6:
                # COMMAND MOV
                self.chose_one_operand_registers()
                self.proc.sum(False)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 7:
                # COMMAND SV
                self.chose_one_operand_registers()
                self.proc.sum(False)
                self.write_mem()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 8:
                # COMMAND LD
                self.chose_one_operand_mem()
                self.proc.sum(False)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 9:
                # COMMAND TEST
                self.chose_one_operand_registers()
                self.proc.sum(True)
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 10:
                # COMMAND JMP
                self.jmp()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 11:
                # COMMAND JZ
                if self.proc.sr[proc.SR_Z]:
                    self.jmp()
                else:
                    self.proc.ip += 1
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 12:
                # COMMAND JN
                if self.proc.sr[proc.SR_N]:
                    self.jmp()
                else:
                    self.proc.ip += 1
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 13:
                # COMMAND JC
                if self.proc.sr[proc.SR_C]:
                    self.jmp()
                else:
                    self.proc.ip += 1
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 14:
                # COMMAND JV
                if self.proc.sr[proc.SR_V]:
                    self.jmp()
                else:
                    self.proc.ip += 1
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 15:
                # COMMAND CLZ
                self.proc.sr[proc.SR_Z] = 0
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 16:
                # COMMAND CLN
                self.proc.sr[proc.SR_N] = 0
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 17:
                # COMMAND CLV
                self.proc.sr[proc.SR_V] = 0
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 18:
                # COMMAND CLC
                self.proc.sr[proc.SR_C] = 0
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 20:
                # COMMAND PUSH
                self.chose_one_operand_registers()
                self.proc.sum(False)
                self.write_stack()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 21:
                # COMMAND POP
                self.read_stack()
                self.proc.sum(False)
                self.write_result()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 22:
                # COMMAND CALL
                self.proc.right_op = self.proc.ip
                self.proc.sum(False)
                self.write_stack()
                self.jmp()
                self.proc.end_tick()
            elif self.proc.cr >> 16 == 23:
                # COMMAND RET
                self.read_stack()
                self.proc.sum(False)
                self.proc.ip = self.proc.result
                self.proc.end_tick()
