# Coding Guidelines for PyGVAS

This document outlines the coding standards for the PyGVAS project. Adhering to these guidelines ensures consistency and readability across the codebase.

## General Formatting

*   **Comments**: Do not add comments unless specifically requested.
*   **Documentation**: Use a third-person voice and describe what the code does, not what the developer is expected to do.
*   **Language**: Use British English (en-GB) spelling and conventions throughout the codebase.

## Markdown Style

*   **Spacing**: Ensure that there is a blank line between headings and paragraphs, and also between headings of different levels.

## Python Code

Python code formatting and style rules are handled by Ruff. Refer to the Ruff configuration in the project for specific formatting rules.

### Naming Conventions

*   **File Names**: Use snake_case for file names. Prefix private modules with an underscore (e.g., `_private_module.py`).
*   **Class Names**: Use PascalCase for class names (e.g., `MyClassName`).
*   **Function and Variable Names**: Use snake_case for function and variable names. Prefix protected methods with an underscore (e.g., `_protected_method`). Consider semantic meaning: variables assigned functions should follow function naming conventions, and variables assigned classes should follow class naming conventions.

### Code Structure and Organisation

*   **Variable and Function Ordering**: All variables should come before all functions, regardless of type or visibility.
*   **Member Ordering**: Within variables and functions separately, group by type in the following order:
    1. Static variables/methods
    2. Class variables/methods
    3. Instance variables/methods
*   **Visibility Grouping**: Within each type group, order by visibility:
    1. Built-in methods (e.g., `__init__`, `__str__`)
    2. Public variables/methods
    3. Protected variables/methods (prefixed with `_`)
*   **Lexicographical Sorting**: Sort variables and methods alphabetically within their respective groups.
*   **Import Management**: Always strip unused imports from files.
*   **Import Sorting**: Sort imports in the following order:
    1. Standard library imports
    2. Third-party library imports
    3. Relative imports
    Within each group, `import` statements should come before `from ... import` statements. Each import group should be separated by exactly one blank line. Additionally, when importing multiple symbols from a single module (e.g., `from module import A, B, C`), sort the imported symbols lexicographically.
*   **Module Export Dependencies**: When exporting types from a module's `__init__.py`, ensure that any related types referenced by exported types are also exported. This includes base classes, metadata classes, and any other types that are part of the public API contract for the exported types.
*   **Blank Line Formatting**: Each declaration block (functions, groups of variables, classes) should have exactly two blank lines in between. Other than this, a maximum of one blank line should be ensured. No blank line should be allowed after the initial line of function or class definition.
*   **Slots Definition**: Always define `__slots__` for classes to optimise memory usage and attribute access.

### Type Annotations

*   **Comprehensive Type Hints**: Add appropriate type hints to all declarations except `cls` in class methods and `self` in instance methods.
*   **Special Method Annotations**: For methods like `__new__` that are actually static methods, annotate the `cls` parameter appropriately.
*   **Class Variable Annotations**: Annotate class variables with `Final` by default, but use `ClassVar` when the variable is intended to be overridden in subclasses.
*   **Modern Annotations**: Use modern and future annotations syntax. This project is built upon Python 3.13 and should maintain compatibility with future releases.

### Method Decorators and Implementation

*   **Decorator Ordering**: When multiple decorators are applied to a method, follow this ordering (from top to bottom):
    1. Other decorators
    2. `@classmethod` or `@staticmethod`
    3. `@final`
    4. `@override`
    5. `@abstractmethod`
*   **Final and Override Decorators**: Apply `@final` and `@override` decorators to concrete methods where appropriate.
*   **Abstract Method Implementation**: For abstract methods, raise `NotImplementedError` with the class name as the parameter.

### Code Quality and Review

*   **Code Formatting**: Run Ruff before finalising any actions to ensure code formatting compliance.
*   **Code Review**: Review all modified files according to these coding guidelines before finalising any actions.

## Git Workflow

*   **Commit Signing**: Commits must be signed off via CLI using `git commit -s`.
*   **Commit Message Format**: Commit messages must follow this structure:
    1. Title line (brief summary of changes)
    2. Blank line
    3. Dotted list of detailed changes (each change on its own line starting with `*`)
    4. Blank line
    5. Footer (sign-off and co-authorship information)
*   **Commit Message Content**: Focus on functional and structural changes. Avoid mentioning detailed implementation changes like variable renaming or minor refactoring details. Document, language-related, or project configuration changes should be avoided unless no code changes have been made.
*   **Commit Message Review**: Always review and verify the commit message after committing to ensure it accurately describes the changes and follows these conventions.
*   **Co-authorship**: GitHub Copilot should be credited as a co-author using `Co-authored-by: GitHub Copilot <github-copilot[bot]@users.noreply.github.com>`.
