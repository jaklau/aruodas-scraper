# aruodas bot

## Installation
Install requirements
```bash
pip install -r requirements.txt
```
Use the package manager pip to install aruodas-bot package.
```bash
pip install .
```

## Tests
Run all tests.
```bash
python -m unittest discover -s tests
```
Run single test (example).
```bash
python -m unittest tests/test_aruodas_bot.py
```

## Environment variables
Add these environment variables
C:\Development
```
HOST={database host};
DB={database name};
USER={database user name}
PASSWORD={database password};
PATH={path to chrome driver};
```