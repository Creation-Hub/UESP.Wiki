# Python
This document explains how to setup Python for this project.



## Prerequisites
Before starting, ensure you have:
- Python 3.13 or higher installed

Verify your Python version:
```shell
python --version
```



## Virtual Environment (venv)
This project uses `venv` to create a virtual Python environment.

This is the one-time initial setup command.
```shell
python -m venv .venv
```

Ensure the Python environment is activated when working on the project.
The VS Code terminal will be prefixed with `(.venv)`.
```shell
# Windows
.venv\Scripts\activate
```



## Packages (pyproject)
The package dependencies managed by `pyproject` for this project.


### Install Packages
Installs the project source to the `venv` virtual environment as an editable package.
The `source/testing` module code is NOT installed.


#### Option 1
Or, install everything at once from root `pyproject.toml` configuration.
```shell
pip install -e .
```

Optionally install the `dev` configuration to support the Python package `build` command.
```shell
pip install -e .[dev]
```


#### Option 2
Install individual packages in development mode.
```shell
pip install -e source/sharp
pip install -e source/papyrus
pip install -e source/wiki
pip install -e source/scribe
```


### Verify Installation
After installing packages, verify everything works:
```shell
# Test the scribe command is available
scribe --help

# Verify all packages are installed
pip list | findstr -i "scribe sharp papyrus wiki"
```

**VS Code can't find modules:**
- Ensure VS Code is using the correct Python interpreter
- Check that `.venv` is activated in VS Code terminal.
- Restart VS Code after installing packages.



## Development Workflow
Some developer workflows to use.


### Adding New Dependencies
If a new dependency is added to a package:
1. Add to the appropriate `pyproject.toml` file.
2. Reinstall the package: `pip install -e source/[package]`.
3. Update documentation if needed.


### Package Dependency Changes
If dependencies between packages are modified:
1. Update `pyproject.toml` dependencies list.
2. Reinstall affected packages in dependency order.
3. Test imports work correctly.
