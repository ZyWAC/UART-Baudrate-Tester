import serial
import time
from tqdm import tqdm
import argparse
import sys
from serial.tools.list_ports import comports
from datetime import datetime
import os

# Author: ZyWAC
# UART Baudrate Tester - Enhanced version with custom parameters

# Baudrates sorted by priority (common rates first)
baudrates = [
    9600, 115200, 57600, 38400, 19200, 2400, 4800, 31250,  # Common rates
    1200, 230400, 460800, 921600, 1000000, 2000000, 4000000,  # High speed
    50, 75, 110, 134, 135, 150, 200, 300, 600, 1800, 3600, 7200,  # Low speed
    14400, 28800, 56000, 76800, 115700, 125000, 128000, 250000, 256000,
    500000, 512000, 600000, 750000, 1152000, 1382400, 1500000, 3686400, 3000000
]

def list_available_ports():
    """List all available serial ports"""
    ports = comports()
    if not ports:
        print("No available serial ports found.")
        return
    print("Available serial ports:")
    for port in ports:
        desc = port.description if port.description else "No description"
        print(f"  - {port.device}: {desc}")

def is_ascii_printable(data):
    """Check if data contains only printable ASCII characters"""
    try:
        text = data.decode('ascii')
        return all(32 <= ord(c) <= 126 or c in '\r\n\t' for c in text)
    except UnicodeDecodeError:
        return False

def test_baudrate(ser, baudrate, test_commands, timeout, raw_mode):
    """Test a single baudrate and return response info"""
    try:
        ser.baudrate = baudrate
        ser.timeout = timeout
        ser.flushInput()
        ser.flushOutput()

        # Send all test commands
        for cmd in test_commands:
            ser.write(cmd)
            time.sleep(0.3)  # Short delay between commands

        # Read response
        response = ser.read(100)
        if not response:
            return None

        # Process response
        is_ascii = is_ascii_printable(response)
        decoded = response.decode('latin-1', errors='replace') if raw_mode else \
                  response.decode('ascii', errors='replace').strip()
        
        return {
            'baudrate': baudrate,
            'response': response,
            'is_ascii': is_ascii,
            'decoded': decoded,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except serial.SerialException as e:
        return {'error': f"Serial error: {str(e)}", 'baudrate': baudrate}
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}", 'baudrate': baudrate}

def save_results(results, output_file):
    """Save test results to a log file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"UART Baudrate Test Results - {datetime.now()}\n")
        f.write("========================================\n\n")
        for res in results:
            if 'error' in res:
                f.write(f"[{res['timestamp']}] Baudrate {res['baudrate']}: ERROR - {res['error']}\n")
            else:
                f.write(f"[{res['timestamp']}] Baudrate {res['baudrate']}:\n")
                f.write(f"  Type: {'ASCII' if res['is_ascii'] else 'Non-ASCII'}\n")
                f.write(f"  Response (hex): {res['response'].hex()}\n")
                f.write(f"  Decoded: {res['decoded'][:100]}\n\n")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Enhanced UART baudrate brute-force tester')
    parser.add_argument('-a', '--all', action='store_true', 
                      help='Show all raw output (including non-ASCII)')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0', 
                      help='Serial port to test (default: /dev/ttyUSB0)')
    parser.add_argument('--list-ports', action='store_true', 
                      help='List all available serial ports and exit')
    parser.add_argument('-d', '--data-bits', type=int, default=8, choices=[5,6,7,8],
                      help='Number of data bits (default: 8)')
    parser.add_argument('--parity', default='none', choices=['none', 'even', 'odd', 'mark', 'space'],
                      help='Parity type (default: none)')
    parser.add_argument('-s', '--stop-bits', type=float, default=1, choices=[1, 1.5, 2],
                      help='Number of stop bits (default: 1)')
    parser.add_argument('-c', '--command', action='append', 
                      help='Custom command to send (can specify multiple, e.g., -c "AT\r" -c "hello\r\n")')
    parser.add_argument('-t', '--timeout', type=float, default=1.0, 
                      help='Response timeout in seconds (default: 1.0)')
    parser.add_argument('-o', '--output', 
                      help='Save results to specified log file')
    parser.add_argument('-q', '--quiet', action='store_true', 
                      help='Quiet mode (only show final results)')
    args = parser.parse_args()

    # Handle port listing
    if args.list_ports:
        list_available_ports()
        return

    # Prepare test commands
    default_commands = [b'\r\n\r\n', b'hello\r\n']
    if args.command:
        # Convert user commands to bytes (utf-8 encoded)
        test_commands = [cmd.encode('utf-8') for cmd in args.command]
    else:
        test_commands = default_commands

    # Map parity to pyserial constants
    parity_map = {
        'none': serial.PARITY_NONE,
        'even': serial.PARITY_EVEN,
        'odd': serial.PARITY_ODD,
        'mark': serial.PARITY_MARK,
        'space': serial.PARITY_SPACE
    }
    parity = parity_map[args.parity]

    # Map data bits to pyserial constants
    data_bits_map = {
        5: serial.FIVEBITS,
        6: serial.SIXBITS,
        7: serial.SEVENBITS,
        8: serial.EIGHTBITS
    }
    data_bits = data_bits_map[args.data_bits]

    # Initialize serial port
    try:
        ser = serial.Serial(
            port=args.port,
            timeout=args.timeout,
            bytesize=data_bits,
            parity=parity,
            stopbits=args.stop_bits,
            rtscts=False,
            dsrdtr=False
        )
    except serial.SerialException as e:
        print(f"Failed to open port {args.port}: {str(e)}")
        sys.exit(1)

    # Run tests
    results = []
    ascii_responses = []
    non_ascii_responses = []
    errors = []

    if not args.quiet:
        print(f"Starting test on port {args.port} with {args.data_bits}{args.parity[0].upper()}{args.stop_bits}...")
        pbar = tqdm(baudrates, desc="Testing baudrates", leave=True)
    else:
        pbar = baudrates

    for b in pbar:
        result = test_baudrate(ser, b, test_commands, args.timeout, args.all)
        if not result:
            continue

        results.append(result)
        
        # Handle output
        if 'error' in result:
            errors.append(result)
            if not args.quiet:
                tqdm.write(f"⚠️ Baudrate {b}: {result['error']}")
        else:
            if result['is_ascii']:
                ascii_responses.append(result)
                if not args.quiet:
                    tqdm.write(f"✅ Baudrate {b} (ASCII): {result['decoded']}")
            else:
                non_ascii_responses.append(result)
                if args.all and not args.quiet:
                    tqdm.write(f"🔍 Baudrate {b} (Raw): {result['decoded'][:20]}")

        if not args.quiet:
            pbar.update(0)

    ser.close()
    if not args.quiet:
        pbar.close()

    # Save results if requested
    if args.output:
        save_results(results, args.output)
        print(f"\nResults saved to {args.output}")

    # Print summary
    print("\nTest completed. Summary:")
    print(f"• Tested {len(baudrates)} baudrates")
    print(f"• Valid responses: {len(ascii_responses) + len(non_ascii_responses)}")
    print(f"• Errors: {len(errors)}")

    # Detailed results
    if ascii_responses:
        print("\nASCII responses (most likely correct):")
        for res in sorted(ascii_responses, key=lambda x: len(x['response']), reverse=True):
            print(f"  {res['baudrate']}: {res['decoded'][:50]}")
    
    if non_ascii_responses and not args.all:
        print("\nNon-ASCII responses (check with -a for details):")
        print(f"  {[res['baudrate'] for res in non_ascii_responses]}")

if __name__ == "__main__":
    main()
