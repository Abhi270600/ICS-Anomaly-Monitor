# sensor_simulator.py
import csv
import time
import random
import math

PATH = "shared_data.csv"

# -------------------------
# Realistic Process Dynamics
# -------------------------

pressure_base = 55       # normal operating pressure (psi)
temperature_base = 110   # base temp (°C)
pump_cycle = 0           # oscillation control

shift_login_hour = 9     # assume day-shift operator present

def generate_normal(t):
    global pump_cycle

    # Pump cycle oscillation (slow sine wave)
    pump_cycle = 5 * math.sin(t / 50)

    # Pressure varies with cycle + noise
    pressure = pressure_base + pump_cycle + random.gauss(0, 0.8)

    # Temperature correlates with pressure + slight delay
    temperature = temperature_base + (pressure - pressure_base) * 0.6 + random.gauss(0, 1.5)

    # ICS write frequency mostly low, occasional small bumps during normal ops
    ics_write_freq = random.gauss(4, 0.4)

    return {
        "pressure": round(pressure, 2),
        "temperature": round(temperature, 2),
        "ics_write_freq": round(ics_write_freq, 2),
        "login_hour": shift_login_hour,
        "source": "sensor"
    }


print("Starting realistic ICS sensor simulation...")
t = 0

while True:
    data = generate_normal(t)

    with open(PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data.values())

    print("[SENSOR] Sent:", data)

    t += 1
    time.sleep(1.5)
