import socket
import pickle
import numpy as np
import warnings

# --- CONFIGURATION ---
HOST = '127.0.0.1'  # Localhost (The Pi talks to itself)
PORT = 5000         # The "Channel" we will use

# --- LOAD AI MODEL ---
print("1. Loading AI Model...")
try:
    with open("model/isolation_forest.pkl", "rb") as f:
        model = pickle.load(f)
    print("   [SUCCESS] Model Loaded!")
except FileNotFoundError:
    print("   [ERROR] Model file not found in 'model/' folder.")
    exit()

# --- START SERVER ---
print(f"2. Starting AI Server on {HOST}:{PORT}...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("   [WAITING] Open Terminal 2 and run the Sender script...")
    
    conn, addr = s.accept()
    with conn:
        print(f"   [CONNECTED] Data Source connected from {addr}")
        print("-" * 40)
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Decode the text data (e.g., "0.01,0.1,0.02,0.85,0.001")
            text_data = data.decode().strip()
            
            try:
                # Convert text to numbers
                values = list(map(float, text_data.split(',')))
                features = np.array([values])
                
                # --- AI PREDICTION ---
                # Suppress warnings for clean output
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    score = model.decision_function(features)[0]
                    prediction = model.predict(features)[0]

                # --- DISPLAY RESULT ---
                status = "NORMAL " if prediction == 1 else "ANOMALY"
                color = "\033[92m" if prediction == 1 else "\033[91m" # Green vs Red
                reset = "\033[0m"
                
                print(f"Input: {values} -> Score: {score:.4f} -> {color}{status}{reset}")
                
            except ValueError:
                print(f"Received invalid data: {text_data}")

print("Connection closed.")
