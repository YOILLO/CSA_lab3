call func1
call func2
call func3
call func_rec1
call func_rec2
halt

func1:
ld r1 o1
sv r1 65534
ret

func2:
ld r1 o2
sv r1 65534
ret

func_rec1:
ld r1 o3
sv r1 65534
call func1
ret

func_rec2:
ld r1 o3
sv r1 65534
jmp func1

func3:
ld r1 o0
push r1
ld r1 o1
sv r1 65534
pop r1
sv r1 65534
ret