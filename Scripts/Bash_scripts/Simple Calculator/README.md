# Simple Bash Calculator

## 📋 Code Comments & Logic Breakdown

### 1. Dependency Handling

The script includes a check for the `bc` package. Since Bash cannot perform decimal math natively, `bc` acts as the external engine for the calculator.

### 2. Input Parsing (Regex)

Instead of simple `read` variables, this script uses **Regular Expressions**.

* `^([+-]?[0-9]*\.?[0-9]+)` : Captures the first number (integer or decimal).
* `\s*([\+\-\*\/])\s*` : Captures the mathematical operator while ignoring extra spaces.
* `([+-]?[0-9]*\.?[0-9]+)$` : Captures the second number at the end of the string.

### 3. Floating-Point Calculation

The calculation is performed by piping a string into `bc`.
`echo "scale=4; 10 / 3" | bc`
The `scale=4` is a specific command for `bc` that tells it how many decimal places to return.

## 🚀 How to Run

1. `chmod +x simple_bash_calculator.sh`
2. `./simple_bash_calculator.sh`

---
**Author:** Wayne Stock  
**Environment:** Bash / Linux  
**Update:** 2026
