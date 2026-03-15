import numpy as np
import matplotlib.pyplot as plt
import random

# ===========================================
# SIMULATION ENVIRONMENT (for RL fine-tuning)
# ===========================================
class DriveStraightEnv:
    def __init__(self, dt=0.015, target_angle=0.0, max_t=3.0):
        self.dt = dt
        self.max_t = max_t
        self.target = target_angle
        self.reset()

    def reset(self):
        self.angle = random.uniform(-5, 5)   # initial drift (deg)
        self.rate = 0.0                      # angular velocity
        self.integral = 0.0
        self.last_error = 0.0
        self.time = 0.0
        self.done = False
        return np.array([self.angle, self.rate])

    def step(self, action):
        """action = [Kp, Ki, Kd, Kg]"""
        Kp, Ki, Kd, Kg = action
        error = self.target - self.angle
        self.integral += error * self.dt
        derivative = (error - self.last_error) / self.dt

        output = Kp * error + Ki * self.integral + Kd * derivative - Kg * self.rate
        output = np.clip(output, -100, 100)

        # --- system response (nonlinear + damping)
        self.rate += 0.1 * output - 0.05 * self.rate
        self.angle += self.rate * self.dt
        self.last_error = error
        self.time += self.dt

        # --- reward: penalize oscillation & overshoot
        reward = - (abs(error) + 0.05 * abs(self.rate) + 0.01 * abs(output))
        if abs(self.angle) < 0.5 and abs(self.rate) < 0.5:
            reward += 1.0  # stability bonus

        # --- termination
        if self.time > self.max_t:
            self.done = True

        obs = np.array([self.angle, self.rate])
        return obs, reward, self.done, {}

# ===========================================
# TRAINING LOOP (simple random policy)
# ===========================================
def evaluate_params(params):
    """Run simulation and return total reward"""
    env = DriveStraightEnv()
    total_reward = 0
    obs = env.reset()
    while not env.done:
        obs, r, d, _ = env.step(params)
        total_reward += r
    return total_reward

def random_search(num_trials=200):
    best_reward = -1e9
    best_params = None
    for _ in range(num_trials):
        # Random parameter sampling
        Kp = random.uniform(0, 5)
        Ki = random.uniform(0.001, 0.01)
        Kd = random.uniform(0.01, 0.3)
        Kg = random.uniform(0.1, 0.9)
        params = (Kp, Ki, Kd, Kg)

        R = evaluate_params(params)
        if R > best_reward:
            best_reward = R
            best_params = params
            print(f"✅ New best {params} => {R:.2f}")
    return best_params

# ===========================================
# DEMO (fine-tune then visualize)
# ===========================================
if __name__ == "__main__":
    best_params = random_search(300)
    print("\n🔍 Best Parameters Found:", best_params)

    # visualize
    env = DriveStraightEnv()
    obs = env.reset()
    angle_log, output_log, rate_log = [], [], []
    while not env.done:
        obs, r, d, _ = env.step(best_params)
        angle_log.append(env.angle)
        rate_log.append(env.rate)
        # output_log can be derived in env.step for plotting if needed

    t = np.arange(len(angle_log)) * env.dt
    plt.figure(figsize=(10,5))
    plt.plot(t, angle_log, label='Angle (°)')
    plt.axhline(0, color='gray', linestyle='--')
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (°)")
    plt.title("RL-Tuned PID Response")
    plt.legend()
    plt.show()
