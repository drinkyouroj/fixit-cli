# Quick Start Guide

Get up and running with Fix-It CLI in 2 minutes!

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# That's it! You can now run:
python fixit.py --help
```

**Note:** Requires Python 3.8 or higher.

## First Commands

### 1. Test the CLI
```bash
python fixit.py --help
```

### 2. Reset a Password
```bash
python fixit.py reset-user alice
```

### 3. Ping a Server
```bash
python fixit.py ping-test google.com
```

### 4. View Logs
```bash
# Create a test log file first
echo -e "INFO: App started\nERROR: Connection failed\nWARN: Retrying..." > test.log

# Then dump it
python fixit.py log-dump test.log
```

## Make it Global (Optional)

If you want to use `fixit` from anywhere:

```bash
pip install -e .
```

Then you can use `fixit` instead of `python fixit.py`:

```bash
fixit --help
fixit reset-user bob
```

## Development Setup

If you want to contribute or customize:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Install pre-commit hooks
pre-commit install
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try all the command options with `--help`
- Check out the [IMPROVEMENTS.md](IMPROVEMENTS.md) for enhancement ideas
- Customize the code to add your own commands!

Happy fixing! 🔧
