# Contributing to UK Fuel Finder Python Library

Thank you for considering contributing to this project!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ukfuelfinder.git
   cd ukfuelfinder
   ```

3. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting: `black ukfuelfinder tests`
- Use type hints for all functions
- Add docstrings to all public methods

## Testing

- Write tests for all new features
- Maintain >80% code coverage
- Run tests before submitting PR:
  ```bash
  pytest
  ```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Add tests
4. Run code quality checks:
   ```bash
   black ukfuelfinder tests
   mypy ukfuelfinder
   flake8 ukfuelfinder
   pytest
   ```
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

## Reporting Issues

- Use GitHub Issues
- Include Python version, library version, and error messages
- Provide minimal reproducible example

## Code of Conduct

Be respectful and constructive in all interactions.
