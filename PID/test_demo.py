from vex import *

# ==========================
# HARDWARE CONFIGURATION
# ==========================
brain = Brain()
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
inertial_sensor = Inertial(Ports.PORT3)

# ==========================
# HELPER FUNCTION
# ==========================
def normalize_angle(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


# ==========================
# 1️⃣ TURN TO ANGLE (หมุนเข้ามุม)
# ==========================
def turn_to_angle(target_deg, Kp=1.0, Ki=0.0, Kd=0.15, max_power=60):
    error = 0
    last_error = 0
    integral = 0
    timer = Timer()

    while True:
        current = inertial_sensor.rotation(DEGREES)
        error = normalize_angle(target_deg - current)
        integral += error
        derivative = error - last_error

        # PID output
        output = Kp * error + Ki * integral + Kd * derivative
        output = max(-max_power, min(max_power, output))  # limit power

        left_motor.spin(FORWARD, output, PERCENT)
        right_motor.spin(FORWARD, -output, PERCENT)

        # Stop condition
        if abs(error) < 1.5:
            left_motor.stop(BRAKE)
            right_motor.stop(BRAKE)
            break

        last_error = error
        wait(15, MSEC)


# ==========================
# 2️⃣ DRIVE STRAIGHT (วิ่งตรงคงหัว)
# ==========================
def drive_straight(distance_cm, speed=40, Kp=2.0, Ki=0.0, Kd=0.1):
    # Reset encoders
    left_motor.set_position(0, DEGREES)
    right_motor.set_position(0, DEGREES)

    # คำนวณรอบล้อ (depends on wheel size)
    wheel_diameter_cm = 10.0
    wheel_circumference = 3.1416 * wheel_diameter_cm
    target_deg = (distance_cm / wheel_circumference) * 360

    # บันทึกหัวเริ่มต้นจาก Inertial
    heading_target = inertial_sensor.rotation(DEGREES)
    integral = 0
    last_error = 0

    while True:
        left_pos = left_motor.position(DEGREES)
        right_pos = right_motor.position(DEGREES)
        avg_pos = (left_pos + right_pos) / 2

        # PID ควบคุมทิศ (heading)
        current_heading = inertial_sensor.rotation(DEGREES)
        heading_error = normalize_angle(heading_target - current_heading)
        integral += heading_error
        derivative = heading_error - last_error

        correction = Kp * heading_error + Ki * integral + Kd * derivative

        left_power = speed + correction
        right_power = speed - correction

        # จำกัดกำลัง
        left_power = max(-100, min(100, left_power))
        right_power = max(-100, min(100, right_power))

        left_motor.spin(FORWARD, left_power, PERCENT)
        right_motor.spin(FORWARD, right_power, PERCENT)

        # ถึงระยะที่ต้องการ
        if avg_pos >= target_deg:
            left_motor.stop(BRAKE)
            right_motor.stop(BRAKE)
            break

        last_error = heading_error
        wait(15, MSEC)


# ==========================
# MAIN FUNCTION
# ==========================
def main():
    brain.screen.print("Calibrating Inertial Sensor...")
    inertial_sensor.calibrate()
    while inertial_sensor.is_calibrating():
        wait(100, MSEC)
    brain.screen.clear_screen()
    brain.screen.print("Ready!")

    # --- ตัวอย่างการใช้งาน ---
    # หมุนเข้ามุม 90°
    turn_to_angle(90)
    wait(500, MSEC)

    # วิ่งตรง 100 cm คงหัวที่หมุนได้
    drive_straight(100, speed=40)

    # หมุนกลับ 0°
    turn_to_angle(0)

main()
