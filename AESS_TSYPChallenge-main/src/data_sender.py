import socket
import time
import random

# --- CONFIGURATION ---
HOST = '127.0.0.1'
PORT = 5000
DELAY = 1.0  # Seconds to wait between sending data

# --- DATA TO SEND ---
# You can replace this list with lines from your CSV file!
test_data = [
    "0.01, 0.1, 0.02, 0.85, 0.001",   # Healthy
    "0.02, 0.1, 0.03, 0.84, 0.001",   # Healthy
    "0.01, 0.1, 0.02, 0.85, 0.002",   # Healthy
    "2.50, 1.5, 0.50, 0.45, 0.100",   # !!! CRITICAL FAULT !!!
    "2.60, 1.6, 0.55, 0.40, 0.120",   # !!! CRITICAL FAULT !!!
    "0.01, 0.1, 0.02, 0.85, 0.001"    # Back to Normal
]

print(f"Connecting to AI Server on {PORT}...")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected! Sending data stream...")
        print("-" * 40)

        for line in test_data:
            print(f"Sending: {line}")
            s.sendall(line.encode())
            time.sleep(DELAY) # Wait a bit to simulate real time

    print("Data stream finished.")

except ConnectionRefusedError:
    print("[ERROR] Could not connect. Did you run the AI Server in Terminal 1 first?")
