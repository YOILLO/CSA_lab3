ld r1 o1
sv r1 0
ld r1 o1
sv r1 1

loop:
ld r1 0
ld r2 1
add r1 r2
sv r2 0
sv r1 1
clz
mod r1 o2
jz summ
jmp compare
summ:
ld r1 1
ld r2 2
add r2 r1
sv r2 2
compare:
ld r1 1
cln
sub r1 o4000000
jn loop
ld r1 2
sv r1 65534
