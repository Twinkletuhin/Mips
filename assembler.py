from pprint import pprint
import re
#control signal formal
#|RegDst|Jump |Brancheq|Branchneq|MemRead|MemtoReg|MemWrite|ALUSrc|RegWrite|ALUop|
description_dict = {
    'A': ('add',       '100000001010'),  # add: RegDst=1, Jump=0, Brancheq=0, Branchneq=0, MemRead=0, MemtoReg=0, MemWrite=0, ALUSrc=0, RegWrite=1, ALUCtrl=010
    'B': ('addi',      '000000011010'),  # addi: RegDst=0, Jump=0, ..., ALUSrc=1, RegWrite=1, ALUCtrl=010
    'C': ('sub',       '100000001011'),  # sub
    'D': ('subi',      '000000011011'),  # subi
    'E': ('and',       '100000001000'),  # and
    'F': ('andi',      '000000011000'),  # andi
    'G': ('or',        '100000001001'),  # or
    'H': ('ori',       '000000011001'),  # ori
    'I': ('sll',       '000000011101'),  # sll
    'J': ('srl',       '000000011111'),  # srl
    'K': ('nor',       '100000001100'),  # nor
    'L': ('lw',        '000011011010'),  # lw
    'M': ('sw',        '000000110010'),  # sw
    'N': ('beq',       '001000000011'),  # beq
    'O': ('bneq',      '000100000011'),  # bneq
    'P': ('j',         '010000000000'),  # j
}
register_map={
    '$zero':"0000",
    '$t0':"0001",
    '$t1':"0010",
    '$t2':"0011",
    '$t3':"0100",
    '$t4':"0101",
    '$sp':"0110",
}
sequence='LODNPBMGAEHKFCIJ'
symbol_table={}
instructions={}
opcode_map={}

R_TYPE=['add','sub','and','or','nor']
S_TYPE=['sll','srl']
I_TYPE=['addi','subi','ori','andi']
B_TYPE=['beq','bneq']
M_TYPE=['lw','sw']
J_TYPE=['j']

for i in range(16):
    instructions[sequence[i]]=description_dict[sequence[i]]

for i,(opc,_) in enumerate(instructions.values()):
    opcode_map[opc]=str(bin(i)[2:]).zfill(4)   
# for i in instructions:
#     print(f"{i}: {instructions[i][0]} - {instructions[i][1]}")

def control_signal(filename,seeTerminal=False):
    with open(filename,'w') as f:
        f.write('v2.0 raw\n')
        for id,(inistr, signal) in instructions.items():
            hex_signal = hex(int(signal, 2))[2:].zfill(3)
            if seeTerminal:
                print(f"{id} -{inistr}: {signal}-> {hex_signal}")
            f.write(hex_signal + '\n')


# a=hex(int('100000001010', 2))[2:]
# print(a,a.upper().zfill(3))

def clean_line(line):
    line=line.split('#')[0]
    return line.strip()

def parse_label(line,pc,symbol_table,makeTable=True):
    if ':' in line:
        label,rest=line.split(':',1)
        if makeTable:
            symbol_table[label.strip()]=pc
        
        return rest.strip()
    return line

def tokenize_instruction(line):
    tokens=re.split(r'[,\s]+',line)
    return [t for t in tokens if t]   

def parse_memory_operand(op) :
    match=re.match(r'(-?\d+)\((\$[a-z0-9]+)\)',op)
    
    if not match:
        raise ValueError("Invalid memory operand")
    offset=int(match.group(1))
    base=match.group(2)

    return offset,base
def get_register(reg):
    if reg not in register_map:
        raise ValueError(f"Unknown register {reg}")
    
    return register_map[reg]

def parse_instruction(line):
    tokens=tokenize_instruction(line)
    
    return {
        "opcode":tokens[0],
        "operands":tokens[1:]
    }



def build_symbol_table(file,symbol_table):
    pc=0
    for line in file:
        line=clean_line(line)
        if not line:
           continue
        line=parse_label(line,pc,symbol_table)#build table
        if not line:
            continue
        inst=parse_instruction(line=line)
        inst = parse_instruction(line)
        opcode = inst["opcode"]

        if opcode in ['push', 'pop']:
            pc += 2      # pseudo instruction expands to 2 instructions
        else:
            pc += 1
         
        
def encode_instruction(srcfile,outfile,symbol_table):
        outfile.write("v2.0 raw\n")
        pc=0
    
        for line in srcfile:
            # print('Before clean', line)
            line=clean_line(line)
            # print('After clean', line)
            # continue
            if not line:
                continue
            line=parse_label(line,pc,symbol_table,makeTable=False)#build table
            if not line:
                    continue    
        
            result=parse_instruction(line=line)
            out=''
            if not result:
                continue
            opcode, instruction = result["opcode"], result["operands"]
            
                
            if opcode in R_TYPE:
                out=opcode_map[opcode]+get_register(instruction[1])+get_register(instruction[2])+get_register(instruction[0])
            
            elif opcode in S_TYPE:
                # print(opcode,instruction,cnvrt_bin(instruction[2],4,False))
                out=opcode_map[opcode]+get_register(instruction[1])+get_register(instruction[0])+cnvrt_bin(instruction[2],4,False) # sh_amnt
                
                
            elif opcode  in I_TYPE:
                out=opcode_map[opcode]+get_register(instruction[1])+get_register(instruction[0])+cnvrt_bin(instruction[2]) #immediate
          
            elif opcode in M_TYPE:
                offset,base=parse_memory_operand(instruction[1])
                out=opcode_map[opcode]+get_register(base)+get_register(instruction[0])+cnvrt_bin(offset)
            elif opcode in B_TYPE:
                offset=symbol_table[instruction[2].strip()]-(pc+1)
                bin_offset=cnvrt_bin(offset,4,True)
                print(opcode,instruction,'offset:',offset,'bin_offset:',bin_offset,symbol_table[instruction[2].strip()],'pc=',pc)
                out=opcode_map[opcode]+get_register(instruction[0])+get_register(instruction[1])+cnvrt_bin(offset,4,True) # branch offset
                print(len(out),hex(int(out, 2))[2:].zfill(4))
            elif opcode in J_TYPE: #direct jump to 8 bit address
               out=opcode_map[opcode]+cnvrt_bin(symbol_table[instruction[0].strip()],8)+"0000"
            #    print(out,opcode,instruction[0])
            elif opcode == 'push':
                reg = instruction[0]

                # addi $sp,$sp,-1
                out1 = opcode_map['addi'] + get_register('$sp') + get_register('$sp') + cnvrt_bin(-1)

                   # sw reg,0($sp)
                out2 = opcode_map['sw'] + get_register('$sp') + get_register(reg) + cnvrt_bin(0)

                outfile.write(hex(int(out1,2))[2:].zfill(4) + '\n')
                outfile.write(hex(int(out2,2))[2:].zfill(4) + '\n')

                pc += 2
                continue
            elif opcode=='pop':
                reg=instruction[0]
                
                #lw reg,0($sp)
                out1=opcode_map['lw']+get_register('$sp')+get_register(reg)+cnvrt_bin(0)
                
                #addi $sp,$sp,1
                out2=opcode_map['addi'] + get_register('$sp') + get_register('$sp') + cnvrt_bin(1)
                outfile.write(hex(int(out1,2))[2:].zfill(4) + '\n')
                outfile.write(hex(int(out2,2))[2:].zfill(4) + '\n')
                pc+=2
                continue
                
            pc+=1
            if out:
                hex_instr= hex(int(out, 2))[2:].zfill(4)
                outfile.write(hex_instr+'\n')
            
   
        

def cnvrt_bin(value, bits=4,signed=True):
    value = int(value)

    # signed range check
    if signed and  (value < -(1 << (bits-1)) or value > (1 << (bits-1)) - 1):
        raise ValueError(f"{value} out of {bits}-bit signed range")

    # two's complement conversion
    value = value & ((1 << bits) - 1)

    return format(value, f'0{bits}b')


        
# def process_line()
def mips_to_machine(sourceFile,outFile):
    with open(sourceFile,'r') as srcfile,open(outFile,'w')as outfile:
        # outfile.write("v2.0 raw\n")
         build_symbol_table(srcfile,symbol_table)
         print("Symbol Table:", symbol_table)
         srcfile.seek(0)
         encode_instruction(srcfile,outfile,symbol_table)      
            
                    
        
if __name__ == "__main__":
    control_signal('control_signal.hex', seeTerminal=False)
    mips_to_machine(sourceFile="source.asm",outFile="instruction.hex")
    
    # print(instructions)
    # print(opcode_map)
