global _start

section .data:
  numberone db 20
  numbertwo db 40
  gtm db "Number one is greater than Number two."
  gtml equ $ - gtm
  ltm db "Number two is greater than Number one."
  ltml equ $ - ltm
  em db "They're equal."
  eml equ $ - em


_start:
  cmp numberone, numbertwo
  jg greaterthan
  jl lessthan
  je equal

greaterthan:
  mov rax, 1
  mov rdi, 1
  lea rsi, [gtm]
  mov rdx, gtml
  syscall
  mov rax, 60
  mov rdi, 69
  syscall

lessthan:
  mov rax, 1
  mov rdi, 1
  lea rsi, [ltm]
  mov rdx, ltml
  syscall
  mov rax, 60
  mov rdi, 69
  syscall

equal:
  mov rax, 1
  mov rdi, 1
  lea rsi, [em]
  mov rdx, eml
  syscall
  mov rax, 60
  mov rdi, 69
  syscall
