# Lab 5: Static Code Analysis — Issues Report

| **Issue** | **Type** | **Line(s)** | **Description** | **Fix Approach** |
|---|---|---|---|---|
| Shell command injection risk | Security — High | 38 | `subprocess.call()` uses `shell=True` with a hostname concatenated into a command string. A malicious hostname could execute unintended shell commands. | Use `subprocess.run()` with a list of arguments and `shell=False`. Validate the hostname and handle errors. |
| Mutable default argument | Bug / Reliability | 10 | `audit_trail=[]` creates a shared mutable default list that can retain data across function calls. | Change the default to `None` and initialize a new list when needed. |
| Missing urgency validation | Bug | 48–49 | Urgency values outside 1–5 are accepted, and non-numeric input causes a `ValueError`. | Validate that urgency is an integer from 1 to 5 and reprompt when the input is invalid. |
| Bare exception | Reliability / Security | 23–24 | `except:` catches all exceptions and silently ignores errors, including unexpected failures. | Catch the expected `KeyError` and handle nonexistent ticket IDs explicitly. |
| Hardcoded administrator password | Security | 8 | The administrator password is stored directly in the source code, exposing the credential to anyone who can read it. | Load the credential from a protected environment variable or secure configuration. |
| Missing module and function docstrings | Code quality | 1, 10, 17, 20, 26, 30, 37, 40, 45 | Missing documentation makes the program harder to understand and maintain. | Add a module docstring and concise docstrings for each function. |
| Incorrect naming conventions | Style | 7, 30 | `ticket_counter` and `unresolvedHighPriority` do not follow Pylint naming conventions. | Use a suitable uppercase constant for a true constant and `unresolved_high_priority` for the function. |
| Unsafe file-handling pattern | Reliability | 41–43 | The file is opened without a context manager or explicit encoding. | Use `with open(file, "w", encoding="utf-8")` to ensure proper resource cleanup. |
| Unused variable | Code quality | 47 | `t2` is assigned a ticket ID but never used. | Remove the unused assignment or use the variable meaningfully. |
| Inconsistent formatting | Style | 13–14, 52, throughout | Long lines, insufficient blank lines, and other PEP 8 violations make the code less readable. | Split long statements, add appropriate blank lines, and rerun Flake8. |
| Incorrect `None` comparison | Style / Correctness | 33 | Comparing a value with `== None` violates recommended Python style. | Replace the comparison with `is None`. |

## Summary

The original Pylint score was **5.53/10**. Bandit identified one high-severity issue (`B602`) and three low-severity findings (`B404`, `B105`, and `B110`). Flake8 reported style violations, including `E722`, `E711`, `E501`, and `F841`.

The goal is to fix the identified issues, preserve the helpdesk ticketing functionality, and rerun all three tools to verify the improvements.