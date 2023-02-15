# Define the Python interpreter to use
PYTHON_INTERPRETER = python3

# Define the name of the requirements file
REQUIREMENTS_FILE = requirements.txt

# Define the name of the main script
MAIN_SCRIPT = main.py

# Define the name of the output file
OUTPUT_FILE = output.txt

# Define the default target
.DEFAULT_GOAL := help

# Display the help message
help:
	@echo "Available targets:"
	@echo "  test             Run the unit tests"
	@echo "  lint             Run the linter"
	@echo "  format           Format the code using black"
	@echo "  check-format     Check the code formatting using black"
	@echo "  check-style      Check the code style using flake8"
	@echo "  check-types      Check the type annotations using mypy"


# Run the unit tests
test:
	$(PYTHON_INTERPRETER) -m pytest tests/functional/src/

# Run the linter
lint:
	$(PYTHON_INTERPRETER) -m flake8 src --ignore=E501

# Format the code using black
format:
	$(PYTHON_INTERPRETER) -m isort .
	$(PYTHON_INTERPRETER) -m black .

# Check the code formatting using black
check-format:
	$(PYTHON_INTERPRETER) -m black --check .

# Check the code style using flake8
check-style:
	$(PYTHON_INTERPRETER) -m flake8

# Check the type annotations using mypy
check-types:
	$(PYTHON_INTERPRETER) -m mypy .

