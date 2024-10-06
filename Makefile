format:
	. venv/bin/activate && find . -type f -name "*.py" ! -path "./venv/*" | xargs ruff format
