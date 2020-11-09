#PYCLOUDIOT : LIBRARY,2,10,fibonacci_library.py,
def Fibonacci(n=40):
    if n<0: 
        print("Incorrect input") 
    elif n==1: 
        return 0
    elif n==2: 
        return 1
    else: 
        return Fibonacci(n-1)+Fibonacci(n-2) 

#PYCLOUDIOT : MAIN,7,10,slicing_main.py, #IMPORTS :slicing_library.py  ;ulab,
a = 1
b = 2
c = 3
to_calculate = a + b + c
Fibonacci(to_calculate)