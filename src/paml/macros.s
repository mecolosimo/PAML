# macros (as is weirdly case sensitive about .endm but not .MARCO)

.macro PUSH1 register
    str \register, [SP, #-16]!
.endm

.macro POP1 register
    ldr \register, [SP], #16
.endm

.macro PUSH2 register1, register2
    stp \register1, \register2, [SP, #-16]!
.endm

.macro POP2 register1, register2
    ldp \register1, \register2, [SP], #16
.endm
