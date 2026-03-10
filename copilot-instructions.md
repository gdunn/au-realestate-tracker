# Repository Instructions

This is a Django project called **au-realestate-tracker**.

## Testing

- Tests are executed using Django's test runner.
- Run all tests with:
  ```bash
  python manage.py test
  ```
- Individual app tests can be run as:
  ```bash
  python manage.py test addresses
  ```

## Formatting & Style

- The project uses **black** for code formatting.
- Before committing or when editing files, run:
  ```bash
  black .
  ```
- Please follow black's automatic formatting; it is the authoritative style.

## General Notes

- Standard Django conventions are followed for apps, models, views, and urls.
- Use the provided `manage.py` commands for migrations, running the server, and interacting with the project.

*Copilot should help by keeping tests passing and applying black formatting when editing Python files.*
