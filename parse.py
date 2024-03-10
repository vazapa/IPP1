import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Process input or display help')
parser.add_argument('input', nargs='?', help='Input from stdin or --help to display help')    
args = parser.parse_args()
variable_regex = r'^(LF|TF|GF)@[a-zA-Z_\-$&%*!?]+[0-9]*[a-zA-Z_\-$&%*!?]*$'
label_regex = r'^[a-zA-Z0-9_\-$&%*!?]+[0-9]*$'
constant_regex = r'^(bool|nil|int|string)@(.*)$'
string_regex = r'^.*$'
type_regex = r'^(int|bool|string)$'
tab = ' ' * 4

if args.input == '--help':
       parser.print_help()


order = 0

### FUNCTION DEFINITIONS ###
def args_num(acc_num,exp_num):
    if acc_num != exp_num :
        sys.exit(23)

def print_label(opcode : str):
    global order
    order += 1
    print(tab + f'<instruction order="{order}" opcode="{opcode.upper()}">')

def print_arg(arg, args_num: int, typeORint: str):
    index = 0

    if len(arg)-1 != args_num:
        print("Wrong number of arguments")
        sys.exit(23)
    else:
        for i in arg[1:]:
            
            index += 1
            if re.match(variable_regex, i) is not None:
                value = i.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                typ = "var"
            elif re.match(constant_regex, i) is not None:
                typ, value = i.split('@',1)
                value = value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elif re.match(type_regex, i) is not None and typeORint == "type":
                typ = "type"
                value = i
            elif re.match(label_regex, i) is not None and typeORint == "label":
                typ = "label"
                value = i
            else:
                print("print_arg err")
                sys.exit(23)
            
            print(tab *2 + f'<arg{index} type="{typ}">{value}</arg{index}>')
        print(tab + "</instruction>")

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
            string_regex2 = r'^(?:[^#\\]|\\[0-9]{3})*$'
            if re.match(string_regex2, constant) is None:
                print(f'ERR: {constant} is not a string')
                sys.exit(23)  
        case "int":
            int_regex = r'^(([-+]?)((0x[0-9a-fA-F]+)|(0o[0-7]+)|([0-9]+)))$'
            if re.match(int_regex, constant) is None:
                print(f'ERR: {constant} is not a int or hex')
                sys.exit(23)  
        case "bool":
            bool_regex = r'^(true|false)$'
            if re.match(bool_regex, constant) is None:
                print(f'ERR: {constant} is not a bool')
                sys.exit(23)  
        case "nil":
            if constant != "nil":
                print(f'ERR: {constant} is not a nil')
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
    for line in sys.stdin:
    
        if (line.startswith('#')) or (not line.strip()) :
            continue
    
        line = re.sub(r'#.*', '', line)
    
        word = line.split()

        match word[0]:
            case ".IPPcode24":
                break
            case _:
                print("Missing header")
                sys.exit(21)
            
    
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<program language="IPPcode24">')
### FUNCTION DEFINITIONS ###

header_check()
header = False

for line in sys.stdin:
    
    if (line.startswith('#')) or (not line.strip()) :
        continue
    
    line = re.sub(r'#.*', '', line)
    
    word = line.split()

    match word[0].upper():
        case ".IPPCODE24":
            print("More than 1 header")
            sys.exit(23)
        # 0
        case "CREATEFRAME" | "PUSHFRAME"| "POPFRAME"| "RETURN"| "BREAK":
            args_num(len(word),1)
            print_label(word[0])
            print(tab + "</instruction>")
        # 1
        # <var>
        case "DEFVAR"| "POPS":
            args_num(len(word),2)
            print_label(word[0]) 
            print_arg(word,1,"")
            var_check(word[1])
        # <label>
        case "CALL"| "LABEL"| "JUMP":
            args_num(len(word),2)
            print_label(word[0])
            label_check(word[1])
            print_arg(word,1,"label")
            
        # <symb>
        case "PUSHS"| "WRITE"| "EXIT"| "DPRINT":
        # print_label(word)
            args_num(len(word),2)
            print_label(word[0])
            print_arg(word,1,"")
            constantORvar(word[1])
        # 2
        # <var> <type>
        case "READ":
            args_num(len(word),3)
            print_label(word[0]) 
            print_arg(word,2,"type")
            var_check(word[1])
            type_check(word[2])
        # <var> <symb>
        case "INT2CHAR" | "MOVE" | "STRLEN" | "TYPE" :
            args_num(len(word),3)
            print_label(word[0])
            print_arg(word,2,"")
            var_check(word[1])
            constantORvar(word[2])
        # 3
        # <var> <symb1>
        case "NOT":
            args_num(len(word),3)
            print_label(word[0])
            print_arg(word,2,"")
            var_check(word[1])
            constantORvar(word[2])
        # <var> <symb1> <symb2>
        case "ADD"| "SUB"| "MUL"| "IDIV"| "LT"| "GT"| "EQ"| "AND"| "OR"| "NOT"| "STRI2INT"| "CONCAT"| "GETCHAR"| "SETCHAR":
            args_num(len(word),4)
            print_label(word[0])
            print_arg(word,3,"")
            var_check(word[1])
            constantORvar(word[1])
            constantORvar(word[2])
        # <label> <symb1> <symb2>
        case "JUMPIFEQ"| "JUMPIFNEQ":
            args_num(len(word),4)
            print_label(word[0])
            print_arg(word,3,"label")  
            label_check(word[1])
            constantORvar(word[2])
            constantORvar(word[3])     
        case _:
            print("!Wrong keyword!")
            sys.exit(22)
print("</program>")
