# 🔧 Fix-It CLI: IT Support Toolkit

> Because sometimes you need to fix things, and sometimes you need to pretend you're fixing things.

A simple, practical command-line tool that mimics real-life IT support tasks. Perfect for learning automation, demonstrating support workflows, or just having a bit of fun with your terminal.

## ✨ Features

- **Password Reset** - Simulate password resets with secure password generation
- **Network Testing** - Ping hosts to test connectivity
- **Log Dumping** - View and filter log files with ease
- **Clean CLI** - Modern, user-friendly interface with helpful error messages
- **Humor Included** - Because IT support doesn't have to be boring

## 🚀 Installation

### Option 1: Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/fixit-cli.git
cd fixit-cli

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Or run directly without installation
python fixit.py --help
```

### Option 2: Direct Usage (No Installation)

```bash
# Just make sure you have Python 3.7+ and click installed
pip install click
python fixit.py --help
```

## 📖 Usage

### General Help

```bash
fixit --help
```

### Password Reset

Reset a user's password (simulated, of course):

```bash
# Basic reset with confirmation
fixit reset-user john.doe

# Force reset without confirmation
fixit reset-user john.doe --force

# Reset with email notification
fixit reset-user john.doe --email john.doe@example.com
```

**Example Output:**
```
🔐 Password Reset Request for: john.doe
────────────────────────────────────────────────────────────
Are you sure you want to reset password for 'john.doe'? [y/N]: y
Processing reset request: 100%|████████████████| 3/3

✅ Password Reset Successful!
   Username: john.doe
   New Password: Kx9#mP2$vL8q
   Reset Time: 2024-01-15 14:30:22

📧 Notification sent to: john.doe@example.com
   (In a real system, this would actually send an email)

💡 Pro Tip: Tell the user to change this password immediately!
```

### Network Ping Test

Test network connectivity to a host:

```bash
# Basic ping test
fixit ping-test google.com

# Custom ping count and timeout
fixit ping-test 8.8.8.8 --count 10 --timeout 5

# Verbose output
fixit ping-test example.com --verbose
```

**Example Output:**
```
🌐 Network Connectivity Test: google.com
────────────────────────────────────────────────────────────
✅ Host is reachable!
   4 packets transmitted, 4 received, 0% packet loss

⏱️  Test completed in 1.23 seconds
```

### Log Dump

View and filter log files:

```bash
# Show first 50 lines
fixit log-dump /var/log/app.log

# Show last 100 lines (tail)
fixit log-dump /var/log/app.log --tail --lines 100

# Filter for specific pattern
fixit log-dump /var/log/app.log --grep "ERROR"

# Save output to file
fixit log-dump /var/log/app.log --grep "WARN" --output warnings.txt

# Works with gzipped logs too!
fixit log-dump /var/log/app.log.gz --lines 200
```

**Example Output:**
```
📋 Log Dump: /var/log/app.log
────────────────────────────────────────────────────────────
📊 Showing 50 lines from head (total: 1234 lines)

   1 │ 2024-01-15 10:00:00 INFO Application started
   2 │ 2024-01-15 10:00:01 INFO Database connection established
   3 │ 2024-01-15 10:00:02 ERROR Failed to load configuration
   4 │ 2024-01-15 10:00:03 WARN Retrying connection...
   ...
```

## 🛠️ Commands Reference

| Command | Description | Options |
|---------|-------------|---------|
| `reset-user <username>` | Reset a user's password | `--force`, `--email` |
| `ping-test <host>` | Test network connectivity | `--count`, `--timeout`, `--verbose` |
| `log-dump <path>` | Dump log file contents | `--lines`, `--tail`, `--grep`, `--output` |

## 🎯 Use Cases

- **Learning Automation** - See how CLI tools are structured and built
- **Demo/Portfolio** - Showcase IT support automation skills
- **Training** - Practice common IT support workflows
- **Development** - Quick testing of support-like operations
- **Humor** - Add some fun to your terminal (because why not?)

## 🏗️ Project Structure

```
fixit-cli/
├── fixit.py              # Main CLI entry point
├── commands/             # Command implementations
│   ├── __init__.py
│   ├── reset_user.py     # Password reset logic
│   ├── ping_test.py      # Network testing logic
│   └── log_dump.py       # Log dumping logic
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## 🔧 Requirements

- Python 3.7 or higher
- `click` library (install via `pip install click`)

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Ideas for contributions:
- Add more IT support commands
- Improve error handling
- Add configuration file support
- Create installers for different platforms
- Add more humor to help messages

## 📝 License

MIT License - feel free to use this project however you'd like!

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) - the Python CLI framework
- Inspired by real IT support workflows (and the occasional need to look busy)

## 💬 Support

Having issues? Found a bug? Want to suggest a feature?

- Open an issue on GitHub
- Check existing issues first
- Be nice (we're all here to learn and have fun)

---

**Remember**: This is a simulation tool. It doesn't actually reset passwords or modify systems. Use responsibly and have fun! 🎉
