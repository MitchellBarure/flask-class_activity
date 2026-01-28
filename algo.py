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
        else:
            raise ValueError("Algorithm is not supported. Use: bubble or linear")

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
