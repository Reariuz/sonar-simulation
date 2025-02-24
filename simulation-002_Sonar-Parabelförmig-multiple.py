import numpy as np 
import matplotlib.pyplot as plt 
import os


def generate_Sonar_plot (frequency,distance_factor,alpha):
    # Parameter
    size = 500 # grid Zise
    Wavelength = 50
    c =1500 #Schallgeschwindigkeit m/s
    #frequency = 1000 # Frequenz in Mhz
    # Parameter für die Parabel
    #a = 0.02  # Steigung der Parabel (je größer, desto enger ist die Parabel)
    a = alpha /100
    h = 50  # Scheitelpunkt x-Koordinate
    k = 100  # Scheitelpunkt y-Koordinate

    # Abstände der Punkte entlang der x-Achse (die x-Werte)
    #y_distances = [-50,-25,0,25,50]  # Die x-Positionen der Punkte
    y_distances = [i * distance_factor for i in range(-2, 3)]


    # Generierung der x-Werte basierend auf der Parabelgleichung x = a * (y - k)^2 + h
    sources = [(a * (y)**2 +h , y + k*2) for y in y_distances]

    #gitter
    x = np.linspace(0, size, size)
    y = np.linspace(0, size, size)
    X, Y = np.meshgrid(x, y)

    # Interferenz berechnen
    pressure = np.zeros_like(X)
    for source in sources:
        sx, sy = source
        distance = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
        pressure += np.sin(2 * np.pi * frequency * distance / c)

    # visualisierung
    plt.figure(figsize=(8,6))
    plt.contourf(X, Y, pressure, levels=100, cmap='viridis')
    plt.colorbar(label='schalldruck')
    plt.title('Interferenzmuster mehrer Sonarsignale')
    plt.xlabel('X-position')
    plt.ylabel('Y-position')

    # Variablen im Plot vermerken
    text_str = f'Variablen: frequency in MHz = {frequency}, distance_factor = {distance_factor}, alpha_faktor = {alpha}'
    
    # Text unter dem Plot hinzufügen
    plt.figtext(0.5, 0.01, text_str, ha='center', fontsize=10, color='black')

    # Quellen als Kreise im Plot anzeigen
    source_x, source_y = zip(*sources)  # x und y Koordinaten der Quellen extrahieren
    plt.scatter(source_x, source_y, color='red', marker='o', s=100, label='Quellen')


    #plt.show()
        # Dateiname für den Plot
    filename = f'plot_{frequency}-{distance_factor}-{alpha}.png'
    filepath = os.path.join(output_dir, filename)

    # Speichern des Plots
    plt.savefig(filepath)

    # Schließen des Plots, um den Speicher für den nächsten Plot freizugeben
    plt.close()

# Verzeichnis zum Speichern der Plots (z.B. 'plots')
output_dir = 'plots'

# Überprüfen, ob der Ordner existiert, falls nicht, dann erstellen
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for j in range(1,25,5):
    for k in range(1,100,5):
        for i in range(1,2000,100):
            generate_Sonar_plot(i,j,k)
            print(f"{i},{j},{k}")