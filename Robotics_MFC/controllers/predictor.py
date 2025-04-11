import torch
import pandas as pd
from sklearn.preprocessing import StandardScaler
from Model import MDCBN
import tkinter as tk
import serial
from tkinter import ttk
import random
import time

# Load EEG dataset
dfs = [pd.read_csv("SEM4/MFC4/realdata/BCICIV_eval_ds1" + user + ".csv") for user in ['a', 'b', 'c', 'd']]
for i in range(len(dfs)):
    dfs[i]['User'] = pd.Series(i, index=dfs[i].index)
data = pd.concat(dfs, axis=0).sample(frac=1.0, random_state=123).reset_index(drop=True)
data = data.drop(['User'], axis=1)

X = data.drop(columns=['Class']).values
y = data['Class'].values
y -= 1  # Convert classes to 0, 1 (Right, Left)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Convert to tensors
X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)

# Load model
model = MDCBN(1, 2)
model.load_state_dict(torch.load("mdcbn_modelv2.pth", map_location='cpu'))
model.eval()

# Connect to Arduino
ser = serial.Serial('COM10', 115200, timeout=1)
time.sleep(2)

# Initialize servo angles
servo_angles = {1: 90, 2: 90, 3: 90}

# Send all servo angles at once
def send_all_angles():
    command = f"{servo_angles[1]} {servo_angles[2]} {servo_angles[3]}\n"
    print(f"Sending: {command.strip()}")
    ser.write(command.encode())
    ser.flush()

def on_key(classifier):
    if classifier == 0:  # Right
        servo_angles[1] = max(0, servo_angles[1] - 10)  # Move left
    elif classifier == 1:  # Left
        servo_angles[1] = min(180, servo_angles[1] + 10)  # Move right
    else:  # Neutral (if used)
        servo_angles[1] = 90

    send_all_angles()

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("EEG Real-Time Simulation")
root.geometry("400x300")
root.configure(bg='white')

label_idx = tk.Label(root, text="Sample: 0", font=("Helvetica", 16), bg='white')
label_idx.pack(pady=10)

label_pred = tk.Label(root, text="Predicted: -", font=("Helvetica", 16), bg='white')
label_pred.pack(pady=10)

label_status = tk.Label(root, text="", font=("Helvetica", 24), bg='white')
label_status.pack(pady=20)

def class_name(class_id):
    return {0: 'Right', 1: 'Left', 2: 'Neutral'}.get(class_id, 'Unknown')

def toggle_noise():
    noise_enabled.set(not noise_enabled.get())
    btn_text = "Disable Noise" if noise_enabled.get() else "Enable Noise"
    noise_button.config(text=btn_text)

noise_enabled = tk.BooleanVar(value=False)
noise_button = ttk.Button(root, text="Enable Noise", command=toggle_noise)
noise_button.pack(pady=10)

# --------------- Simulation Loop ---------------
def update_loop():
    sample_idx = random.randint(0, len(X_tensor) - 1)

    eeg_tensor = X_tensor[sample_idx].unsqueeze(0).unsqueeze(0)
    if noise_enabled.get():
        eeg_tensor += torch.randn(eeg_tensor.size()) * 0.1

    with torch.no_grad():
        output = model(eeg_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    label_idx.config(text=f"Sample: {sample_idx}")
    label_pred.config(text=f"Predicted: {class_name(predicted_class)}")
    label_status.config(text="✓", fg='green')

    on_key(predicted_class)
    root.after(2000, update_loop)

# Start simulation
root.after(2000, update_loop)
root.mainloop()
