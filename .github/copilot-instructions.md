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

## Git Workflow

*   **Commit Message Review**: Always review and verify the commit message after committing to ensure it accurately describes the changes and follows the project's commit message conventions.
*   **Commit Message Format**: Commit messages must follow this structure:
    1. Title line (brief summary of changes)
    2. Blank line
    3. Dotted list of detailed changes (each change on its own line starting with `*`)
    4. Blank line
    5. Footer (sign-off and co-authorship information)
*   **Commit Signing**: Commits must be signed off via CLI using `git commit -s`.
*   **Commit Messages**: Document, language-related, or project configuration changes should be avoided in commit messages unless no code changes have been made. Focus on functional and structural changes. Avoid mentioning detailed implementation changes like variable renaming or minor refactoring details.
*   **Co-authorship**: GitHub Copilot should be credited as a co-author using `Co-authored-by: GitHub Copilot <github-copilot[bot]@users.noreply.github.com>`.
