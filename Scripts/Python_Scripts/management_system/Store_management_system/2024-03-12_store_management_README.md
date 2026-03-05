# Store Management System

**Created:** 2024-03-12  
**Updated:** 2025-12-25  
**Author:** omegazyph  
**Platform:** Windows 11 (Lenovo Legion)  
**Environment:** VSCode / Python 3.x  

---

## 📝 Description

The **Store Management System** is a Python-based utility designed to simulate real-world grocery store interactions. It manages staff member profiles and provides a robust age-verification workflow for customers attempting to purchase age-restricted items.

## 🚀 Key Features

* **Employee Tracking:** Manages staff names, ages, and department assignments with status reporting.
* **Two-Step Age Verification:** 1.  **ID Check:** Confirms if a shopper possesses valid identification.
    2.  **Age Logic:** If ID is present, the system verifies the user is 21 or older.
* **Readable Output:** Implements `__repr__` methods for clean, professional object summaries in the console.
* **Modern Formatting:** Uses Python f-strings for optimized string interpolation.

## 🛠️ Usage

### Employee Management

python
bob = Employee("Bob", 36, "Perishables")
bob.working() # Output: Bob is 36 and currently working in Perishables.

Shopper Verification
Python

richard = Shopper("Richard", 21, True)
richard.id_check() # Checks ID status then triggers age verification.

## 📂 File Structure

    store_management.py: The core logic containing Employee and Shopper classes.

    README.md: System documentation (this file).

## 📝 Change Log

[2025-12-25]

    Refactored string formatting from .format() to modern f-strings.

    Improved variable naming (e.g., id changed to has_id) for better clarity.

    Added detailed docstrings and comments for better maintainability in VSCode.

    Fixed attribute naming errors in the working() method.
