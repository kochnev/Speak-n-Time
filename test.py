def fibo():
    a, b = 0, 1
    while True:
        yield a
        b = a + b
        a = b


for x in range(10):
    fgen = fibo()
    print(next(fgen))

