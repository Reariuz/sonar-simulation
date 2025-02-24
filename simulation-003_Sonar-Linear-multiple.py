import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_antenna_gain(frequency, distance_factor, target_y=250):
    # Parameter
    size_x = 500
    size_y = 1000
    c = 1500
    h = 100
    k = 100

    y_distances = [i * distance_factor for i in range(-2, 3)]
    sources = [(y + (size_x/2), 10) for y in y_distances]

    # Gitter
    x = np.linspace(0, size_x, size_x)
    y = np.linspace(0, size_y, size_y)
    X, Y = np.meshgrid(x, y)

    # Interferenz berechnen
    pressure = np.zeros_like(X)
    for source in sources:
        sx, sy = source
        distance = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
        pressure += np.sin(2 * np.pi * frequency * distance / c)

    # Messung des Schalldrucks bei target_y (z.B. y=500)
    target_pressure = pressure[target_y, :]

    # Berechnung des maximalen Schalldrucks und des Gewinns
    max_pressure = np.max(target_pressure)
    mean_pressure = np.mean(target_pressure)

    return max_pressure, mean_pressure

def generate_Sonar_plot(frequency, distance_factor,text_str):
    # Parameter
    size_x = 500  # Breite des Gitters (x-Achse)
    size_y = 1000  # Höhe des Gitters (y-Achse)
    c = 1500  # Schallgeschwindigkeit in m/s
    h = 100  # Scheitelpunkt x-Koordinate
    k = 100  # Scheitelpunkt y-Koordinate

    y_distances = [i * distance_factor for i in range(-2, 3)]
    sources = [(y +(size_x/2), 10) for y in y_distances]

    x = np.linspace(0, size_x, size_x)
    y = np.linspace(0, size_y, size_y)
    X, Y = np.meshgrid(x, y)

    pressure = np.zeros_like(X)
    for source in sources:
        sx, sy = source
        distance = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
        pressure += np.sin(2 * np.pi * frequency * distance / c)

    # Visualisierung
    plt.figure(figsize=(10, 20))
    plt.contourf(X, Y, pressure, levels=100, cmap='viridis')
    plt.colorbar(label='Schalldruck')
    plt.title('Interferenzmuster mehrerer Sonarsignale')
    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')

    
    plt.figtext(0.5, 0.01, text_str, ha='center', fontsize=10, color='black')

    source_x, source_y = zip(*sources)
    plt.scatter(source_x, source_y, color='red', marker='o', s=100, label='Quellen')

    filename = f'plot_{frequency}-{distance_factor}.png'
    filepath = os.path.join(output_dir, filename)

    plt.savefig(filepath)
    plt.close()

# Verzeichnis zum Speichern der Plots
output_dir = 'plots_linear2'

# Ordner erstellen, falls er noch nicht existiert
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Schleifen zur Erzeugung der Plots und Messung des Antennengewinns
for j in range(5, 50, 5):
    for i in range(5, j, 5):
        max_pressure, mean_pressure = calculate_antenna_gain(i, j)
        text_str = f"Frequenz: {i} MHz, Abstandsfaktor: {j}, Max. Schalldruck: {max_pressure}, Mittelwert: {mean_pressure}"
        generate_Sonar_plot(i, j, text_str )
        print(f"Frequenz: {i} MHz, Abstandsfaktor: {j}, Max. Schalldruck: {max_pressure}, Mittelwert: {mean_pressure}")
