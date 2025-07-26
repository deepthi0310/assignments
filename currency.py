def format_currency(a):
    i = '.'
    if i in a:
        w, f = a.split(i)
        f = i + f
    else:
        w, f = a, ''
    if len(w) <= 3:
        return w + f
    head = w[-3:]
    tail = w[:-3]
    result = ""
    while len(tail) > 2:
        result = "," + tail[-2:] + result
        tail = tail[:-2]
    result = tail + result if tail else result
    return result + "," + head + f if result else head + f

a = input()
print(format_currency(a))