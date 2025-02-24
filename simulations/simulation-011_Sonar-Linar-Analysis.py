import numpy as np
import matplotlib.pyplot as plt

# Simulationsparameter
sample_rate = 1e6  # Abtastrate (Hz)
N = 1000  # Anzahl der Samples

# Generiere einen Ton als Sender-Signal
t = np.arange(N) / sample_rate  # Zeitvektor
f_tone = 100000  # Frequenz des Tones (Hz)
tx = np.exp(2j * np.pi * f_tone * t)  # Sender-Signal (komplex)

# Array-Eigenschaften
d = 0.5  # Abstand zwischen Sensoren (in Wellenlängen)
Nr = 5  # Anzahl der omnidirektionalen Sensoren im Array
theta_degrees = 0  # Einfallswinkel (Grad)
theta = theta_degrees / 180 * np.pi  # Einfallswinkel in Radiant

# Steering-Vektor für Einfallsrichtung
s = np.exp(-2j * np.pi * d * np.arange(Nr) * np.sin(theta))
s = s.reshape(-1, 1)  # Spaltenvektor
tx = tx.reshape(1, -1)  # Zeilenvektor

# Empfangssignal simulieren (Matrix-Multiplikation)
X = s @ tx

# Darstellung des Empfangssignals für alle Sensoren (nur Realteil)
plt.plot(np.asarray(X[0, :]).squeeze().real[:200], label="Sensor 1")
plt.plot(np.asarray(X[1, :]).squeeze().real[:200], label="Sensor 2")
plt.plot(np.asarray(X[2, :]).squeeze().real[:200], label="Sensor 3")
plt.plot(np.asarray(X[3, :]).squeeze().real[:200], label="Sensor 4")
plt.plot(np.asarray(X[4, :]).squeeze().real[:200], label="Sensor 5")
plt.legend()
plt.title("Empfangssignal der Sensoren (Realteil)")
plt.xlabel("Sample-Index")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# Beamforming: Delay-and-Sum
w = np.exp(-2j * np.pi * d * np.arange(Nr) * np.sin(theta))  # Gewichtungen
X_weighted = w.conj().T @ X  # Beamforming anwenden
print(X_weighted.shape)  # 1xN Empfangssignal nach Beamforming

# Richtungsscanning
theta_scan = np.linspace(-1 * np.pi, np.pi, 1000)  # Winkelbereich (-180 bis +180 Grad)
results = []
for theta_i in theta_scan:
    w = np.exp(-2j * np.pi * d * np.arange(Nr) * np.sin(theta_i))  # Beamforming-Gewichtungen
    X_weighted = w.conj().T @ X  # Beamforming
    results.append(10 * np.log10(np.var(X_weighted)))  # Leistung in dB
results -= np.max(results)  # Normalisieren

# Maximale Richtung anzeigen
print("Maximaler Winkel (DOA):", theta_scan[np.argmax(results)] * 180 / np.pi, "Grad")

# Ergebnisse plotten
plt.plot(theta_scan * 180 / np.pi, results)  # Winkel in Grad
plt.title("DOA-Scannen")
plt.xlabel("Theta [Grad]")
plt.ylabel("DOA-Metrik (dB)")
plt.grid()
plt.show()

# Polaris-Diagramm
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta_scan, results)  # Radian für Polarplot
ax.set_theta_zero_location('N')  # 0 Grad oben
ax.set_theta_direction(-1)  # Uhrzeigersinn
ax.set_rlabel_position(55)  # Gitterbeschriftung
plt.show()

# Array-Beamforming-Pattern analysieren (FFT-Methode)
N_fft = 512
theta_degrees = 0  # Richtung, auf die wir fokussieren
theta = theta_degrees / 180 * np.pi
w = np.exp(-2j * np.pi * d * np.arange(Nr) * np.sin(theta))  # Beamforming-Gewichtungen
w = np.conj(w)  # Konjugiert für korrektes Beamforming
w_padded = np.concatenate((w, np.zeros(N_fft - Nr)))  # Zero-Padding für FFT
w_fft_dB = 10 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(w_padded))) ** 2)  # FFT und dB-Skalierung
w_fft_dB -= np.max(w_fft_dB)  # Normalisierung

# Zuordnung von FFT-Bins zu Winkeln
theta_bins = np.arcsin(np.linspace(-1, 1, N_fft))  # Winkel in Radiant
theta_max = theta_bins[np.argmax(w_fft_dB)]  # Maximaler Winkel

# Polaris-Diagramm für Beamforming-Muster
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta_bins, w_fft_dB)  # Polarisplot
ax.plot([theta_max], [np.max(w_fft_dB)], 'ro')  # Maximum markieren
ax.text(theta_max - 0.1, np.max(w_fft_dB) - 4, np.round(theta_max * 180 / np.pi))  # Winkel beschriften
ax.set_theta_zero_location('N')  # 0 Grad oben
ax.set_theta_direction(-1)  # Uhrzeigersinn
ax.set_thetamin(-90)  # Nur obere Hälfte
ax.set_thetamax(90)
ax.set_ylim([-30, 1])  # Dynamikbereich begrenzen
plt.show()
