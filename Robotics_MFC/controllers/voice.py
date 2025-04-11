import speech_recognition as sr
import serial
import time
import numpy as np

# --- Arduino setup ---
ser = serial.Serial('COM10', 115200, timeout=1)
time.sleep(2)

# --- Arm configuration ---
L1 = 10  # Base to shoulder (Z direction offset)
L2 = 10  # Shoulder to elbow
L3 = 10  # Elbow to wrist
step = 2  # Step size per command (in cm)

# Initial position of end-effector
x, y, z = 15.0, 0.0, 5.0

# --- Inverse Kinematics Function ---
def send_angles(theta1, theta2, theta3):
    command = f"{int(theta1)} {int(theta2)} {int(theta3)}\n"
    print(f"🦾 Sending angles: {command.strip()}")
    ser.write(command.encode())

def ik_3d(x, y, z):
    try:
        theta1 = np.degrees(np.arctan2(y, x))

        xy_dist = np.hypot(x, y)
        wrist_dist = np.hypot(xy_dist, z - L1)

        cos_theta3 = (L2**2 + L3**2 - wrist_dist**2) / (2 * L2 * L3)
        cos_theta3 = np.clip(cos_theta3, -1.0, 1.0)
        theta3 = np.degrees(np.arccos(cos_theta3))

        angle_a = np.arctan2(z - L1, xy_dist)
        angle_b = np.arccos(np.clip((L2**2 + wrist_dist**2 - L3**2) / (2 * L2 * wrist_dist), -1.0, 1.0))
        theta2 = np.degrees(angle_a + angle_b)

        # Safety bounds
        theta1 = np.clip(theta1, 0, 180)
        theta2 = np.clip(theta2, 0, 180)
        theta3 = np.clip(theta3, 0, 180)

        send_angles(theta1, theta2, theta3)

    except Exception as e:
        print(f"⚠️ IK Error: {e}")

# --- Voice Recognition Setup ---
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎙 Voice control (IK) started. Say: left, right, up, down, forward, backward, or stop.")

def listen_for_commands():
    global x, y, z

    while True:
        with mic as source:
            print("🎧 Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                print("⚠️ Timeout. Listening again...")
                continue

        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"🔊 Heard: {command}")

            if "left" in command:
                x -= step
            elif "right" in command:
                x += step
            elif "up" in command:
                z += step
            elif "down" in command:
                z -= step
            elif "forward" in command:
                y += step
            elif "backward" in command:
                y -= step
            elif "stop" in command:
                print("🛑 Stopping voice control.")
                break
            else:
                print("❓ Command not recognized.")
                continue

            # Apply inverse kinematics
            ik_3d(x, y, z)
            print(f"📍 New Position: x={x:.1f}, y={y:.1f}, z={z:.1f}")

        except sr.UnknownValueError:
            print("🤷 Could not understand.")
        except sr.RequestError as e:
            print(f"⚠️ API Error: {e}")

listen_for_commands()
ser.close()
