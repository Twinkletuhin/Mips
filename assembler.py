from pprint import pprint

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
    '$zero':"000",
    '$t0':"001",
    '$t1':"010",
    '$t2':"011",
    '$t3':"100",
    '$t4':"101",
    '$sp':"110",
}
sequence='LODNPBMGAEHKFCIJ'

instructions={}
for i in range(16):
    instructions[sequence[i]]=description_dict[sequence[i]]
    
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
if __name__ == "__main__":
    control_signal('control_signal.hex', seeTerminal=True)