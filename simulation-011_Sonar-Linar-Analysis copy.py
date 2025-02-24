import numpy as np
import matplotlib.pyplot as plt

# Gegebene Senderpositionen (x, y)
sender_positions = [(145, 980), (55, 948), (118, 972), (279, 993), (20, 930)]
num_senders = len(sender_positions)

# Array-Eigenschaften
d = 0.5  # Abstand zwischen Sensoren (in Wellenlängen)
mean_x = np.mean([x for x, y in sender_positions])
mean_y = np.mean([y for x, y in sender_positions])

# Winkelbereich für das Antennendiagramm
theta_scan = np.linspace(-np.pi, np.pi, 1000)

# Berechnung des Interferenzmusters (komplexes Antennendiagramm)
def calculate_interference_pattern(sender_positions, theta_scan, d, offset_x, offset_y):
    interference_results = []
    for theta_i in theta_scan:
        # Berechnung des Beamforming-Weights für jeden Sender
        steering_weights = np.exp(-2j * np.pi * d * np.array([np.sqrt((x - offset_x)**2 + (y - offset_y)**2) * np.sin(theta_i) for x, y in sender_positions]))
        interference_results.append(np.abs(np.sum(steering_weights))**2)  # Interferenz aufgrund der Phasenverschiebung
    return interference_results

# Berechnung des Interferenzmusters
interference_results = calculate_interference_pattern(sender_positions, theta_scan, d, mean_x, mean_y)

# Polaris-Diagramm für Interferenzen (Radar-Diagramm)
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta_scan, 10 * np.log10(np.array(interference_results)))  # Interferenz in dB
ax.set_theta_zero_location('N')  # 0 Grad oben
ax.set_theta_direction(-1)  # Uhrzeigersinn
ax.set_rlabel_position(55)  # Gitterbeschriftung
ax.set_title("Komplexes Antennen-Diagramm (Radar-Diagramm)")

# Senderpositionen im Polarplot markieren
max_radius = np.max([np.sqrt((x - mean_x)**2 + (y - mean_y)**2) for x, y in sender_positions])  # maximaler Abstand der Sender
for (x, y) in sender_positions:
    # Verschiebung der Koordinaten relativ zum Mittelpunkt
    x_rel = x - mean_x
    y_rel = y - mean_y
    angle = np.arctan2(y_rel, x_rel)  # Winkel der Senderposition im 2D-Raum
    radius = np.sqrt(x_rel**2 + y_rel**2)  # Abstand vom Ursprung (Array-Position)
    
    # Senderposition als rotes Punkt markieren
    ax.plot(angle, radius, 'ro')  
    
    # Position beschriften (nur bei Sendern innerhalb des maximalen Abstands)
    if radius < max_radius:
        ax.text(angle + 0.05, radius + 5, f'({x},{y})', fontsize=9)  # Position beschriften

plt.show()
