# Python Watch Meeting Script

Python 3.7+ implementation of the watch-meeting script for managing multi-agent meeting coordination.

## Features

- ✅ **Pure Python** - Uses only standard library (no external dependencies)
- ✅ **Cross-platform** - Works on Windows, Linux, and macOS
- ✅ **Python 3.7+** - Compatible with Python 3.7 and newer
- ✅ **Colored output** - ANSI color support for better readability
- ✅ **Full feature parity** - Same functionality as PowerShell, Node.js, and Deno versions

## Installation

No installation required! The script uses only Python standard library modules.

### Requirements

- Python 3.7 or higher

### Verify Python Version

```bash
python --version
# or
python3 --version
```

## Usage

### Basic Usage

```bash
# Monitor a meeting file
python watch-meeting.py --persona "Agent-Name" --meeting-file "../../active/meeting.md"

# Or using short flags
python3 watch-meeting.py -p "Agent-Name" -f "../../active/meeting.md"
```

### Post a Message

```bash
python watch-meeting.py --persona "DevOps-Engineer" \
  --meeting-file "../../active/meeting.md" \
  --message "Your message here"
```

### End a Meeting

```bash
python watch-meeting.py --persona "Moderator" \
  --meeting-file "../../active/meeting.md" \
  --end-meeting
```

### Fetch Current Content

```bash
python watch-meeting.py --persona "Agent-Name" \
  --meeting-file "../../active/meeting.md" \
  --fetch
```

### Show Help

```bash
python watch-meeting.py --help
```

## Command Line Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--persona` | `-p` | ✅ | Agent persona name |
| `--meeting-file` | `-f` | ❌ | Path to meeting file (default: "meetings/meeting.md") |
| `--message` | `-m` | ❌ | Message to post to the meeting |
| `--context-messages` | `-c` | ❌ | Number of recent messages to display (default: 5) |
| `--end-meeting` | `-e` | ❌ | Flag to end the meeting (sets Status to COMPLETE) |
| `--fetch` | | ❌ | Fetch current content without monitoring |
| `--help` | `-h` | ❌ | Show help message |

## Examples

### Example 1: Join a Meeting

```bash
# From the python directory
python watch-meeting.py -p "Backend-Architect" -f "../../active/vscode-extension.md"
```

### Example 2: Post Multiple Messages

```bash
# Post a message
python watch-meeting.py -p "Tech-Lead" -f "../../active/meeting.md" -m "I recommend using TypeScript for type safety."

# Script automatically monitors after posting
# When changes detected, evaluate and respond again if needed
python watch-meeting.py -p "Tech-Lead" -f "../../active/meeting.md" -m "We should also consider ESLint configuration."
```

### Example 3: Check Meeting Status

```bash
# Fetch without monitoring (quick status check)
python watch-meeting.py -p "Product-Manager" -f "../../active/meeting.md" --fetch
```

### Example 4: Close a Meeting

```bash
# Moderator ends the meeting
python watch-meeting.py -p "Product-Manager" -f "../../active/meeting.md" --end-meeting
```

## Making the Script Executable (Linux/macOS)

```bash
# Make executable
chmod +x watch-meeting.py

# Run directly
./watch-meeting.py --persona "Agent-Name" --meeting-file "../../active/meeting.md"
```

## Windows Usage

### Using Python Launcher

```powershell
# If you have Python installed via python.org installer
py watch-meeting.py --persona "Agent-Name" --meeting-file "..\..\active\meeting.md"
```

### Direct Python Command

```powershell
python watch-meeting.py --persona "Agent-Name" --meeting-file "..\..\active\meeting.md"
```

## Script Behavior

The Python script follows the same protocol as all other implementations:

1. **Validation**: Checks if meeting file exists
2. **Operation Mode**:
   - `--end-meeting`: Updates Status to COMPLETE and exits
   - `--message`: Appends timestamped message to meeting file
   - `--fetch`: Displays current content and exits
   - Default: Monitors for file changes
3. **Monitoring Loop**:
   - Checks initial Status (exits if COMPLETE)
   - Polls file modification time every 0.5 seconds
   - Detects changes and displays recent messages
   - Exits if Status changed to COMPLETE
   - 5-minute timeout to prevent infinite waiting

## Troubleshooting

### Module Not Found Errors

This script uses only standard library modules. If you get import errors:

```bash
# Verify Python version (needs 3.7+)
python --version

# Try python3 explicitly
python3 watch-meeting.py --help
```

### File Path Issues

Use appropriate path separators for your OS:

```bash
# Linux/macOS
python watch-meeting.py -p "Agent" -f "../../active/meeting.md"

# Windows
python watch-meeting.py -p "Agent" -f "..\..\active\meeting.md"
```

Or use forward slashes which work on all platforms:

```bash
python watch-meeting.py -p "Agent" -f "../../active/meeting.md"
```

### Encoding Issues

The script uses UTF-8 encoding explicitly. If you see encoding errors:

```bash
# Set UTF-8 environment (Linux/macOS)
export PYTHONIOENCODING=utf-8

# Windows PowerShell
$env:PYTHONIOENCODING = "utf-8"
```

## Comparison with Other Versions

| Feature | Python | PowerShell | Node.js | Deno |
|---------|--------|------------|---------|------|
| Setup Required | ❌ None | ❌ None | ✅ npm install | ❌ None |
| External Dependencies | ❌ None | ❌ None | ✅ Yes (tsx, @types/node) | ❌ None |
| Python Version | 3.7+ | N/A | N/A | N/A |
| Cross-platform | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Colored Output | ✅ ANSI | ✅ Built-in | ✅ ANSI | ✅ ANSI |
| Type Safety | ❌ Dynamic | ❌ Dynamic | ✅ TypeScript | ✅ TypeScript |
| Best For | Python projects | Windows default | Node.js ecosystem | Modern TS runtime |

## License

MIT
