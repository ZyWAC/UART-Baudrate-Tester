import serial
import time
from tqdm import tqdm
import argparse
import sys

# Author: ZyWAC
# UART Baudrate Tester - A tool to brute-force test and identify correct UART baudrates

# Comprehensive list of baud rates including standard and specialized ones
baudrates = [
    50, 75, 110, 134, 135, 150, 200, 300, 600, 1200, 1800, 2400, 3600, 4800, 7200, 9600, 14400, 19200, 28800, 31250, 38400, 
    56000, 57600, 76800, 115200, 115700, 125000, 128000, 230400, 250000, 256000, 460800, 500000, 512000, 600000, 750000, 921600, 
    1000000, 1152000, 1382400, 1500000, 2000000, 3686400, 3000000, 4000000
]

def is_ascii_printable(data):
    """Check if data contains only printable ASCII characters"""
    try:
        text = data.decode('ascii')
        # Check if all characters are printable ASCII (32-126) or common whitespace
        return all(32 <= ord(c) <= 126 or c in '\r\n\t' for c in text)
    except UnicodeDecodeError:
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Baudrate brute-force tester for serial ports')
    parser.add_argument('-a', '--all', action='store_true', 
                      help='Show all raw output without ASCII check (up to 20 characters)')
    parser.add_argument('-p', '--port', default='/dev/ttyUSB0', 
                      help='Serial port to test (default: /dev/ttyUSB0)')
    args = parser.parse_args()

    test_string = b'hello\r\n'  # Test string to send
    non_ascii_baudrates = []    # Store baudrates with non-ASCII output

    print("Starting baudrate brute-force test...")
    # Create progress bar, leave=True to keep it after completion
    pbar = tqdm(baudrates, desc="Testing baudrates", leave=True)
    for b in pbar:
        try:
            with serial.Serial(args.port, b, timeout=1) as ser:
                # Send two carriage returns (simulate pressing enter twice)
                ser.write(b'\r\n\r\n')
                time.sleep(0.5)  # Short delay to allow response
                
                # Send test string
                ser.write(test_string)
                time.sleep(0.5)  # Short delay to allow response
                
                # Read up to 100 bytes of response
                response = ser.read(100)
                
                if response:
                    # Handle -a flag: show raw output without ASCII check
                    if args.all:
                        # Limit to 20 characters for readability
                        limited_response = response[:20]
                        
                        # Use tqdm's write method to preserve progress bar
                        # Convert raw bytes to string representation to avoid control characters
                        tqdm.write(f"Baudrate {b} raw output: {limited_response.decode('latin-1', errors='replace')}")
                        
                    else:
                        # Normal mode with ASCII check
                        if is_ascii_printable(response):
                            tqdm.write(f"Baudrate {b} returned ASCII data: {response.decode('ascii').strip()}")
                        else:
                            non_ascii_baudrates.append(b)
                            
        except serial.SerialException:
            # Ignore unsupported baudrates or port errors
            pass
        except Exception as e:
            # Ignore other errors to continue testing
            pass
        # Update progress bar explicitly
        pbar.update(0)

    pbar.close()
    # Test completion message
    print("\nTest completed.")
    
    # Show non-ASCII baudrates only in normal mode
    if not args.all and non_ascii_baudrates:
        print(f"Baudrates with non-ASCII output: {sorted(non_ascii_baudrates)}")
    elif not args.all:
        print("No baudrates with non-ASCII output detected.")

if __name__ == "__main__":
    main()
    
