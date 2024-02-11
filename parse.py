import sys
import argparse
import re


parser = argparse.ArgumentParser(description='Process input or display help')
parser.add_argument('input', nargs='?', help='Input from stdin or --help to display help')    
args = parser.parse_args()

header = False
order = 0

first_line = sys.stdin.readline().strip()
if first_line != ".IPPcode24":
    print("Missing header")
    sys.exit(21)


if args.input == '--help':
       parser.print_help()

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<program language="IPPcode24">')

def print_label(opcode : str):
    global order
    order += 1
    print(f'\t<instruction order="{order}" opcode="{opcode}">')

def print_arg(arg, args_num: int):
    if len(arg)-1 != args_num:
        print("Wrong number of arguments LMAO")
    else:
        for i in range(args_num):
            print(f'\t\t<arg{i+1} type="var">{arg[i+1]}</arg{i+1}>')
for line in sys.stdin:

    word = line.split()
    if line.startswith('#'):
        continue

    # m = re.match(r'^([^#]*)#(.*)$', line)
    # if m:  # The line contains a hash / comment
    #     print("FOUND IT FOUND IT FOUND IT FOUND IT")
    #     line = m.group(1)
    
    match word[0]:
        # 0
        case "CREATEFRAME" | "PUSHFRAME"| "POPFRAME"| "RETURN"| "BREAK":
            print("OK")
        # 1
        # <var>
        case "DEFVAR":
            print_label(word[0])            
            print_arg(word,1)
        # <label>
        case "CALL"| "LABEL"| "JUMP":
            print_label(word[0])
            print_arg(word,1)
        # <symb>
        case "PUSHS"| "POPS"| "WRITE"| "EXIT"| "DPRINT":
        # print_label(word)
            print_label(word[0])
            print_arg(word,1)
        # 2
        case "MOVE"| "INT2CHAR"| "READ"| "STRLEN"| "TYPE":
            print_label(word[0])
            print_arg(word,2)
        # 3
        # <var> <symb1> <symb2>
        case "ADD"| "SUB"| "MUL"| "IDIV"| "LT"| "GT"| "EQ"| "AND"| "OR"| "NOT"| "STRI2INT"| "CONCAT"| "GETCHAR"| "SETCHAR":
            print_label(word[0])
            print_arg(word,3)
        # <label> <symb1> <symb2>
        case "JUMPIFEQ"| "JUMPIFNEQ":
            print_label(word[0])
            print_arg(word,3)        
        case _:
            print("!Wrong keyword!")
            sys.exit(22)

