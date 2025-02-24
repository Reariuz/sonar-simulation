import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameter
frequency = 100e3  # Frequenz in Hz
c = 1500  # Schallgeschwindigkeit im Wasser (m/s)
wavelength = c / frequency  # Wellenlänge

# Antennenpositionen (Mitte + Hexagon)
center_position = np.array([0, 0, 0])
hexagon_radius = 50 * wavelength

# Berechnung der Positionen der Sender
second_layer_radius = 2.0 * hexagon_radius   # Radius of the second layer

# Angles for the first and second layers
angles_first_layer = np.linspace(0, 2 * np.pi, 7)[:-1]  # 6 points in the first layer
angles_second_layer = np.linspace(0, 2 * np.pi, 13)[:-1]  # 12 points in the second layer

# First layer (1 point in the middle and 6 surrounding it)
positions_first_layer = np.array([
    center_position] +  # Include center_position in the array
    [
        [hexagon_radius * np.cos(angle), hexagon_radius * np.sin(angle), 0]  # Positions around the hexagon
        for angle in angles_first_layer
    ]
)

# Second layer (12 points around the second layer radius)
positions_second_layer = np.array([
    [second_layer_radius * np.cos(angle), second_layer_radius * np.sin(angle), 0]  # Points around the second hexagon
    for angle in angles_second_layer
])

# Combine the layers
positions = np.vstack([positions_first_layer, positions_second_layer])


# Erstellen des Plots
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotten der Senderpositionen
ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], color='r', s=100)

# Erstellen eines Gitters für das Antennendiagramm
theta = np.linspace(0, 2 * np.pi, 100)  # Azimutwinkel
phi = np.linspace(0, np.pi, 50)  # Elevationswinkel

theta, phi = np.meshgrid(theta, phi)

# Berechnung der kartesischen Koordinaten für das Diagramm
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Berechnung der Intensität basierend auf den Abständen zu den Sendern und der Strahlrichtung
intensity = np.zeros_like(x)

# Berechnung der Intensität unter Berücksichtigung der Strahlcharakteristik (Dipolstrahlung)
for pos in positions:
    # Berechnung der Abstände zu den Beobachtungspunkten
    distance = np.sqrt((x - pos[0]) ** 2 + (y - pos[1]) ** 2 + (z - pos[2]) ** 2)
    
    # Vektoren zu den Beobachtungspunkten
    pos_x = pos[0] - x  # Subtraktion für jede x-Koordinate
    pos_y = pos[1] - y  # Subtraktion für jede y-Koordinate
    pos_z = pos[2] - z  # Subtraktion für jede z-Koordinate
    
    # Berechnung des Richtungsvektors und der Intensität
    r_unit = np.array([pos_x, pos_y, pos_z])  # Differenz-Vektor zu jedem Punkt
    r_unit /= np.linalg.norm(r_unit, axis=0)  # Normalisieren des Vektors
    
    # Berechnung des Winkels zur Z-Achse (vertikal)
    angle = np.arccos(r_unit[2])  # Winkel von der Z-Achse
    
    # Monopolstrahlungsmuster mit "Eierform"
    alpha = 2  # Steuert die Asymmetrie der Strahlung
    beta = 1    # Weitere Modifikation des Musters
    radiation_pattern = (np.sin(angle)**alpha) * (np.cos(angle)**beta)  # Egg-shaped pattern
    
    # Sicherstellen, dass die Shapes kompatibel sind
    intensity += (radiation_pattern / (distance + 1e-6)**2)  # Inverses Quadrat der Entfernung



# Normalisieren der Intensität für die Farbskala
intensity /= np.max(intensity)

# Plotten der Oberfläche mit Farbskala basierend auf der Intensität
ax.plot_surface(x, y, z, facecolors=plt.cm.viridis(intensity), rstride=5, cstride=5, alpha=0.8)

# Achsenbeschriftung und Titel
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Antennendiagramm mit Keulen (Sonar, 100kHz)')

plt.show()
