import numpy as np
import serial
import time
import keyboard  # pip install keyboard

# Serial connection to Arduino
ser = serial.Serial('COM10', 115200, timeout=1)
time.sleep(2)

# Link lengths (cm)
L1 = 10  # Base to shoulder
L2 = 10  # Shoulder to elbow
L3 = 10  # Elbow to wrist

# Initial end effector position
x, y, z = 15.0, 0.0, 5.0
step = 5.0  # Movement step per keypress (cm)

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

        theta1 = np.clip(theta1, 0, 180)
        theta2 = np.clip(theta2, 0, 180)
        theta3 = np.clip(theta3, 0, 180)

        send_angles(theta1, theta2, theta3)

    except Exception as e:
        print(f"⚠️ IK Error: {e}")

# Main loop
print("🔧 Use W/S (Z axis), A/D (X axis), Q/E (Y axis) — ESC to exit.")

while True:
    try:
        if keyboard.is_pressed("w"): z += step
        if keyboard.is_pressed("s"): z -= step
        if keyboard.is_pressed("a"): x -= step
        if keyboard.is_pressed("d"): x += step
        if keyboard.is_pressed("q"): y += step
        if keyboard.is_pressed("e"): y -= step

        ik_3d(x, y, z)
        print(f"📍 Position → X: {x:.1f}, Y: {y:.1f}, Z: {z:.1f}")
        time.sleep(0.3)

        if keyboard.is_pressed("esc"):
            print("🛑 Exiting...")
            break

    except KeyboardInterrupt:
        break

ser.close()