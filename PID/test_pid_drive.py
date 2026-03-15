#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
intake_motor_motor_a = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
intake_motor_motor_b = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
intake_motor = MotorGroup(intake_motor_motor_a, intake_motor_motor_b)
left_drive_motor_motor_a = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
left_drive_motor_motor_b = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
left_drive_motor = MotorGroup(left_drive_motor_motor_a, left_drive_motor_motor_b)
right_drive_motor_motor_a = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
right_drive_motor_motor_b = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
right_drive_motor = MotorGroup(right_drive_motor_motor_a, right_drive_motor_motor_b)
digital_out_a = DigitalOut(brain.three_wire_port.a)
digital_out_b = DigitalOut(brain.three_wire_port.b)
outtake_motor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
inertial_sensor = Inertial(Ports.PORT21)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEXs
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *


# Begin project code
def dir_drive(L_Dir, R_Dir, SL, SR, t):
    """Manual directional drive with % speed control"""
    if L_Dir == 1:
        L_Dir = FORWARD
    elif L_Dir == 0:
        L_Dir = REVERSE

    if R_Dir == 1:
        R_Dir = FORWARD
    elif R_Dir == 0:
        R_Dir = REVERSE

    left_drive_motor.set_velocity(SL, PERCENT)
    right_drive_motor.set_velocity(SR, PERCENT)

    left_drive_motor.spin(L_Dir)
    right_drive_motor.spin(R_Dir)

    wait(t, SECONDS)

    left_drive_motor.stop()
    right_drive_motor.stop()


def intakeOne(s, t):
    """Run intake and outtake motors"""
    outtake_motor.set_max_torque(80, PERCENT)
    intake_motor.set_velocity(s, PERCENT)
    outtake_motor.set_velocity(95, PERCENT)

    intake_motor.spin(FORWARD)
    outtake_motor.spin(REVERSE)
    wait(t, SECONDS)
    intake_motor.stop()


# ===========================================
# ADVANCED MOTION FUNCTIONS (PID CONTROL)
# ===========================================

def normalize_angle(angle):
    """Keep angle between -180 and 180 degrees"""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def turn_to_angle(target_deg, Kp=1.0, Ki=0.005, Kd=0.2, max_power=20):
    """PID control to turn robot smoothly to target angle"""
    
    # ========= STEP 1 : รอและเซ็ตเซนเซอร์ให้พร้อม =========
    brain.screen.print("Preparing inertial sensor...")

    # ถ้าเพิ่งเปิดเครื่องใหม่ ควร calibrate
    if inertial_sensor.is_calibrating():
        while inertial_sensor.is_calibrating():
            wait(100, MSEC)

    # รอให้ค่านิ่งก่อนเริ่ม
    base_angle = inertial_sensor.rotation(DEGREES)
    wait(200, MSEC)
    for _ in range(5):
        diff = abs(inertial_sensor.rotation(DEGREES) - base_angle)
        if diff < 0.3:
            continue
        else:
            base_angle = inertial_sensor.rotation(DEGREES)
            wait(100, MSEC)

    # รีเซ็ต rotation ให้เริ่มที่ 0 ทุกครั้ง
    inertial_sensor.set_rotation(0, DEGREES)
    print("✅ Inertial ready, starting turn...")

    # ========= STEP 2 : PID เริ่มทำงาน =========
    error = 0
    last_error = 0
    integral = 0
    stable_count = 0

    while True:
        current = inertial_sensor.rotation(DEGREES)
        gyro_z = inertial_sensor.gyro_rate(AxisType.ZAXIS, VelocityUnits.DPS)
        error = normalize_angle(target_deg - current)

        # Reset / Clamp integral
        if abs(error) < 2:
            integral = 0
        else:
            integral += error
            integral = max(-300, min(300, integral))

        derivative = error - last_error

        # PID output + damping
        damping = gyro_z * 0.05
        output = Kp * error + Ki * integral + Kd * derivative - damping
        output = max(-max_power, min(max_power, output))

        left_drive_motor.spin(FORWARD, output, PERCENT)
        right_drive_motor.spin(FORWARD, -output, PERCENT)

        if abs(error) < 1.0 and abs(gyro_z) < 3:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count > 5:
            left_drive_motor.stop(BRAKE)
            right_drive_motor.stop(BRAKE)
            print("===========================================")

            break

        last_error = error
        print("Angle = {:.2f}, Rate = {:.2f}, Output = {:.2f}".format(current, gyro_z, output))
        wait(15, MSEC)

def drive_straight(distance_cm, max_speed=40):
    """Drive straight with gyro-assisted PID and soft BRAKE stop"""
    
    # --- รีเซ็ตเซนเซอร์ ---
    left_drive_motor.set_position(0, DEGREES)
    right_drive_motor.set_position(0, DEGREES)
    inertial_sensor.set_rotation(0, DEGREES)
    
    # --- Wheel setup ---
    wheel_circumference = 22.0  # cm per wheel revolution
    target_deg = (distance_cm / wheel_circumference) * 360
    
    # --- PID parameters ---
    Kp = 3.5
    Ki = 0.01
    Kd = 0.1
    Kg = 0.5  # weight for gyro rate correction
    integral = 0
    last_error = 0
    
    heading_target = inertial_sensor.rotation(DEGREES)
    
    while True:
        # --- Encoder average ---
        left_pos = left_drive_motor.position(DEGREES)
        right_pos = right_drive_motor.position(DEGREES)
        avg_pos = (left_pos + right_pos) / 2
        
        # --- Heading PID ---
        current_heading = inertial_sensor.rotation(DEGREES)
        error = normalize_angle(heading_target - current_heading)
        integral += error
        derivative = error - last_error
        
        # --- Gyro rate ---
        gyro_z = inertial_sensor.gyro_rate(AxisType.ZAXIS, VelocityUnits.DPS)
        
        # --- Combined correction ---
        correction = Kp * error + Ki * integral + Kd * derivative + Kg * (-gyro_z)
        
        # --- Ramp-down speed near target ---
        remaining = target_deg - avg_pos
        if remaining < 30:  # ใกล้เป้าหมาย <30 deg, ลดกำลัง
            ramp_speed = max(5, max_speed * (remaining / 30))
        else:
            ramp_speed = max_speed
        
        # --- Motor power ---
        left_power = ramp_speed - correction
        right_power = ramp_speed - correction
        left_power = max(-100, min(100, left_power))
        right_power = max(-100, min(100, right_power))

        # print(gyro_z,",", correction)
        print(left_power, ",", right_power)
        
        left_drive_motor.spin(FORWARD, left_power, PERCENT)
        right_drive_motor.spin(FORWARD, right_power, PERCENT)
        
        # --- Stop condition ---
        if remaining <= 1.5:  # ใกล้สุด
            left_drive_motor.stop(BRAKE)
            right_drive_motor.stop(BRAKE)
            wait(50, MSEC)  # ให้ motor PID ปรับแก้ tilt สั้น ๆ
            break
        
        last_error = error
        wait(15, MSEC)

# ===========================================
# MAIN PROGRAM
# ===========================================


def test():
    # PID-based turn and drive
    inertial_sensor.calibrate()
    drive_straight(60,60)
    #turn_to_angle(-90)           # Turn to 90°
    # wait(500, MSEC)
    # turn_to_angle(0)            # Turn back to 0°

test()

def main():
    brain.screen.print("Calibrating Inertial Sensor...")
    inertial_sensor.calibrate()
    while inertial_sensor.is_calibrating():
        wait(100, MSEC)
    brain.screen.clear_screen()
    brain.screen.print("Ready!")

    # ---- Autonomous example sequence ----
    dir_drive(1, 1, 40, 40, 0.5)
    dir_drive(1, 1, 0, 20, 0.2)
    dir_drive(1, 1, 20, 20, 2.5)
    intakeOne(60, 1)

    # PID-based turn and drive
    turn_to_angle(90)           # Turn to 90°
    wait(500, MSEC)
    drive_straight(1000, 40)     # Drive forward 100 cm
    turn_to_angle(0)            # Turn back to 0°

# main()





# def test():
#     left_drive_motor.spin(FORWARD)
#     right_drive_motor.spin(FORWARD)
#     wait(1,SECONDS)
#     left_drive_motor.stop()
#     right_drive_motor.stop()

# # test()


# def dir_drive(L_Dir,R_Dir,SL,SR,t):
#     if L_Dir == 1:
#         L_Dir = FORWARD
#     elif L_Dir == 0:
#         L_Dir = REVERSE

#     if R_Dir == 1:
#         R_Dir = FORWARD
#     elif R_Dir == 0:
#         R_Dir = REVERSE

#     left_drive_motor.set_velocity(SL,PERCENT)
#     right_drive_motor.set_velocity(SR,PERCENT)

#     left_drive_motor.spin(L_Dir)
#     right_drive_motor.spin(R_Dir)

#     wait(t,SECONDS)

#     left_drive_motor.stop()
#     right_drive_motor.stop()


# def intakeOne(s,t):
#     outtake_motor.set_max_torque(80,PERCENT)
#     intake_motor.set_velocity(s,PERCENT)
#     outtake_motor.set_velocity(95,PERCENT)

#     intake_motor.spin(FORWARD)
#     outtake_motor.spin(REVERSE)
#     wait(t,SECONDS)
#     intake_motor.stop()


# dir_drive(1,1,40,40,0.5)
# dir_drive(1,1,0,20,0.2)
# dir_drive(1,1,20,20,2.5)
# intakeOne(60,1)