class Instruction:
    def __init__(self, code, fields):
        self.code = code
        self.fields = fields

    def to_bytes(self):
        bits = 0
        bits |= (self.code & 0x7F) << 0  # Биты 0-6
        if 'B' in self.fields:
            bits |= (self.fields['B'] & 0xFFFFF) << 7  # Биты 7-26 (20 бит)
        if 'C' in self.fields:
            if self.code == 59:  # LOAD_CONST
                bits |= (self.fields['C'] & 0x1FFFF) << 27  # Биты 27-43 (17 бит)
            elif self.code == 109 or self.code == 82:  # READ_MEM или OR
                bits |= (self.fields['C'] & 0xFFFFF) << 27  # Биты 27-46 (20 бит)
            elif self.code == 69:  # WRITE_MEM
                bits |= (self.fields['C'] & 0x7FFF) << 27  # Биты 27-41 (15 бит)
        if 'D' in self.fields:
            if self.code == 69:  # WRITE_MEM
                bits |= (self.fields['D'] & 0xFFFFF) << 42  # Биты 42-61 (20 бит)
            elif self.code == 82:  # OR
                bits |= (self.fields['D'] & 0xFFFFF) << 47  # Биты 47-66 (20 бит)
        return bits.to_bytes(9, byteorder='little')

    @classmethod
    def from_assembly(cls, line):
        parts = line.split()
        opcode = parts[0]
        params = {}
        for part in parts[1:]:
            key, value = part.split('=')
            params[key] = int(value)
        code_map = {
            'LOAD_CONST': 59,
            'READ_MEM': 109,
            'WRITE_MEM': 69,
            'OR': 82
        }
        code = code_map.get(opcode)
        return cls(code, params)

    def to_dict(self):
        data = {'code': self.code}
        data.update(self.fields)
        return data
