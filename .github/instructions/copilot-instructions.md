General Principles
Write clear, concise, and consistent code for web development, prioritizing modularity and readability.

Use descriptive, conventional naming for variables, functions, classes, and CSS selectors (snake_case for Python, camelCase for JavaScript, kebab-case for CSS).

Structure code and assets by feature: separate HTML, CSS, JavaScript, and Python scripts.

HTML and CSS
Organize HTML markup with semantic tags (e.g., <header>, <main>, <section>, <footer>).

Use clean, maintainable CSS; prefer classes over IDs, and group styles logically.

Avoid inline styles—keep styles in dedicated CSS files or style blocks.

Prioritize responsive design using modern CSS techniques (Flexbox, Grid).

Minimize unnecessary HTML/CSS; eliminate unused code and selectors.

Python Integration
If using Python for backend or scripting:

Follow PEP 8 for style and structure.

Decompose logic into modular functions and scripts for maintainability.

Use descriptive names and docstrings for all functions and modules.

Handle errors gracefully using try-except blocks where needed, and validate user input.

JavaScript
Place JavaScript logic in separate files; avoid inline scripts.

Write modular, reusable functions.

Use event-driven code for interactivity and DOM manipulation.

Handle errors with try-catch, and validate user or form input.

Minimize global variables; prefer closure or ES6 modules for scope control.

Project Structure
Keep a clear directory organization:

index.html, /css/styles.css, /js/scripts.js, /python/ (for scripts or backend).

Document code blocks and provide comments for complex logic.

Performance and Security
Optimize assets: minify CSS and JS for production.

Avoid unnecessary dependencies and unused code.

For backend scripts, sanitize all user input to prevent security vulnerabilities.

If applicable, follow web security practices: prevent XSS, sanitize form submissions, avoid exposing sensitive data.

Testing and Quality
Test code for cross-browser and device compatibility.

Use Python's unittest or pytest for backend scripts.

Debug JavaScript interactively; test UI responsiveness and reliability.

Key Conventions
Use "Convention Over Configuration" to reduce excess boilerplate and streamline development.

Ensure code is maintainable, modular, and secure throughout the lifecycle.

Document project setup, usage, and logic thoroughly in README.md and code comments.