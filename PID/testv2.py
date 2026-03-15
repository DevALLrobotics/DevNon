import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- Simulation parameters ---
target = 90
dt = 0.02
time = np.arange(0, 5, dt)

# --- Initialize variables ---
angle = 0
error_sum = 0
last_error = 0

# --- Tkinter GUI setup ---
root = tk.Tk()
root.title("🎮 PID Simulation Game (Real-Time)")

# --- Matplotlib Figure ---
fig, ax = plt.subplots(figsize=(6, 3))
ax.set_ylim(0, 100)
ax.set_xlim(0, 5)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Angle (°)")
ax.set_title("PID Control Response")
line, = ax.plot([], [], lw=2)
ax.axhline(target, color='r', linestyle='--', label='Target (90°)')
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)

# --- PID sliders ---
Kp = tk.DoubleVar(value=1.2)
Ki = tk.DoubleVar(value=0.1)
Kd = tk.DoubleVar(value=0.05)

def create_slider(text, var, row, from_, to_):
    label = ttk.Label(root, text=text)
    label.grid(row=row, column=0)
    slider = ttk.Scale(root, from_=from_, to=to_, orient='horizontal', variable=var, length=200)
    slider.grid(row=row, column=1)
    value_label = ttk.Label(root, textvariable=var)
    value_label.grid(row=row, column=2)

create_slider("Kp", Kp, 1, 0, 3)
create_slider("Ki", Ki, 2, 0, 0.5)
create_slider("Kd", Kd, 3, 0, 0.3)

# --- Simulation update function ---
def simulate():
    global angle, error_sum, last_error
    angle = 0
    error_sum = 0
    last_error = 0
    angles = []

    kp = Kp.get()
    ki = Ki.get()
    kd = Kd.get()

    for t in time:
        error = target - angle
        error_sum += error * dt
        derivative = (error - last_error) / dt
        output = kp * error + ki * error_sum + kd * derivative
        angle += (output - 0.05 * angle) * dt  # inertia effect
        last_error = error
        angles.append(angle)

    # Update graph
    line.set_data(time, angles)
    ax.relim()
    ax.autoscale_view()
    canvas.draw()

# --- Update button ---
simulate_button = ttk.Button(root, text="▶️ Run Simulation", command=simulate)
simulate_button.grid(row=4, column=1, pady=10)

# --- Start GUI loop ---
root.mainloop()
