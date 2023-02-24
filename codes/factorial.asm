ld r4 65535
ld r1 o1
sv r1 0
ld r2 o1
loop:
add r1 0
mul r2 r1
mov r3 r1
sub r3 r4
jz end
jmp loop
end:
sv r2 65534
halt
