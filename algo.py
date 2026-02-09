#algo.py

#Import tool to get test data and timing functions to measure runtime of algo
import random
import time

#Sort list in correct order
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

#Check each element, until value is found
def linear_search(arr, target):
    for x in arr:
        if x == target:
            return True
    return False

# Binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

# Nested loops (O(n^2))
def nested_loops(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count

# Exponential example: recursive Fibonacci (O(2^n))
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def run_analysis(algo, n, steps):
    if steps < 1:
        steps = 1

    algo = algo.lower()

    sizes = []
    times = []

    for step in range(1, steps + 1):
        size = int(step * n / steps)
        data = [random.randint(0, 100000) for _ in range(size)]

        start = time.perf_counter()

        if algo == "bubble":
            bubble_sort(data)
            complexity = "O(n^2)"
        elif algo == "linear":
            target = data[-1]
            linear_search(data, target)
            complexity = "O(n)"
        elif algo == "binary":
            data = sorted([random.randint(0, 100000) for _ in range(size)])
            target = data[-1]
            binary_search(data, target)
            complexity = "O(log n)"
        elif algo == "nested":
            nested_loops(size)
            complexity = "O(n^2)"
        elif algo == "exponential":
            # Exponential algorithms explode quickly, so map size to a safe fib input
            fib_n = min(28, max(1, size // 10))
            fib_recursive(fib_n)
            complexity = "O(2^n)"
        else:
            raise ValueError("Algorithm is not supported. Use: bubble, linear, binary, nested or exponential")

        end = time.perf_counter()

        sizes.append(size)
        times.append((end - start) * 1000)

    return {
        "algo": algo,
        "items": n,
        "steps": steps,
        "sizes": sizes,
        "times": times,
        "time_complexity": complexity
    }
