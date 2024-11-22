class VM:
    def __init__(self):
        self.memory = [0] * 65536
        self.instructions = []

    def load_program(self, binary_file):
        with open(binary_file, 'rb') as f:
            data = f.read()
        for i in range(0, len(data), 9):
            instr_data = int.from_bytes(data[i:i+9], 'little')
            self.instructions.append(instr_data)

    def run(self):
        for instr_data in self.instructions:
            self.execute(instr_data)

    def execute(self, instr_data):
        code = (instr_data >> 0) & 0x7F
        if code == 59:  # LOAD_CONST
            B = (instr_data >> 7) & 0xFFFFF  # Биты 7-26
            C = (instr_data >> 27) & 0x1FFFF  # Биты 27-43
            self.memory[B] = C
        elif code == 109:  # READ_MEM
            B = (instr_data >> 7) & 0xFFFFF  # Биты 7-26
            C = (instr_data >> 27) & 0xFFFFF  # Биты 27-46
            self.memory[B] = self.memory[C]
        elif code == 69:  # WRITE_MEM
            B = (instr_data >> 7) & 0xFFFFF  # Биты 7-26
            C = (instr_data >> 27) & 0x7FFF  # Биты 27-41
            D = (instr_data >> 42) & 0xFFFFF  # Биты 42-61
            address = self.memory[B] + C
            self.memory[address] = self.memory[D]
        elif code == 82:  # OR
            B = (instr_data >> 7) & 0xFFFFF  # Биты 7-26
            C = (instr_data >> 27) & 0xFFFFF  # Биты 27-46
            D = (instr_data >> 47) & 0xFFFFF  # Биты 47-66
            operand1 = self.memory[D]
            operand2 = self.memory[C]
            self.memory[B] = operand1 | operand2  # Исправлено: сохранение по адресу B

    def get_memory_range(self, start, end):
        return self.memory[start:end+1]
