# Python Functions: Basics and Practical Applications

---

## 1. Lesson Overview
This lesson introduces complete beginners to Python functions. You will learn why functions are essential for writing clean, reusable code, how to define and call them, how to pass data using parameters and arguments, how to return results, and how variable scope determines where variables can be accessed. By the end of this lesson, you will understand how to encapsulate logic into modular building blocks to solve programming problems efficiently. 

---

## 2. Learning Objectives
By the end of this 45-minute lesson, learners will be able to:
* Explain what Python functions are and why they prevent code repetition (the DRY principle).
* Define and call basic Python functions using proper syntax.
* Pass data into functions using parameters and arguments.
* Retrieve data from functions using the `return` statement.
* Differentiate between local and global variables.
* Write reusable functions to solve simple programming problems.

---

## 3. Introduction (5 minutes)
Imagine you are building a Python program to calculate the area of multiple rectangles. Without a function, you might copy and paste the same multiplication code over and over again:

```python
# Without functions - repetitive code
first_area = 5 * 3
second_area = 10 * 7
third_area = 8 * 4

print(f"Area 1: {first_area}")
print(f"Area 2: {second_area}")
print(f"Area 3: {third_area}")
```

If you need to change how the calculation works later, you have to update it in every single place. This is inefficient and prone to errors. 

**What is a Function?**
A Python function is a reusable block of code designed to perform a specific task. Think of it like a mini-program or a recipe: you give it some inputs, it performs its instructions, and it gives you a result. Once defined, you can run that block of code as many times as you want without rewriting it.

---

## 4. Main Concepts and Explanations (15 minutes)

### Defining and Calling a Function
To create a function in Python, you use the `def` keyword, followed by a descriptive function name, parentheses `()`, and a colon `:`.

```python
def greet_user():
    """A simple greeting function."""
    print("Hello! Welcome to Python programming.")

# Calling the function
greet_user()
```

**Anatomy of a Function:**
1. **`def`**: The keyword telling Python you are defining a function.
2. **`greet_user`**: The name of the function (written in `snake_case`).
3. **`()`**: Holds input parameters (empty if no inputs are needed).
4. ** `:`**: Marks the start of the function body.
5. **Indented Body**: The block of code that runs whenever the function is called.

### Parameters and Arguments
Functions become powerful when you pass data into them. 
* **Parameters**: The variable names listed inside the parentheses during the function *definition*.
* **Arguments**: The actual values you pass into the function when you *call* it.

```python
def calculate_area(width, height): # width and height are parameters
    return width * height

# 5 and 3 are arguments passed to the function
result = calculate_area(5, 3) 
print(result)  # Output: 15
```

### The `return` Statement
Functions can send data back to the main program using the `return` keyword. Once Python hits a `return` statement, the function stops running and hands the resulting value back.

```python
def add_numbers(a, b):
    sum_result = a + b
    return sum_result

total = add_numbers(10, 5)
print(total)  # Output: 15
```

### Variable Scope: Local vs. Global Variables
When working with functions, it is important to understand where variables can be accessed, which is known as **scope**:
* **Local Variables**: Variables created *inside* a function (including its parameters). They only exist while the function is running and cannot be accessed outside of it.
* **Global Variables**: Variables created in the main body of your code (outside any function). They can be read throughout the program, though functions should generally rely on parameters rather than modifying global state directly.

```python
# Global variable
multiplier = 2

def multiply_by_two(number):
    # 'result' is a local variable
    result = number * multiplier
    return result

print(multiply_by_two(5))  # Output: 10
# print(result)            # Error! 'result' is not accessible outside the function.
```

---

## 5. Practical Examples and Applications (10 minutes)

### Example 1: Reusable Calculation Function
Using the rectangle area example from our introduction, here is how a function cleans up repetitive code:

```python
def calculate_area(width, height):
    return width * height

# Reusing the function cleanly
print(f"Area 1: {calculate_area(5, 3)}")
print(f"Area 2: {calculate_area(10, 7)}")
print(f"Area 3: {calculate_area(8, 4)}")
```

### Example 2: Modular Temperature Converter
Functions help break down real-world logic into manageable, testable components. Here is a utility function that converts Fahrenheit to Celsius:

```python
def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return round(celsius, 2)

# Testing the converter with different temperatures
print(f"75°F is {fahrenheit_to_celsius(75)}°C")
print(f"32°F is {fahrenheit_to_celsius(32)}°C")
print(f"212°F is {fahrenheit_to_celsius(212)}°C")
```

---

## 6. Hands-on Activity (10 minutes)
**Task:** Write a Python program that includes a custom function. 

1. Create a function named `calculate_total_price` that takes two parameters: `item_price` and `tax_rate`.
2. Inside the function, calculate the total cost (`item_price + (item_price * tax_rate)`) and return it.
3. Call your function twice with different values and print the results using formatted strings (`f-strings`).

**Starter Code:**
```python
def calculate_total_price(item_price, tax_rate):
    # Write your code here
    pass

# Test your function here
# print(calculate_total_price(50.0, 0.05))
# print(calculate_total_price(100.0, 0.08))
```

---

## 7. Knowledge Check (5 minutes)

**Q1: Which keyword is used to define a function in Python?**
* A) `func`
* B) `define`
* C) `def`
* D) `function`  
*(Answer: C)*

**Q2: What is the purpose of the `return` statement in a function?**
* A) To print text directly to the console.
* B) To send a computed value back to the caller of the function.
* C) To restart the Python interpreter.
* D) To create a loop.  
*(Answer: B)*

**Q3: What is the difference between a parameter and an argument?**
* A) Parameters are values passed into a function call, while arguments are placeholders in the function definition.
* B) Parameters are placeholders defined in the function signature, while arguments are the actual values passed when calling the function.
* C) There is no difference; they mean the exact same thing.
* D) Arguments are only used in math calculations, while parameters are only used for printing text.  
*(Answer: B)*

**Q4: What happens if you try to access a local variable from outside the function where it was created?**
* A) Python will return `None`.
* B) Python will automatically convert it into a global variable.
* C) Python will raise a NameError because the variable does not exist outside that function's scope.
* D) Python will print the variable value to the console.  
*(Answer: C)*

---

## 8. Summary
* Functions are reusable blocks of code that help organize programs and eliminate code duplication.
* They are defined using the `def` keyword, take optional input parameters, and can send results back using the `return` statement.
* Variables defined inside a function have local scope and cannot be accessed outside of it.
* Using functions makes code cleaner, easier to test, and simpler to maintain as programs grow in size.

---

## 9. References
* GeeksforGeeks. *Python Functions*. Retrieved from [https://www.geeksforgeeks.org/python/python-functions/](https://www.geeksforgeeks.org/python/python-functions/)
* W3Schools. *Python Functions*. Retrieved from [https://www.w3schools.com/python/python_functions.asp](https://www.w3schools.com/python/python_functions.asp)
* CodeChef. *Functions in Python (Examples and Practice)*. Retrieved from [https://www.codechef.com/blogs/functions-in-python](https://www.codechef.com/blogs/functions-in-python)
* Universo Python. *Python Functions: Complete Guide with Examples*. Retrieved from [https://universopython.com/en/blog/python-functions-complete-guide](https://universopython.com/en/blog/python-functions-complete-guide)
* Real Python. *Defining and Calling Python Functions*. Retrieved from [https://realpython.com/courses/defining-and-calling-functions/](https://realpython.com/courses/defining-and-calling-functions/)
* PYnative. *18 Python Functions Coding Exercises with Solutions*. Retrieved from [https://pynative.com/python-functions-exercise-with-solutions/](https://pynative.com/python-functions-exercise-with-solutions/)
* Sweigart, Al. *Automate the Boring Stuff with Python*. Open Library: [https://openlibrary.org/works/OL17192141W](https://openlibrary.org/works/OL17192141W)
* Perkovic, Ljubomir. *Introduction to Computing Using Python*. Open Library: [https://openlibrary.org/works/OL21458935W](https://openlibrary.org/works/OL21458935W)

---

## References

### Websites
- [Python Functions - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-functions/)
- [Python Functions - W3Schools](https://www.w3schools.com/python/python_functions.asp)
- [Functions in Python (Examples and Practice) - CodeChef](https://www.codechef.com/blogs/functions-in-python)
- [Python Functions: Complete Guide with Examples [2026]](https://universopython.com/en/blog/python-functions-complete-guide)
- [Defining and Calling Python Functions](https://realpython.com/courses/defining-and-calling-functions/)
- [18 Python Functions Coding Exercises with Solutions - PYnative](https://pynative.com/python-functions-exercise-with-solutions/)

### Books
- [Automate the Boring Stuff with Python](https://openlibrary.org/works/OL17192141W)
- [Introduction to Computing Using Python](https://openlibrary.org/works/OL21458935W)
- [The Official Blender 2.3 guide](https://openlibrary.org/works/OL8989089W)

### YouTube videos
- [47. Functions in Python | Python PCEP Certification (PCEP-30-02)](https://www.youtube.com/watch?v=EthvAnHB3gU) - UiPath RPA
- [10) Master Python Functions](https://www.youtube.com/watch?v=UwtEMgpl-j4) - tech with jai
- [DAY-12|Python Complete Series|Python Functions with practical Examp](https://www.youtube.com/watch?v=cL3d4oVuduw) - AMERICAN ACADEMY RRC
- [Functions in Python | Python Full Course](https://www.youtube.com/watch?v=5vFOzaActuo) - TECH SUJAL

