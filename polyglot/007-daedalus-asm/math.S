.intel_syntax noprefix
.text
.globl daedalus_gcd
.type daedalus_gcd, @function
daedalus_gcd:
    mov rax, rdi
    test rsi, rsi
    jz .Lgcd_done
.Lgcd:
    xor edx, edx
    div rsi
    mov rax, rsi
    mov rsi, rdx
    test rsi, rsi
    jnz .Lgcd
.Lgcd_done:
    ret
.size daedalus_gcd, .-daedalus_gcd

.globl daedalus_sum
.type daedalus_sum, @function
daedalus_sum:
    xor eax, eax
    test rsi, rsi
    jz .Lsum_done
.Lsum:
    add rax, [rdi]
    add rdi, 8
    dec rsi
    jnz .Lsum
.Lsum_done:
    ret
.size daedalus_sum, .-daedalus_sum

.globl daedalus_popcount
.type daedalus_popcount, @function
daedalus_popcount:
    xor eax, eax
    test rdi, rdi
    jz .Lpop_done
.Lpop:
    lea rdx, [rdi - 1]
    inc eax
    and rdi, rdx
    jnz .Lpop
.Lpop_done:
    ret
.size daedalus_popcount, .-daedalus_popcount
.section .note.GNU-stack,"",@progbits
