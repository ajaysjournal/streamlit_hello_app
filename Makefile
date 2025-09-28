# Makefile for Streamlit Hello App

.PHONY: help install install-dev run test lint format clean build

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install with development dependencies
	pip install -e ".[dev]"

# Running
run: ## Run the Streamlit application
	streamlit run src/streamlit_hello_app/main.py

run-simple: ## Run using the simple launcher script
	streamlit run run_app.py

run-package: ## Run using the package script
	streamlit-app

# Development
test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src/streamlit_hello_app --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	pytest-watch

# Code quality
lint: ## Run linting
	flake8 src/ tests/
	mypy src/

format: ## Format code
	black src/ tests/
	isort src/ tests/

format-check: ## Check code formatting
	black --check src/ tests/
	isort --check-only src/ tests/

# Pre-commit
install-hooks: ## Install pre-commit hooks
	pre-commit install

hooks: ## Run pre-commit hooks
	pre-commit run --all-files

# Building
build: ## Build the package
	python -m build

build-clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# Cleaning
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage

clean-all: build-clean clean ## Clean everything including build artifacts

# Documentation
docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

# Virtual environment
venv: ## Create virtual environment
	python -m venv venv
	@echo "Activate with: source venv/bin/activate"

# Dependencies
deps: ## Show dependency information
	pip list
	pip show streamlit-hello-app

# Environment
env: ## Copy environment example file
	cp env.example .env
	@echo "Edit .env file with your configuration"

# Quick setup for new developers
setup: venv install-dev install-hooks env ## Complete setup for new developers
	@echo "Setup complete! Activate virtual environment with: source venv/bin/activate"

# CI/CD helpers
ci-test: format-check lint test ## Run all CI checks
