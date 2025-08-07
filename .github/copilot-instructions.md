# Coding Guidelines for PyGVAS

This document outlines the coding standards for the PyGVAS project. Adhering to these guidelines ensures consistency and readability across the codebase.

## General Formatting

*   **Line Length**: Maximum line length of 80 characters.
*   **Blank Lines**: A maximum of one blank line should be used for separation, except where specified otherwise for Python code.
*   **Comments**: Do not add comments unless specifically requested.
*   **Documentation**: Use a third-person voice and describe what the code does, not what the developer is expected to do.
*   **Language**: Use British English (en-GB) spelling and conventions throughout the codebase.

## Markdown Style

*   **Spacing**: Ensure that there is a blank line between headings and paragraphs, and also between headings of different levels.

## Python-Specific Style

### Code Structure

*   **Blank Lines**: Use two blank lines between file-level declarations (e.g., classes, functions). An exception is for grouped variable declarations, which should not have blank lines between them.
*   **Comprehensions**: Use list/dictionary comprehensions or generator expressions for creating sequences where possible. When a comprehension is split across multiple lines, each `for` and `if` clause must be on its own line.

### Data Structures and Formatting

*   **Lists and Dictionaries**: When a list or dictionary literal contains more than one element, it must be split across multiple lines, with each element or key-value pair on its own line with a trailing comma. Single-element lists and dictionaries are the only exception and should be on a single line.
*   **Tuples**: Avoid enclosing tuples in parentheses when not required for clarity or precedence. Tuple assignment without parentheses is preferred where possible.
*   **Function Parameters**: Function parameters must follow consistent formatting - either all parameters on a single line, or each parameter on its own separate line. Never mix parameters across multiple lines inconsistently. When split across multiple lines, each parameter must be on its own line with a trailing comma after the last parameter. When breaking down parameters to fit the line length limit, always prioritise chopping down function parameters over breaking arithmetic/logical expressions within parameters.
*   **Variable Declarations**: Avoid declaring unnecessary variables that are only used once, except when the variable stores the result of a function call that may not be stateless or when it significantly improves readability. Variables should only be inlined automatically if the operation is known to be idempotent, or otherwise require confirmation before inlining.

### Class Design

*   **Class Organisation**: Classes must follow this exact order:
    1. `__slots__` declaration (always at the top)
    2. Class variables
    3. Type hints for instance variables
    4. Static methods
    5. Class methods
    6. Properties (using `@property` decorator and associated setters/deleters)
    7. Instance methods
*   **Member Ordering Rules**: All class members follow consistent ordering principles:
    *   **Visibility Order**: Public members first, then protected members (prefixed with `_`)
    *   **Alphabetical Sorting**: Within each visibility level, sort members alphabetically
    *   **Built-in Priority**: For methods, built-in method overrides come before custom methods within each method type
*   **Assignment Type Analysis**: Before rearranging code, always analyse the type of assignment to distinguish between variable declarations, function assignments, and type assignments. Functions assigned to identifiers should be treated as function definitions and placed in the appropriate method section. Type assignments should be placed in the class variables section.
*   **`__slots__`**:
    *   Always declare `__slots__` to predefine instance variables.
    *   For classes with no instance variables, use `__slots__ = ()`.
    *   In `__slots__`, each member should be on a separate line unless the tuple is empty.
*   **Type Hinting**: Always add class-level type hints for all instance variables declared in `__slots__`. Type hints must follow the same order as the `__slots__` declaration.

### Method Design

*   **Private Methods**: Single underscore prefix (`_method_name`) indicates methods intended for internal use within the class or module.
*   **Return Types**: Return types must be specified in method signatures, including `-> None` for methods that don't return a value.
*   **Method Parameters**: Type hints are required for all parameters.

### Naming Conventions

*   **File Names**: Use snake_case for file names (e.g., `gvas_header.py`).
*   **Class Names**: Use PascalCase for class names. Acronyms should be fully capitalised (e.g., `GVASHeader`, `XMLParser`, `HTTPClient`).
*   **Variable and Function Names**: Use snake_case for variable names, function names, and method names (e.g., `save_version`, `parse_data`, `get_customs`).
*   **Protected Methods**: Prefix protected methods with a single underscore (e.g., `_internal_method`).

## File Revision Requirements

*   **Post-Action Review**: After completing any modifications, always review and revise all edited files to ensure they conform to these coding guidelines.
*   **Compliance Verification**: Verify that all changes adhere to the formatting rules, naming conventions, class organisation principles, and other style requirements.
*   **Consistency Check**: Ensure consistency across all modified files, particularly for formatting patterns, naming conventions, and structural organisation.
*   **Error Correction**: Address any deviations from the established guidelines before finalising the changes.

## Examples

### Data Structure Formatting

**Dictionary formatting:**

```python
return {
    "key1": value1,
    "key2": value2,
    "key3": value3,
}
```

**List formatting:**

```python
values = [
    item1,
    item2,
    item3,
]
```

**Function parameters - single line:**

```python
def simple_function(first_parameter: str, second_parameter: int) -> bool:
    return True
```

**Function parameters - multi-line (one per line with trailing comma):**

```python
def complex_function(
    first_parameter: str,
    second_parameter: int,
    third_parameter: list[str],
) -> bool:
    return True
```

**Function calls - multi-line:**

```python
result = some_function(
    argument1,
    argument2,
    argument3,
)
```

**Avoid mixing parameters across lines:**

```python
# INCORRECT - mixed formatting
def bad_function(first_parameter: str, second_parameter: int,
                 third_parameter: list[str]) -> bool:
    return True

# CORRECT - choose one style consistently
def good_function(
    first_parameter: str,
    second_parameter: int,
    third_parameter: list[str],
) -> bool:
    return True
```

### Class with `__slots__` and Type Hints

```python
class ExampleClass:
    __slots__ = (
        "_field1",
        "_field2",
        "_field3",
    )

    CLASS_CONSTANT = "example"

    _field1: str
    _field2: int
    _field3: list[str]

    @staticmethod
    def utility_function(value: str) -> str:
        return value.upper()

    @classmethod
    def create_default(cls) -> Self:
        obj = cls.__new__(cls)
        obj._field1 = "default"
        obj._field2 = 0
        obj._field3 = []
        return obj

    @property
    def field1(self) -> str:
        return self._field1

    @field1.setter
    def field1(self, value: str) -> None:
        self._field1 = value

    def process_data(self) -> None:
        self._field1 = self.utility_function(self._field1)
```

### Method with Type Hints

```python
def _read_multiple_values(self, count: int) -> list[int]:
    values = []
    for _ in range(count):
        value = self._read_single_value()
        values.append(value)
    return values
```

### Comprehension Usage

**Preferred:**

```python
filtered_items = [
    item.process()
    for item in items
    if item.is_valid()
]
```

**Instead of:**

```python
filtered_items = []
for item in items:
    if item.is_valid():
        filtered_items.append(item.process())
```

## Git Workflow

*   **Commit Message Review**: Always review and verify the commit message after committing to ensure it accurately describes the changes and follows the project's commit message conventions.
*   **Commit Message Format**: Commit messages must follow this structure:
    1. Title line (brief summary of changes)
    2. Blank line
    3. Dotted list of detailed changes (each change on its own line starting with `*`)
    4. Blank line
    5. Footer (sign-off and co-authorship information)
*   **Commit Signing**: Commits must be signed off via CLI using `git commit -s`.
*   **Commit Messages**: Document or language-related changes should be avoided in commit messages unless no code changes have been made. Focus on functional and structural changes.
*   **Co-authorship**: GitHub Copilot should be credited as a co-author using `Co-authored-by: GitHub Copilot <github-copilot[bot]@users.noreply.github.com>`.
