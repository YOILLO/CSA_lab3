ld r1 65535
ld r2 65535
sv r1 0
sv r2 1

add r1 r2
sv r1 65534

ld r1 0
ld r2 1
add r2 r1
sv r2 65534

ld r1 0
ld r2 1
sub r1 r2
sv r1 65534

ld r1 0
ld r2 1
sub r2 r1
sv r2 65534

ld r1 0
ld r2 1
mul r1 r2
sv r1 65534

ld r1 0
ld r2 1
mul r2 r1
sv r2 65534

ld r1 0
ld r2 1
div r1 r2
sv r1 65534

ld r1 0
ld r2 1
div r2 r1
sv r2 65534

ld r1 0
ld r2 1
mod r1 r2
sv r1 65534

ld r1 0
ld r2 1
mod r2 r1
sv r2 65534
halt