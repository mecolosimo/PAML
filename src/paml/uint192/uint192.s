// functions for uint192 (24 bytes, three 64-bit uints)
.global _init_uint192
.global _uint192_is_equal
.global _uint192_is_greater
.global _uint192_is_less
.global _uint192_add
.global _uint192_sub
.global _uint192_mul
.align 2

.include "src/paml/constants.s"

// Inputs:
//   uint192Struct    = x0 (ptr)
// Output:
//   None
_init_uint192:
    ldr x1, =UINT192_ID      // Loads the full 64-bit constant from memory and store
    str x1, [x0, #0]

    ret

// Inputs: 
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of B)
// Output:
//   x0 = 1 if A == B, else 0
_uint192_is_equal:
    // check to see if uint192 ints
    ldr x6, =UINT192_ID
    ldr x7, [x0]
    cmp x7, x6
    b.ne eq_ptr_fail

    ldr x7, [x1]
    cmp x7, x6
    b.ne eq_ptr_fail

    // load A and B
    ldr x2, [x0, #8]            // A high
    ldr x3, [x0, #16]           // A mid
    ldr x4, [x0, #24]           // A low

    ldr x6, [x1, #8]            // B high
    ldr x7, [x1, #16]           // B mid
    ldr x8, [x1, #24]           // B low

    // compare the low 64 bits
    cmp x4, x8

    // compare mid bits ONLY IF the low bits matched (eq).
    // if they didn't match, force the flags to mismatch (Z=0).
    ccmp x3, x7, #0, eq

    // compare high bits ONLY IF all previous bits matched (eq).
    ccmp x2, x6, #0, eq

    // set x0 to 1 if the final state is Equal (Z=1), otherwise 0.
    cset x0, eq       
    ret

eq_ptr_fail:
    mov x0, #0        // false
    ret

// Inputs: 
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of B)
// Output:
//   x0 = 1 if A > B, else 0
_uint192_is_greater:
    // check to see if uint192 ints
    ldr x6, =UINT192_ID
    ldr x7, [x0]
    cmp x7, x6
    b.ne gt_ptr_fail

    ldr x7, [x1]
    cmp x7, x6
    b.ne gt_ptr_fail

    // load A and B
    ldr x2, [x0, #8]            // A high
    ldr x3, [x0, #16]           // A mid
    ldr x4, [x0, #24]           // A low

    ldr x6, [x1, #8]            // B high
    ldr x7, [x1, #16]           // B mid
    ldr x8, [x1, #24]           // B low

    // compare the most significant 64 bits
    cmp     x2, x6
    b.ne    evaluate_gt_cmp     // if they aren't equal, high bits decide the outcome

    // high bits were identical. cmp net set of bit
    cmp     x3, x7
    b.ne    evaluate_gt_cmp     // if they aren't equal, mid bits decide the outcome

    // high and mid bits were identical. Low bits decide everything
    cmp     x4, x8

evaluate_gt_cmp:
    // cset (Conditional Set) writes 1 into x0 if the last active comparison 
    // resulted in a "Higher" (Unsigned Greater Than) condition. Otherwise, it writes 0.
    cset    x0, hi            
    ret

gt_ptr_fail:
    mov x0, #0                  // false
    ret

// Inputs: 
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of B)
// Output:
//   x0 = 1 if A > B, else 0
_uint192_is_less:
    // check to see if uint192 ints
    ldr x6, =UINT192_ID
    ldr x7, [x0]
    cmp x7, x6
    b.ne lt_ptr_fail

    ldr x7, [x1]
    cmp x7, x6
    b.ne lt_ptr_fail

    // load A and B
    ldr x2, [x0, #8]            // A high
    ldr x3, [x0, #16]           // A mid
    ldr x4, [x0, #24]           // A low

    ldr x6, [x1, #8]            // B high
    ldr x7, [x1, #16]           // B mid
    ldr x8, [x1, #24]           // B low

    // compare the most significant 64 bits
    cmp     x2, x6
    b.ne    .evaluate_lt_cmp     // If they aren't equal, high bits decide the outcome

    // high bits were identical
    cmp     x3, x7
    b.ne    .evaluate_lt_cmp     // If they aren't equal, mid bits decide the outcome

    // high and mid bits were identical. Low bits decide everything
    cmp     x4, x8

.evaluate_lt_cmp:
    // cset (Conditional Set) writes 1 into x0 if the last active comparison 
    // resulted in a "Lower" (Unsigned Less Than) condition. Otherwise, it writes 0.
    cset    x0, cc            
    ret

lt_ptr_fail:
    mov x0, #0        // false
    ret

// Input:
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of B)
//   ResStruct = x2 (ptr to structure of Res)
// Output:
//   None
_uint192_add:
    // check to see if uint192 ints
    ldr x6, =UINT192_ID
    ldr x7, [x0, #0]
    cmp x7, x6
    b.ne add_ptr_fail

    ldr x7, [x1, #0]
    cmp x7, x6
    b.ne add_ptr_fail

    // load A and B
    ldr x3, [x0, #8]            // A high
    ldr x4, [x0, #16]           // A mid
    ldr x5, [x0, #24]           // A low

    ldr x6, [x1, #8]            // B high
    ldr x7, [x1, #16]           // B mid
    ldr x8, [x1, #24]           // B low

    // add low to high with carry propagation
    adds x14, x5, x8            // low: set carry flag
    adcs x13, x4, x7            // mid1: use carry, set carry
    adcs x12, x3, x6            // high: use carry    
    b.cs add_overflow           // jump if carry (C flag = 1)

    // store results
    mov x20, #1
    str x20, [x2, #0]           // success
    mov x20, #0
    str x20, [x2, #1]           // no overflow

    // padding to 8 byte boundery
    str x12, [x2, #8]          // high
    str x13, [x2, #16]
    str x14, [x2, #24]          // low

    ret

add_overflow:
    mov x20, #0
    str x20, [x2, #0]           // failed
    mov x20, #2         
    str x20, [x2, #1]           // overflow error

    ret

add_ptr_fail:
    mov x20, #0
    str x20, [x2, #0]           // failed
    mov x20, #1 
    str x20, [x2, #1]           // ptr error (incorrect types)

    ret

// Input:
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of B)
//   ResStruct = x2 (ptr to structure of Res)
// Output:
//   None
_uint192_sub:
    // check to see if uint192 ints
    ldr x6, =UINT192_ID
    ldr x7, [x0, #0]
    cmp x7, x6
    b.ne add_ptr_fail           // sub_ptr_fail

    ldr x7, [x1, #0]
    cmp x7, x6
    b.ne add_ptr_fail           // sub_ptr_fail

    // load A and B
    ldr x3, [x0, #8]            // A high
    ldr x4, [x0, #16]           // A mid
    ldr x5, [x0, #24]           // A low

    ldr x6, [x1, #8]            // B high
    ldr x7, [x1, #16]           // B mid
    ldr x8, [x1, #24]           // B low

    // Use 'subs' to set the carry flag if a borrow is needed
    subs x14, x5, x8            // x13 = x5 - x9 (sets borrow flag)
    sbcs x13, x4, x7            // x12 = x4 - x8 - borrow
    sbcs x12, x3, x6            // x11 = x3 - x7 - borrow
    b.cc sub_underflow

    // store results
    mov x20, #1
    str x20, [x2, #0]           // success
    mov x20, #0
    str x20, [x2, #1]           // no underflow, no error

    str x12, [x2, #8]           // low
    str x13, [x2, #16]
    str x14, [x2, #24]          // high

    ret

sub_underflow:
    mov x20, #0
    str x20, [x2, #0]           // failed
    mov x20, #3
    str x20, [x2, #1]           // underflow error

    ret

// Input:
//   A = x0 (ptr to structure of A, 192-bit uint)
//   B = x1 64-bit uint
//   ResStruct = x2 (ptr to structure of Res, holds 256-bit uint)
// Output:
//   None
_uint192_mul:
    // check to see if uint192 ints
    ldr x6, =UINT192_ID
    ldr x7, [x0, #0]
    cmp x7, x6
    b.ne mul_ptr_fail

    ldr x3, [x0, #8]        // A high
    ldr x4, [x0, #16]        // A mid
    ldr x5, [x0, #24]       // A low

    // A low 64-bits
    mul x6, x5, x1          // low 64-bits
    umulh x7, x5, x1

    // mid 64-bits
    mul x8, x4, x1
    umulh x9, x4, x1
    adds x8, x8, x7         // C mid1 64-bits
    adc x9, x9, xzr

    // mid 64-bits
    mul x10, x3, x1
    umulh x11, x3, x1
    adds x10, x10, x9       // C mid2 64-bits
    adc x11, x11, xzr       // C high 64-bits

    // save
    mov x20, #1
    str x20, [x2, #0]       // success
    mov x20, #0
    str x20, [x2, #1]       // no err

    str x6, [x2, #32]       // low
    str x8, [x2, #24]
    str x10, [x2, #16]
    str x11, [x2, #8]       // high
    ret

mul_ptr_fail:
    mov x20, #0
    str x20, [x2, #0]           // failed
    mov x20, #1 
    str x20, [x2, #1]           // ptr error (incorrect types)

    ret