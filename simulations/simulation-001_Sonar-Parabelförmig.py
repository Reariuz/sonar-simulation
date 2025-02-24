import numpy as np 
import matplotlib.pyplot as plt 

## Parameter
size = 200 # grid Zise
Wavelength = 50
c =1500 #Schallgeschwindigkeit m/s
frequency = 1000 # Frequenz in Mhz

# Parameter für die Parabel
a = 0.02  # Steigung der Parabel (je größer, desto enger ist die Parabel)
h = 50  # Scheitelpunkt x-Koordinate
k = 40  # Scheitelpunkt y-Koordinate

# Abstände der Punkte entlang der x-Achse (die x-Werte)
y_distances = [-50,-25,0,25,50]  # Die x-Positionen der Punkte

# Generierung der x-Werte basierend auf der Parabelgleichung
sources = [(a * (y)**2 +h , y + k*2) for y in y_distances]
print(sources)

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

# Quellen als Kreise im Plot anzeigen
source_x, source_y = zip(*sources)  # x und y Koordinaten der Quellen extrahieren
plt.scatter(source_x, source_y, color='red', marker='o', s=100, label='Quellen')


plt.show()