# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt

# Load the Log Data
try:
    df = pd.read_csv("log.csv", header=None,
        names=["pressure", "temperature", "ics_write", "login", "alert", "source"])
except FileNotFoundError:
    print("Error: log.csv not found. Run monitor.py first!")
    exit()

# Setup the Dashboard (3 rows, 1 column)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
plt.subplots_adjust(hspace=0.3)
fig.suptitle(f"OT System Security Audit\nTotal Records: {len(df)} | Anomalies Detected: {df['alert'].sum()}", fontsize=16)

# --- CHART 1: Physical Process (Pressure & Temp) ---
ax1.plot(df["pressure"], label="Pressure (psi)", color="tab:blue", alpha=0.7)
ax1.plot(df["temperature"], label="Temperature (°C)", color="tab:orange", alpha=0.7)
ax1.set_ylabel("Physical Values")
ax1.set_title("1. Physical Process Layer (Sensors)")
ax1.grid(True, alpha=0.3)
ax1.legend(loc="upper left")

# --- CHART 2: Network Activity (ICS Writes) ---
ax2.plot(df["ics_write"], label="ICS Write Freq (Hz)", color="tab:green")
ax2.set_ylabel("Frequency (Hz)")
ax2.set_title("2. Network Layer (Command Frequency)")
ax2.grid(True, alpha=0.3)
ax2.legend(loc="upper left")

# --- CHART 3: Access Control (Login Time) ---
ax3.plot(df["login"], label="Login Hour (24h)", color="tab:purple", drawstyle="steps-post")
ax3.set_ylabel("Hour of Day")
ax3.set_xlabel("Time (Simulation Steps)")
ax3.set_title("3. User Layer (Access Logs)")
ax3.set_yticks([0, 6, 9, 12, 18, 24])
ax3.grid(True, alpha=0.3)
ax3.legend(loc="upper left")

# --- HIGHLIGHT ANOMALIES (Red Dots) on ALL Charts ---
anomalies = df[df["alert"] == 1]

if not anomalies.empty:
    ax1.scatter(anomalies.index, anomalies["temperature"], color="red", s=50, zorder=5)
    ax1.scatter(anomalies.index, anomalies["pressure"], color="red", s=50, zorder=5, label="ANOMALY DETECTED")
    ax2.scatter(anomalies.index, anomalies["ics_write"], color="red", s=50, zorder=5)
    ax3.scatter(anomalies.index, anomalies["login"], color="red", s=50, zorder=5)
    ax1.legend(loc="upper left")

print("Plot generated. Close window to exit.")
plt.show()