# UART-Baudrate-Tester

A lightweight Python tool to brute-force test and identify the correct baudrate for UART (Universal Asynchronous Receiver/Transmitter) serial communication. Perfect for debugging embedded systems, microcontrollers, or legacy hardware with unknown communication settings.

This tool automates testing a comprehensive list of standard and specialized baudrates, sending test data and capturing responses to help you quickly determine the correct communication speed for serial devices.

## Features

- Tests a comprehensive list of standard and specialized baudrates (50 to 4,000,000), sorted by common usage priority for faster results
- Detects printable ASCII responses for quick validation of correct baudrates
- Supports raw output mode to view all serial data (including non-printable characters)
- Progress bar for tracking test progress
- Cross-platform compatibility (works with Linux, macOS, and Windows serial ports)
- **Enhanced configuration options**:
  - Custom serial parameters (data bits: 5/6/7/8; parity: none/even/odd/mark/space; stop bits: 1/1.5/2)
  - Custom commands to send to the target device (supports multiple commands)
  - Configurable response timeout
- Serial port discovery utility (`--list-ports`)
- Results logging to a file with timestamps and hexadecimal response representations
- Multiple output modes: verbose (default), quiet (only final summary), and raw (all output)

## Requirements

- Python 3.6+
- pyserial (for serial port communication)
- tqdm (for progress bar visualization)

See `requirements.txt` for specific version information.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/UART-Baudrate-Tester.git
   cd UART-Baudrate-Tester
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python brutRate.py [OPTIONS]
```

### Command Line Options

| Flag | Description |
|------|-------------|
| `-h`, `--help` | Show help message and exit |
| `-a`, `--all` | Show all raw output including non-ASCII responses |
| `-p`, `--port` | Specify serial port to test (default: `/dev/ttyUSB0`) |
| `--list-ports` | List all available serial ports and exit |
| `-d`, `--data-bits` | Number of data bits (5,6,7,8) (default: 8) |
| `--parity` | Parity type (none, even, odd, mark, space) (default: none) |
| `-s`, `--stop-bits` | Number of stop bits (1, 1.5, 2) (default: 1) |
| `-c`, `--command` | Custom command to send (can specify multiple times, e.g., `-c "AT\r" -c "hello\r\n"`) |
| `-t`, `--timeout` | Response timeout in seconds (default: 1.0) |
| `-o`, `--output` | Save results to specified log file |
| `-q`, `--quiet` | Quiet mode - only show final results summary |

### Platform Notes

#### Windows Users
On Windows, serial ports are typically named like `COM3` instead of `/dev/ttyUSB0`:
```bash
python brutRate.py -p COM3
```

### Examples

List all available serial ports:
```bash
python brutRate.py --list-ports
```

Basic usage (tests with ASCII validation):
```bash
python brutRate.py -p /dev/ttyUSB0
```

Test with custom serial parameters:
```bash
python brutRate.py -p /dev/ttyUSB1 -d 8 --parity even -s 1 -t 2.0
```

Send custom AT commands and save results:
```bash
python brutRate.py -p COM3 -c "AT\r" -c "AT+VERSION\r" -o test_results.txt
```

Raw output mode (shows all data including non-printable characters):
```bash
python brutRate.py -a -p /dev/ttyUSB0
```

Run in quiet mode with extended timeout:
```bash
python brutRate.py -p /dev/ttyUSB0 -t 2.5 -q
```

## How It Works

1. The script tests each baudrate in a pre-defined list (sorted by common usage priority)
2. For each baudrate, it:
   - Configures the serial port with specified parameters (data bits, parity, stop bits)
   - Sends configured test commands (default: `\r\n\r\n` and `hello\r\n`; custom commands with `-c`)
   - Waits for and reads any response (up to 100 bytes) with the specified timeout
3. In normal mode:
   - Prints ASCII-readable responses immediately (strong indicator of correct baudrate)
   - Collects baudrates with non-ASCII output and reports them at the end
   ![NormalMode](https://github.com/ZyWAC/UART-Baudrate-Tester/blob/c9e152daaf66998bcb0573ef93a713457ba8e2ed/images/NormalMode.png)
4. In raw mode (`-a`):
   - Shows all received data (limited to 20 characters) regardless of type, useful for non-text-based protocols or noisy output
   ![-a Mode](https://github.com/ZyWAC/UART-Baudrate-Tester/blob/c9e152daaf66998bcb0573ef93a713457ba8e2ed/images/-aMode.png)

## Common Use Cases

- Identifying the correct baudrate for:
  - Embedded devices and microcontrollers
  - Arduino/ESP8266/ESP32 boards with unknown settings
  - Industrial equipment and sensors
  - Legacy hardware and retro computing systems
- Troubleshooting serial communication issues
- Reverse engineering unknown serial protocols
- Validating UART connection integrity

## Output Explanation

- `✅` Indicates baudrates with valid ASCII responses (most likely correct)
- `🔍` Shows raw output for non-ASCII responses (when using `-a` flag)
- `⚠️` Marks errors encountered during testing

The final summary provides:
- Total number of tested baudrates
- Count of valid responses
- Error count
- Detailed list of ASCII responses sorted by response length
- Overview of non-ASCII responses (unless in raw mode)


## Notes

- Some baudrates may not be supported by your hardware - these will be skipped automatically
- Non-printable characters in raw mode may display as special symbols depending on your terminal emulator
- Control characters (like `\r`, `\n`, `\t`) might affect terminal display in raw mode
- Testing all baudrates takes approximately 1-2 minutes (varies by system and hardware response times)
- Ensure proper electrical connections and voltage levels (typically 3.3V or 5V for UART) before testing
- Log files include timestamps, hexadecimal response representations, and decoded data for later analysis


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
