def query(x):
    return -1 * (x - 7) ** 2 + 49

def find_peak(N: int) -> int:
    x = N // 2
    while 0 < x < N:
        if query(x) < query(x + 1):
            x += 1
        elif query(x) < query(x - 1):
            x -= 1
        else:
            break
    return x

N = 14
print(find_peak(N))
