import sys
import json
from instruction import Instruction

def assemble(input_file, output_file, log_file):
    instructions = []
    with open(input_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        instr: Instruction = Instruction.from_assembly(line)
        instructions.append(instr)

    with open(output_file, 'wb') as f:
        for instr in instructions:
            f.write(instr.to_bytes())

    log_data = [instr.to_dict() for instr in instructions]
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
