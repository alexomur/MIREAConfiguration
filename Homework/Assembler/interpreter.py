import sys
import json
from vm import VM

def interpret(binary_file, result_file, memory_range):
    vm = VM()
    vm.load_program(binary_file)
    vm.run()
    start, end = map(int, memory_range.split('-'))
    memory_data = vm.get_memory_range(start, end)
    with open(result_file, 'w') as f:
        json.dump(memory_data, f, indent=4)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python interpreter.py <binary_file> <result_file> <memory_range>")
        sys.exit(1)
    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    memory_range = sys.argv[3]
    interpret(binary_file, result_file, memory_range)
