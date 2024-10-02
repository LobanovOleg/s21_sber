import time
import argparse
from cyth.multiply import mul
from itertools import tee


def pure_python_mul(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ]
        for i, row_a in enumerate(a)
    ]


def generate_matrices(size):
    return [[i + j for j in range(size)] for i in range(size)], [
        [j + 1 for j in range(size)] for i in range(size)
    ]


if __name__ == "__main__":
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Matrix multiplication performance test."
    )
    parser.add_argument(
        "--size", type=int, default=100, help="Size of the matrices (default: 100)"
    )
    args = parser.parse_args()

    size = args.size
    x, y = generate_matrices(size)

    # Тестирование реализации на чистом Python
    start = time.monotonic_ns()
    result_python = pure_python_mul(x, y)
    finish = time.monotonic_ns()
    print("Результат на чистом Python:", result_python)
    print("Время на чистом Python:", finish - start)

    # Тестирование реализации на Cython
    start = time.monotonic_ns()
    result_cython = mul(x, y)
    finish = time.monotonic_ns()
    print("Результат на Cython:", result_cython)
    print("Время на Cython:", finish - start)
