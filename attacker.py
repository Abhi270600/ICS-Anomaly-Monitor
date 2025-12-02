# attacker.py
import csv
import time

PATH = "shared_data.csv"

while True:
    input("\nPress ENTER to launch insider action…")

    print("\n=== Attack Options ===")
    print("1. Pressure spike (forced pump override)")
    print("2. Cooling failure (temp surge)")
    print("3. ICS write burst (malicious config changes)")
    print("4. Off-hours login event")
    print("5. Multi-step coordinated insider attack")

    c = input("Choose attack: ")

    atk = {
        "pressure": 55,
        "temperature": 110,
        "ics_write_freq": 4,
        "login_hour": 9,
        "source": "attacker"
    }

    if c == "1":
        atk["pressure"] = 80
        atk["temperature"] = 170

    elif c == "2":
        atk["temperature"] = 170

    elif c == "3":
        atk["ics_write_freq"] = 28

    elif c == "4":
        atk["ics_write_freq"] = 25
        atk["login_hour"] = 2

    elif c == "5":
        atk["pressure"] = 75
        atk["temperature"] = 150
        atk["ics_write_freq"] = 25
        atk["login_hour"] = 3

    with open(PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(atk.values())

    print("[ATTACK] Injected:", atk)
