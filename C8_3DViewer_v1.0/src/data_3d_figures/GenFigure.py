import random

vertices = 100
rangee = 10000

with open(f'{vertices}Vertices.obj', 'w') as file:
    for i in range(1, vertices + 1):
        vertex1 = random.randint(-rangee, rangee) / rangee
        vertex2 = vertex1
        vertex3 = vertex1
        while vertex1 == vertex2:
            vertex2 = random.randint(-rangee, rangee) / rangee
        while vertex3 == vertex2 or vertex3 == vertex1:
            vertex3 = random.randint(-rangee, rangee)/ rangee
        vertex = f'v {vertex1} {vertex2} {vertex3}\n'
        file.write(vertex)
    for i in range(1, vertices + 1):
        vertex1 = i
        vertex2 = random.randint(1, vertices)
        while vertex2 == vertex1:
            vertex2 = random.randint(1, vertices)
        vertex3 = random.randint(1, vertices)
        while vertex3 == vertex1 or vertex3 == vertex2:
            vertex3 = random.randint(1, vertices)
        edge = f'f {vertex1} {vertex2} {vertex3}\n'
        file.write(edge)
