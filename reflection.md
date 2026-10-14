# Lab 5: Static Code Analysis — Reflection

### 1. What is the purpose of static code analysis?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, coding-standard violations, and maintainability problems. In this lab, Pylint, Bandit, and Flake8 helped identify different categories of issues in the helpdesk ticketing program.

### 2. What issues did you identify and fix?

The original program had a mutable default argument, a bare exception handler, unsafe shell-command execution, missing input validation, inconsistent naming conventions, missing docstrings, and unsafe file-handling practices. I fixed these issues by using `None` for the optional audit trail, handling missing tickets explicitly, avoiding `shell=True`, validating urgency values, improving naming and documentation, and using a context manager when saving JSON data.

### 3. How did Pylint, Bandit, and Flake8 differ?

- **Pylint** identified code-quality and maintainability issues, including missing docstrings, naming problems, and the mutable default argument.
- **Bandit** identified security concerns, particularly the use of `shell=True` and the hardcoded administrator password in the original code.
- **Flake8** identified style and formatting violations, such as long lines, bare exception handling, incorrect `None` comparisons, and unused variables.

Together, these tools provided complementary views of the program.

### 4. How did static analysis improve the program, and what are its limitations?

Static analysis helped improve the program's readability, error handling, input validation, and security. The Pylint score increased from 5.53/10 to 10.00/10. However, a perfect score does not guarantee that a program is free from bugs or vulnerabilities. The program must still be tested with valid and invalid inputs, and its behavior must be reviewed manually.
