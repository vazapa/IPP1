import sys
import argparse
import re
# TODOTODOTODOTODOTODO
# comments_test hlavicka a az potom komentar
# hex_int_test checknout spravny hex format


# <var>  GF@swag -> type = var (variable regex)
# <symb> int@1 -> typ = int/boo/string (constant regex)
#        GF@swag -> typ = var (variable regex)
# <label> jakykolivstring -> type = var (string regex)
# <type> int string bool -> type = type ()

parser = argparse.ArgumentParser(description='Process input or display help')
parser.add_argument('input', nargs='?', help='Input from stdin or --help to display help')    
args = parser.parse_args()
variable_regex = r'^(LF|TF|GF)@[a-zA-Z_\-$&%*!?]+[0-9]*$'
label_regex = r'^[a-zA-Z0-9_\-$&%*!?]+[0-9]*$'
constant_regex = r'^(bool|nil|int|string)@(.+)$'
string_regex = r'^.*$'
type_regex = r'(int|bool|string)'

if args.input == '--help':
       parser.print_help()

header = False
order = 0

### FUNCTION DEFINITIONS ###
def print_label(opcode : str):
    global order
    order += 1
    print(f'\t<instruction order="{order}" opcode="{opcode}">')

def print_arg(arg, args_num: int):

    # match idk :
    #     case "label":
    #         typ = "label"
    #         value = arg
    #     case "var":
    #         typ = "var"
    #         value = arg 
    #     case "type":
    #         typ, value = arg[1].split('@')
    
    #temporary
    index = 1

    if len(arg)-1 != args_num:
        print("Wrong number of arguments LMAO LMAO LMAO LMAOLMAO LMAOLMAO LMAO")
        sys.exit(23)
    else:
        for i in arg[1:]:
            # print(f'\t\t<arg{i+1} type="{typ}">{value}</arg{i+1}>')
            index += 1
            if re.match(variable_regex, i) is not None:
                typ = "var"
                value = i
            elif re.match(constant_regex, i) is not None:
                
                
                typ, value = i.split('@',1)
                
                
            elif re.match(label_regex, i) is not None:
                typ = "label"
                value = i
            elif re.match(type_regex, i) is not None:
                typ = "type"
                value = i

            
            print(f'\t\t<arg{index} type="{typ}">{value}</arg{index}>')
            
        
        
        
        print("\t</instruction>")

def var_check(arg):
    

    if re.match(variable_regex, arg) is None:
        print(f'ERR: {arg} is not a variable')
        sys.exit(23)  
def label_check(arg):
    
    
    if re.match(label_regex, arg) is None:
        print(f'ERR: {arg} is not a label')
        sys.exit(23)  
def constant_check(arg):
    check = re.match(constant_regex, arg)
    if check is None:
        print(f'ERR: {arg} is not a constant')
        sys.exit(23)  


    typ = check.group(1)
    constant = check.group(2)

    match typ:
        case "string":
            if re.match(string_regex, constant) is None:
                print(f'ERR: {constant} is not a string')
                sys.exit(23)  
        case "int":
            int_regex = r'^((-?0x[0-9a-fA-F]+)|([-0-9]+))$'
            
            if re.match(int_regex, constant) is None:
                print(f'ERR: {constant} is not a int or hex')
                sys.exit(23)  
        case "bool":
            bool_regex = r'^(true|false)$'
            if re.match(bool_regex, constant) is None:
                print(f'ERR: {constant} is not a bool')
                sys.exit(23)  
        case "nill":
            if constant != "nill":
                print(f'ERR: {constant} is not a nill')
                sys.exit(23)  
def type_check(arg) :
    
    if re.match(type_regex, arg) is None:
                print(f'ERR: {arg} is not a type')
                sys.exit(23)  


def constantORvar(arg):
    decider = r'^(GF|LF|TF)'
    if re.match(decider, arg) is None:
        constant_check(arg)
    else :
        var_check(arg)

def header_check():
    first_line = re.sub(r'#.*', '', sys.stdin.readline())
    if first_line.strip() != ".IPPcode24":
        print("Missing header")
        sys.exit(21)
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<program language="IPPcode24">')
### FUNCTION DEFINITIONS ###

header_check()

for line in sys.stdin:
    
    if (line.startswith('#')) or (not line.strip()) :
        continue
    
    line = re.sub(r'#.*', '', line)
    
    word = line.split()

    
    match word[0]:
        # 0
        case "CREATEFRAME" | "PUSHFRAME"| "POPFRAME"| "RETURN"| "BREAK":
            print("OK") 
            if len(word) != 1:
                print("Too much arguments")
                sys.exit(23)
        # 1
        # <var>
        case "DEFVAR":
            print_label(word[0])            
            print_arg(word,1)
            var_check(word[1])
        # <label>
        case "CALL"| "LABEL"| "JUMP":
            print_label(word[0])
            label_check(word[1])
            print_arg(word,1)
            
        # <symb>
        case "PUSHS"| "POPS"| "WRITE"| "EXIT"| "DPRINT":
        # print_label(word)
            print_label(word[0])
            print_arg(word,1)
            constantORvar(word[1])
        # 2
        # <var> <type>
        case "READ":
            print_label(word[0]) 
            print_arg(word,2)
            var_check(word[1])
            type_check(word[2])
        # <var> <symb>
        case "INT2CHAR" | "MOVE" | "STRLEN" | "TYPE" :
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
print("</program>")