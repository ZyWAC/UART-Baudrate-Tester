# UART-Baudrate-Tester

A lightweight Python tool to brute-force test and identify the correct baudrate for UART (Universal Asynchronous Receiver/Transmitter) serial communication. Perfect for debugging embedded systems, microcontrollers, or legacy hardware with unknown communication settings.

This tool automates testing a comprehensive list of standard and specialized baudrates, sending test data and capturing responses to help you quickly determine the correct communication speed for serial devices.

## Features

- Tests a comprehensive list of standard and specialized baudrates (50 to 4,000,000)
- Detects printable ASCII responses for quick validation of correct baudrates
- Supports raw output mode to view all serial data (including non-printable characters)
- Progress bar for tracking test progress
- Cross-platform compatibility (works with Linux, macOS, and Windows serial ports)
- Simple command-line interface with intuitive options

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

Basic usage (tests with ASCII validation):
```bash
python brutRate.py -p /dev/ttyUSB0
```

Raw output mode (shows all data including non-printable characters):
```bash
python brutRate.py -a -p /dev/ttyUSB0
```

### Command Line Options

| Flag | Description |
|------|-------------|
| `-h`, `--help` | Show help message and exit |
| `-a`, `--all` | Show all raw output without ASCII filtering (up to 20 characters) |
| `-p`, `--port` | Specify serial port to test (default: `/dev/ttyUSB0`) |

### Windows Users

On Windows, serial ports are typically named like `COM3` instead of `/dev/ttyUSB0`:
```bash
python brutRate.py -p COM3
```

## How It Works

1. The script tests each baudrate in a pre-defined list of standard and specialized rates
2. For each baudrate, it:
   - Sends two carriage returns (simulating Enter key presses to trigger device responses)
   - Sends a test string (`hello\r\n`)
   - Waits for and reads any response (up to 100 bytes)
3. In normal mode:
   - Prints ASCII-readable responses immediately (strong indicator of correct baudrate)
   - Collects baudrates with non-ASCII output and reports them at the end
4. In raw mode (`-a`):
   - Shows all received data (limited to 20 characters) regardless of type, useful for non-text-based protocols

## Common Use Cases

- Identifying the correct baudrate for:
  - Embedded devices and microcontrollers
  - Arduino/ESP8266/ESP32 boards with unknown settings
  - Industrial equipment and sensors
  - Legacy hardware and retro computing systems
- Troubleshooting serial communication issues
- Reverse engineering unknown serial protocols
- Validating UART connection integrity

## Notes

- Some baudrates may not be supported by your hardware - these will be skipped automatically
- Non-printable characters in raw mode may display as special symbols depending on your terminal emulator
- Control characters (like `\r`, `\n`, `\t`) might affect terminal display in raw mode
- Testing all baudrates takes approximately 1-2 minutes (varies by system and hardware response times)
- Ensure proper electrical connections and voltage levels (typically 3.3V or 5V for UART) before testing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
