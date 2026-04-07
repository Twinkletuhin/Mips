# ---------------------------
# Register Initialization
# ---------------------------

addi $t0, $zero, 3      # t0 = 3
addi $t1, $zero, 1      # t1 = 1
addi $t2, $zero, 2      # t2 = 2
addi $t3, $zero, 4      # t3 = 4
addi $t4, $zero, 0      # t4 = 0

# ---------------------------
# R-TYPE ARITHMETIC
# ---------------------------

# add $t4, $t0, $t1       # t4 = 3 + 1 = 4
# sub $t4, $t0, $t1       # t4 = 3 - 1 = 2

# ---------------------------
# LOGIC
# ---------------------------

# and $t4, $t0, $t2       # t4 = 3 & 2
# or  $t4, $t0, $t1       # t4 = 3 | 1
# nor $t4, $t0, $t1       # t4 = ~(3|1)

# ---------------------------
# IMMEDIATE INSTRUCTIONS
# ---------------------------

# addi $t0, $t0, 1        # t0 = t0 + 1
# subi $t0, $t0, 1        # t0 = t0 - 1
# andi $t1, $t0, 2        # t1 = t0 & 2
# ori  $t1, $t1, 1        # t1 = t1 | 1

# ---------------------------
# SHIFT
# ---------------------------

# sll $t2, $t1, 1         # t2 = t1 << 1
# srl $t2, $t2, 1         # t2 = t2 >> 1

# ---------------------------
# MEMORY OPERATIONS
# ---------------------------

# addi $sp, $sp, -1      # initialize stack pointer

# sw $t1, 0($sp)          # MEM[sp] = t0
# lw $t2, 0($sp)          # t3 = MEM[sp]

# ---------------------------
# STACK OPERATIONS
# ---------------------------

# push $t1                # push t1
# push $t2                # push t2

# pop $t4                 # t4 = top
# pop $t3                 # t3 = next

# ---------------------------
# BRANCH TEST
# ---------------------------

# addi $t0, $zero, 2
# addi $t1, $zero, 2

# beq $t0, $t1, equal_label   # branch taken

# addi $t2, $zero, 3          # skipped

# equal_label:
# addi $t2, $zero, 7

# # ---------------------------
# # BNE TEST
# # ---------------------------

# addi $t0, $zero,3
# addi $t1, $zero, 3

# bneq $t0, $t1, notequal

# addi $t3, $zero, 7          # skipped

# notequal:
# addi $t3, $zero, 6

# # ---------------------------
# # JUMP TEST
# # ---------------------------

# j end_program

# addi $t4, $zero, 5          # skipped

# end_program:
# addi $t4, $zero, 4