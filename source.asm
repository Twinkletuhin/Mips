start:
addi $t0,$zero,5
amar:
beq $t0,$zero,end
sll $t0,$t1,2
end:
lw $t1,-4($sp)
tomar:
sub $t2,$t1,$t0
j end