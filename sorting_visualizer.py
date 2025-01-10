import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
import ttkbootstrap as tb
import random
import time
import winsound

# Global variables
array = []
speed = 0.1
sorting_algorithm = None
array_size=20



# Function to generate a random array
def generate_array():
    global array, is_running
    is_running = True  # Reset the running flag
    array = [random.randint(10, 100) for _ in range(array_size)]
    draw_array(array, ["gray" for _ in range(len(array))])

# Function to take user input for the array
def input_array():
    global array
    user_input = simpledialog.askstring("Input Array", "Enter numbers separated by spaces:")
    if user_input:
        try:
            array = list(map(int, user_input.split()))
            draw_array(array, ["gray" for _ in range(len(array))])
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid array of integers.")

# Function to draw the array on the canvas
def draw_array(array, colors):
    canvas.delete("all")
    canvas_width = 800
    canvas_height = 400
    bar_width = max(canvas_width / len(array), 5)  # Adjust bar width for larger arrays
    for i, value in enumerate(array):
        x0 = i * bar_width
        y0 = canvas_height - value * 3  # Scale bars for better visibility
        x1 = (i + 1) * bar_width - 2  # Add spacing between bars
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i])
        canvas.create_text(x0 + bar_width / 2, y0, anchor=tk.S, text=str(value), font=("Arial", 10), fill="white")
    root.update_idletasks()

# Play sound based on bar height
def play_sound(value):
    frequency = 100 + value * 10
    winsound.Beep(frequency, 50)

# Insertion Sort
def insertion_sort():
    global array
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
            draw_array(array, ["yellow" if x == j + 1 or x == j else "gray" for x in range(len(array))])
            play_sound(array[j + 1])
            time.sleep(speed)
        array[j + 1] = key
    draw_array(array, ["green" for _ in range(len(array))])

# Bubble Sort
def bubble_sort():
    global array, is_running
    for i in range(len(array)):
        if not is_running:
            return
        for j in range(len(array) - i - 1):
            if not is_running:
                return
            draw_array(array, ["yellow" if x == j or x == j + 1 else "gray" for x in range(len(array))])
            play_sound(array[j])
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            time.sleep(speed)
    draw_array(array, ["green" for _ in range(len(array))])
# Selection Sort
def selection_sort():
    global array
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            draw_array(array, ["yellow" if x == j or x == min_idx else "gray" for x in range(len(array))])
            play_sound(array[j])
            if array[j] < array[min_idx]:
                min_idx = j
            time.sleep(speed)
        array[i], array[min_idx] = array[min_idx], array[i]
    draw_array(array, ["green" for _ in range(len(array))])

# Merge Sort
def merge_sort():
    def merge(arr, l, m, r):
        left = arr[l:m + 1]
        right = arr[m + 1:r + 1]
        i = j = 0
        k = l

        while i < len(left) and j < len(right):
            draw_array(array, ["yellow" if x == k else "gray" for x in range(len(arr))])
            play_sound(arr[k])
            time.sleep(speed)
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    def merge_sort_recursive(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort_recursive(arr, l, m)
            merge_sort_recursive(arr, m + 1, r)
            merge(arr, l, m, r)

    merge_sort_recursive(array, 0, len(array) - 1)
    draw_array(array, ["green" for _ in range(len(array))])

# Quick Sort
def quick_sort():
    def partition(low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            draw_array(array, ["yellow" if x == j or x == high else "gray" for x in range(len(array))])
            play_sound(array[j])
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
            time.sleep(speed)
        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(array) - 1)
    draw_array(array, ["green" for _ in range(len(array))])

# Heap Sort
def heap_sort():
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and array[left] > array[largest]:
            largest = left

        if right < n and array[right] > array[largest]:
            largest = right

        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            heapify(n, largest)

    n = len(array)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(i, 0)
        draw_array(array, ["yellow" if x == i else "gray" for x in range(len(array))])
        time.sleep(speed)
    draw_array(array, ["green" for _ in range(len(array))])

# Sort Function
def start_sorting():
    if sorting_algorithm == "Bubble Sort":
        bubble_sort()
    elif sorting_algorithm == "Selection Sort":
        selection_sort()
    elif sorting_algorithm == "Merge Sort":
        merge_sort()
    elif sorting_algorithm == "Quick Sort":
        quick_sort()
    elif sorting_algorithm == "Heap Sort":
        heap_sort()
    elif sorting_algorithm == "Insertion Sort":
        insertion_sort()


# Function to set the sorting algorithm and time complexity
def set_algorithm(algorithm):
    global sorting_algorithm
    sorting_algorithm = algorithm
    
    # Display the time complexity based on selected algorithm
    if algorithm == "Bubble Sort":
        complexity_label.config(text="Time Complexity: O(n²)")
    elif algorithm == "Selection Sort":
        complexity_label.config(text="Time Complexity: O(n²)")
    elif algorithm == "Merge Sort":
        complexity_label.config(text="Time Complexity: O(n log n)")
    elif algorithm == "Quick Sort":
        complexity_label.config(text="Time Complexity: O(n log n) [Average], O(n²) [Worst]")
    elif algorithm == "Heap Sort":
        complexity_label.config(text="Time Complexity: O(n log n)")

# UI Setup (Add this inside the UI setup)
# complexity_label = tk.Label(ui_frame, text="Time Complexity: O(n²)", font=("Arial", 10))
# complexity_label.grid(row=1, column=2, padx=10, pady=10)


# Speed control
def set_speed(val):
    global speed
    speed = float(val)

# UI Setup
root = tb.Window(themename="darkly")
root.title("Sorting Visualizer")
root.geometry("800x600")

# Frames
ui_frame = tk.Frame(root, width=1600, height=100)
ui_frame.pack(side=tk.TOP)
canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.pack(side=tk.BOTTOM)

# Dropdown menu for algorithm selection
algo_label = tk.Label(ui_frame, text="Algorithm:")
algo_label.grid(row=0, column=0, padx=10, pady=10)
algo_menu = ttk.Combobox(ui_frame, values=["Bubble Sort", "Selection Sort", "Merge Sort", "Quick Sort", "Heap Sort"])
algo_menu.grid(row=0, column=1, padx=10, pady=10)
algo_menu.bind("<<ComboboxSelected>>", lambda e: set_algorithm(algo_menu.get()))

# Buttons
generate_btn = ttk.Button(ui_frame, text="Generate Random Array", command=generate_array)
generate_btn.grid(row=0, column=2, padx=10, pady=10)

input_btn = ttk.Button(ui_frame, text="Input Array", command=input_array)
input_btn.grid(row=0, column=3, padx=10, pady=10)

start_btn = ttk.Button(ui_frame, text="Start Sorting", command=start_sorting)
start_btn.grid(row=0, column=4, padx=10, pady=10)

# Speed control slider
speed_label = tk.Label(ui_frame, text="Speed:")
speed_label.grid(row=1, column=0, padx=10, pady=10)
speed_slider = ttk.Scale(ui_frame, from_=0.01, to=0.5, length=200, orient="horizontal", command=set_speed)
speed_slider.grid(row=1, column=1, padx=10, pady=10)
speed_slider.set(0.1)

# Time complexity label
complexity_label = tk.Label(ui_frame, text="", font=("Arial", 10), justify=tk.LEFT)
complexity_label.grid(row=1, column=2, padx=10, pady=10)

# Function to set the sorting algorithm and time complexity
def set_algorithm(algorithm):
    global sorting_algorithm
    sorting_algorithm = algorithm
    
    # Display the time complexity based on selected algorithm
    if algorithm == "Bubble Sort":
        complexity_label.config(text="Time Complexity: O(n²)\nBest: O(n)\nAverage: O(n²)\nWorst: O(n²)\nStable Sort")
    elif algorithm == "Selection Sort":
        complexity_label.config(text="Time Complexity: O(n²)\nBest: O(n²)\nAverage: O(n²)\nWorst: O(n²)\nUnstable Sort")
    elif algorithm == "Merge Sort":
        complexity_label.config(text="Time Complexity: O(n log n)\nBest: O(n log n)\nAverage: O(n log n)\nWorst: O(n log n)\nStable Sort")
    elif algorithm == "Quick Sort":
        complexity_label.config(text="Time Complexity: O(n log n) [Average], O(n²) [Worst]\nBest: O(n log n)\nAverage: O(n log n)\nWorst: O(n²)\nUnstable Sort")
    elif algorithm == "Heap Sort":
        complexity_label.config(text="Time Complexity: O(n log n)\nBest: O(n log n)\nAverage: O(n log n)\nWorst: O(n log n)\nUnstable Sort")

# Initialize
generate_array()
root.mainloop()
