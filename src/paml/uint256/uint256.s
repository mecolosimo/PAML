// functions for uint256 (32 bytes, four 64-bit uints)
.global _init_uint256
.global _uint256_is_equal
.global _uint256_is_greater
.global _uint256_is_less
.global _uint256_add
.align 2

.EQU UINT256_ID, 0X5B94B1AD6E34E064

// Inputs:
//   Uint256Struct    = x0 (ptr)
// Output:
//   None
_init_uint256:
    ldr x1, =UINT256_ID      // Loads the full 64-bit constant from memory and store
    str x1, [x0, #0]

    ret

// Inputs: 
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of A)
// Output:
//   x0 = 1 if A == B, else 0
_uint256_is_equal:
    // check to see if uint256 ints
    ldr x6, =UINT256_ID
    ldr x7, [x0]
    cmp x7, x6
    b.ne eq_ptr_fail

    ldr x7, [x1]
    cmp x7, x6
    b.ne eq_ptr_fail

    // load A and B
    ldr x2, [x0, #8]        // A high
    ldr x3, [x0, #16]        // A mid2
    ldr x4, [x0, #24]        // A mid1
    ldr x5, [x0, #32]        // A low

    ldr x6, [x1, #8]        // B high
    ldr x7, [x1, #16]        // B mid2
    ldr x8, [x1, #24]        // B mid1
    ldr x9, [x1, #32]        // B low

    // compare the low 64 bits
    cmp x5, x9

    // compare mid1 bits ONLY IF the low bits matched (eq).
    // if they didn't match, force the flags to mismatch (Z=0).
    ccmp x4, x8, #0, eq

    // compare mid2 bits ONLY IF the low bits matched (eq).
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
//   B = x1 (ptr to structure of A)
// Output:
//   x0 = 1 if A > B, else 0
_uint256_is_greater:
    // check to see if uint256 ints
    ldr x6, =UINT256_ID
    ldr x7, [x0]
    cmp x7, x6
    b.ne gt_ptr_fail

    ldr x7, [x1]
    cmp x7, x6
    b.ne gt_ptr_fail

    // load A and B
    ldr x2, [x0, #8]        // A high
    ldr x3, [x0, #16]        // A mid2
    ldr x4, [x0, #24]        // A mid1
    ldr x5, [x0, #32]        // A low

    ldr x6, [x1, #8]        // B high
    ldr x7, [x1, #16]        // B mid2
    ldr x8, [x1, #24]        // B mid1
    ldr x9, [x1, #32]        // B low

    // compare the most significant 64 bits
    cmp     x2, x6
    b.ne    evaluate_gt_cmp     // if they aren't equal, high bits decide the outcome

    // high bits were identical. cmp net set of bit
    cmp     x3, x7
    b.ne    evaluate_gt_cmp     // if they aren't equal, mid bits decide the outcome

    cmp     x4, x8
    b.ne    evaluate_gt_cmp

    // high and mid bits were identical. Low bits decide everything
    cmp     x5, x9

evaluate_gt_cmp:
    // cset (Conditional Set) writes 1 into x0 if the last active comparison 
    // resulted in a "Higher" (Unsigned Greater Than) condition. Otherwise, it writes 0.
    cset    x0, hi            
    ret

gt_ptr_fail:
    mov x0, #0        // false
    ret

// Inputs: 
//   A = x0 (ptr to structure of A)
//   B = x1 (ptr to structure of B)
// Output:
//   x0 = 1 if A > B, else 0
_uint256_is_less:
    // check to see if uint256 ints
    ldr x6, =UINT256_ID
    ldr x7, [x0]
    cmp x7, x6
    b.ne lt_ptr_fail

    ldr x7, [x1]
    cmp x7, x6
    b.ne lt_ptr_fail

    // load A and B
    ldr x2, [x0, #8]        // A high
    ldr x3, [x0, #16]       // A mid2
    ldr x4, [x0, #24]       // A mid1
    ldr x5, [x0, #32]       // A low

    ldr x6, [x1, #8]        // B high
    ldr x7, [x1, #16]       // B mid2
    ldr x8, [x1, #24]       // B mid1
    ldr x9, [x1, #32]       // B low

    // compare the most significant 64 bits
    cmp     x2, x6
    b.ne    .evaluate_lt_cmp     // If they aren't equal, high bits decide the outcome

    // high bits were identical.
    cmp     x3, x7
    b.ne    .evaluate_lt_cmp     // If they aren't equal, mid bits decide the outcome

    cmp     x4, x8
    b.ne    .evaluate_lt_cmp

    // high and mid bits were identical. Low bits decide everything
    cmp     x5, x9

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
_uint256_add:
    // check to see if uint256 ints
    ldr x6, =UINT256_ID
    ldr x7, [x0, #0]
    cmp x7, x6
    b.ne add_ptr_fail

    ldr x7, [x1, #0]
    cmp x7, x6
    b.ne add_ptr_fail

    // load A and B
    ldr x3, [x0, #8]        // A high
    ldr x4, [x0, #16]       // A mid2
    ldr x5, [x0, #24]       // A mid1
    ldr x6, [x0, #32]       // A low

    ldr x7, [x1, #8]        // B high
    ldr x8, [x1, #16]       // B mid2
    ldr x9, [x1, #24]       // B mid1
    ldr x10, [x1, #32]      // B low

    // add low to high with carry propagation
    mov x20, #0
    ands xzr, xzr, x20       // clear all flags (including C, not sure if needed)
    adds x14, x6, x10       // low: set carry flag
    adcs x13, x5, x9        // mid1: use carry, set carry
    adcs x12, x4, x8        // mid2: use carry, set carry
    adcs x11, x3, x7        // high: use carry
    //cset x15, cs            // convert carry flag to register (x15=1 if carry)    
    b.cs add_overflow       // jump if carry (C flag = 1)

    // store results
    mov x20, #1
    str x20, [x2, #0]       // success
    mov x20, #0
    str x20, [x2, #1]
    str x15, [x2, #2]       // overflow should be zero

    str x11, [x2, #8]       // high
    str x12, [x2, #16]
    str x13, [x2, #24]
    str x14, [x2, #32]      // low

    ret

add_overflow:
    mov x20, #0
    str x20, [x2, #0]       // failed
    mov x20, #2         
    str x20, [x2, #1]       // overflow err
    mov x20, #1
    str x20, [x2, #2]       // overflow should be one

    ret

add_ptr_fail:
    mov x20, #0
    str x20, [x2, #0]       // failed
    str x20, [x2, #2]       // didn't add so no overflow
    mov x20, #1 
    str x20, [x2, #1]       // ptr error (incorrect types)

    ret
