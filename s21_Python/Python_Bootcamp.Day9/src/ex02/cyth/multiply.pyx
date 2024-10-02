def mul(list a, list b):
    if len(a[0]) != len(b):
        raise ValueError("The width of the first matrix should be equal to the height of the second one.")
    
    if len(a) > 100 or len(a[0]) > 100:
        raise ValueError("Cannot be larger then 100.")
    
    if len(b) > 100 or len(b[0]) > 100:
        raise ValueError("Cannot be larger then 100.")
    
    for i in range(len(a)):
        for j in range(len(a[0])):
            if not isinstance(a[i][j], int):
                raise TypeError("Numbers must be integers only.")
            
    for i in range(len(b)):
        for j in range(len(b[0])):
            if not isinstance(b[i][j], int):
                raise TypeError("Numbers must be integers only.")
            
    cdef int m = len(a)
    cdef int n = len(b[0])
    cdef int l = len(b)
    cdef list res = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            s = 0
            for k in range(l):
                s += a[i][k] * b[k][j]
            res[i][j] = s
    
    return res
