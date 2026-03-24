# Repository Instructions

This is a Django project called **au-realestate-tracker**.

## ⚠️ IMPORTANT REMINDERS

### Always Run Tests
- **BEFORE committing any changes**, run the full test suite:
  ```bash
  python manage.py test
  ```
- **AFTER making any code changes**, run tests to ensure nothing is broken
- Tests are critical for maintaining code quality and preventing regressions

### Always Format Code
- **BEFORE committing any changes**, format all Python files:
  ```bash
  black .
  ```
- **AFTER editing any Python files**, run black to ensure consistent formatting
- Black formatting is mandatory and enforced

## Testing

- Tests are executed using Django's test runner
- Run all tests with:
  ```bash
  python manage.py test
  ```
- Individual app tests can be run as:
  ```bash
  python manage.py test addresses
  ```

## Formatting & Style

- The project uses **black** for code formatting
- Before committing or when editing files, run:
  ```bash
  black .
  ```
- Please follow black's automatic formatting; it is the authoritative style

## General Notes

- Standard Django conventions are followed for apps, models, views, and urls
- Use the provided `manage.py` commands for migrations, running the server, and interacting with the project

## Addresses app

- Contains a simple `Address` model and administration interface
- Front‑end listing available at `/addresses/` with sorting options by date or suburb
- Anonymous visitors can add new addresses and delete existing ones via simple forms on that page
- Default `state` value is configurable via the admin under the single
  `Address configuration` object

*Copilot should help by keeping tests passing and applying black formatting when editing Python files.*
