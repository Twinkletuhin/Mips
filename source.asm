addi $t1, $zero, 1        #00000000  $t1 = 1
addi $t2, $zero, 3        #00000001  $t2 = 3
add  $t0, $t1, $t2        #00000010  $t0 = 4
add  $t3, $t0, $t2        #00000011  $t3 = 7
add  $t4, $t0, $t1        #00000100  $t4 = 5
sw   $t1, 3($t2)          #00000101  mem[6] = 1
sll  $t1, $t1, 2          #00000110  $t1 = 4
beq  $t0, $t1, label1     #00000111  branch taken
j    end                  #00001000  (skipped)

label1:
sub  $t4, $t3, $t0        #00001001  $t4 = 3
subi $t3, $t3, 1          #00001010  $t3 = 6
srl  $t3, $t3, 1          #00001011  $t3 = 3
lw   $t1, 3($t2)          #00001100  $t1 = 1
and  $t0, $t1, $t3        #00001101  $t0 = 1
or   $t1, $t3, $t4        #00001110  $t1 = 3
j    label2               #00001111  jump

label3:
push $t0                  #00010000 00010001  mem[FF] = 1
push $t1                  #00010010 00010011  mem[FE] = 3
ori  $t0, $t0, 4          #00010100  $t0 = 5
pop  $t0                  #00010101 00010110  $t0 = 3
andi $t2, $t2, 0          #00010111  $t2 = 0
pop  $t2                  #00011000 00011001  $t2 = 1
nor  $t2, $t2, $t2        #00011010  $t2 = -2
j    end                  #00011011

label2:
bneq $t0, $t2, near_label #00011100  branch taken
j    end                  #00011101  (skipped)

near_label:
j    label3               #00011110  jump

end: