# PID simulation to pre-tune gains for a VEX-style turn-to-angle
# (single-axis rotational dynamics with inertia and damping).
#
# We'll sweep Kp, Ki, Kd over a small grid and compute quality metrics:
# - Overshoot (deg)
# - Settling time within ±1.5° for at least 0.25 s
# - IAE (integral of absolute error)
#
# Then we'll plot the best response and show a table of top candidates.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, Dict

# ------------------ Plant & PID Simulation ------------------
def simulate_turn_to_angle(
    Kp: float,
    Ki: float,
    Kd: float,
    target_deg: float = 90.0,
    J: float = 1.0,            # moment of inertia (arbitrary units)
    c: float = 1.2,            # damping/friction coefficient
    dt: float = 0.01,
    T: float = 3.0,            # total simulation time (s)
    max_power: float = 60.0,   # output saturation (%)
    integral_clamp: float = 200.0,
    settle_band: float = 1.5,  # degrees
    settle_hold: float = 0.25  # seconds
) -> Dict[str, float]:
    """
    Discrete-time simulation of a simple rotational plant:
      theta'' = (u - c*theta') / J
    where u is PID output saturated to +/- max_power.
    """
    n = int(T / dt)
    theta = 0.0       # angle (deg)
    omega = 0.0       # angular velocity (deg/s)
    integ = 0.0
    prev_err = target_deg - theta
    prev_u = 0.0

    time = np.arange(n) * dt
    theta_hist = np.zeros(n)
    err_hist = np.zeros(n)

    settled_since = None
    settling_time = None

    for i in range(n):
        err = target_deg - theta
        integ += err * dt
        # Anti-windup clamp
        integ = max(-integral_clamp, min(integral_clamp, integ))
        deriv = (err - prev_err) / dt

        u = Kp * err + Ki * integ + Kd * deriv
        # Output saturation
        u = max(-max_power, min(max_power, u))

        # Plant dynamics (semi-implicit Euler)
        omega += dt * ( (u - c * omega) / J )
        theta += dt * omega

        # Record
        theta_hist[i] = theta
        err_hist[i] = err

        # Settling detection: |error| < settle_band continuously for settle_hold
        if abs(err) < settle_band:
            if settled_since is None:
                settled_since = time[i]
            else:
                if (time[i] - settled_since) >= settle_hold and settling_time is None:
                    settling_time = settled_since
        else:
            settled_since = None

        prev_err = err
        prev_u = u

    overshoot = max(0.0, np.max(theta_hist) - target_deg)
    iae = np.sum(np.abs(err_hist)) * dt

    # If never settled, set a large sentinel
    if settling_time is None:
        settling_time = float('inf')

    return {
        "Kp": Kp,
        "Ki": Ki,
        "Kd": Kd,
        "overshoot_deg": overshoot,
        "settling_time_s": settling_time,
        "IAE": iae,
        "time": time,
        "theta_hist": theta_hist,
        "err_hist": err_hist
    }

# ------------------ Grid Search ------------------
Kp_grid = np.linspace(0.6, 2.0, 8)        # 0.6 .. 2.0
Ki_grid = [0.0, 0.003, 0.006, 0.01]       # small integral
Kd_grid = np.linspace(0.0, 0.30, 7)       # 0.0 .. 0.30
results = []

for Kp in Kp_grid:
    for Ki in Ki_grid:
        for Kd in Kd_grid:
            sim = simulate_turn_to_angle(Kp, Ki, Kd)
            results.append({
                "Kp": Kp, "Ki": Ki, "Kd": Kd,
                "overshoot_deg": sim["overshoot_deg"],
                "settling_time_s": sim["settling_time_s"],
                "IAE": sim["IAE"]
            })

df = pd.DataFrame(results)

# Filter for "good" candidates and sort by IAE (lower is better)
good = df[(df["overshoot_deg"] < 5.0) & (df["settling_time_s"] < 0.6)].copy()
good = good.sort_values(by=["IAE", "settling_time_s", "overshoot_deg"]).reset_index(drop=True)

# Pick best candidate (or fallback to overall best IAE if none satisfies constraints)
if len(good) > 0:
    best_row = good.iloc[0]
else:
    best_row = df.sort_values(by=["IAE", "settling_time_s", "overshoot_deg"]).iloc[0]

best_params = (float(best_row["Kp"]), float(best_row["Ki"]), float(best_row["Kd"]))

# Re-simulate with best params to plot response
best_sim = simulate_turn_to_angle(*best_params)

# ------------------ Plot Best Response ------------------
plt.figure(figsize=(8,4))
plt.plot(best_sim["time"], best_sim["theta_hist"], label="Angle (deg)")
plt.axhline(90.0, linestyle="--", label="Target (90°)")
plt.title(f"Best PID Response  Kp={best_params[0]:.3f}, Ki={best_params[1]:.3f}, Kd={best_params[2]:.3f}")
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.legend()
plt.grid(True)
plt.show()

# ------------------ Show Top Candidates Table ------------------
# Show top 15 good candidates if available; otherwise show top 15 overall.
top = good.head(15) if len(good) > 0 else df.sort_values(by=["IAE"]).head(15)

# Display as an interactive table to the user
from caas_jupyter_tools import display_dataframe_to_user
display_dataframe_to_user("Top PID Candidates (Turn-to-Angle)", top)

best_params, len(good)
