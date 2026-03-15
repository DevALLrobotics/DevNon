import numpy as np
import matplotlib.pyplot as plt

print("🎮 WELCOME TO PID SIMULATION GAME 🎮")
print("Your mission: Tune Kp, Ki, Kd so that the robot reaches 90° smoothly!")
print("-----------------------------------------------------------")

# ผู้เล่นกรอกค่าที่อยากลอง
Kp = float(input("Enter Kp (recommended 0.5–2.0): "))
Ki = float(input("Enter Ki (recommended 0–0.5): "))
Kd = float(input("Enter Kd (recommended 0–0.3): "))

# -------- Simulation Settings --------
target = 90       # เป้าหมาย
dt = 0.02         # 20 ms
time = np.arange(0, 5, dt)
angle = 0
error_sum = 0
last_error = 0
angles = []

# -------- Simulation Loop ------------
for t in time:
    error = target - angle
    error_sum += error * dt
    derivative = (error - last_error) / dt
    
    output = Kp * error + Ki * error_sum + Kd * derivative
    
    # โมเดลจำลองความเฉื่อยของหุ่นยนต์
    angle += output * dt - 0.05 * angle * dt
    
    last_error = error
    angles.append(angle)

# -------- Plot Result ---------------
plt.figure(figsize=(8,4))
plt.plot(time, angles, label='Robot Angle')
plt.axhline(target, color='r', linestyle='--', label='Target (90°)')
plt.title(f'PID Simulation Result (Kp={Kp}, Ki={Ki}, Kd={Kd})')
plt.xlabel('Time (s)')
plt.ylabel('Angle (°)')
plt.legend()
plt.grid(True)
plt.show()

# -------- Score System ---------------
final_angle = angles[-1]
overshoot = max(angles) - target
steady_error = abs(final_angle - target)

print("\n📊 GAME RESULT 📊")
print(f"Final angle: {final_angle:.2f}°")
print(f"Overshoot: {overshoot:.2f}°")
print(f"Steady-state error: {steady_error:.2f}°")

if overshoot < 5 and steady_error < 2:
    print("🎉 Perfect! Smooth control achieved!")
elif overshoot < 10:
    print("✅ Good! Some overshoot but acceptable.")
else:
    print("⚠️ Too unstable or too slow! Try tuning again!")
