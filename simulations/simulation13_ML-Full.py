import numpy as np
import matplotlib.pyplot as plt
import os
import random
import cv2

# Fitness-Funktion
def calculate_antenna_gain(frequency,  sources, target_y=500):
    size_x = 500
    size_y = 1000
    c = 1500
    
    # Gitter
    x = np.linspace(0, size_x, size_x)
    y = np.linspace(0, size_y, size_y)
    X, Y = np.meshgrid(x, y)

    pressure = np.zeros_like(X)
    for sx, sy in sources:
        distance = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
        pressure += np.sin(2 * np.pi * frequency * distance / c)

    target_pressure = pressure[490:510, :]
    rest_pressure = pressure[0:490, :]
    max_pressure = np.max(target_pressure)/np.max(rest_pressure)

    return max_pressure

def genetic_algorithm(frequency,  generations=100, population_size=20, mutation_rate=1, output_dir='plots_video'):
    population = []  # Liste der aktuellen Population
    fitness_values = []  # Liste für die Fitnesswerte jeder Generation
    best_individual = None  # Beste Individuum
    
    # Initialisiere das erste Individuum auf einer horizontalen Linie mit gleichmäßigen Abständen
    spacing = 100  # Abstände der Quellen auf der X-Achse
    first_individual = [(spacing * i, 950) for i in range(5)]  # 5 Quellen, gleichmäßig entlang der X-Achse verteilt
    population.append(first_individual)

    # Initialisiere die anderen Individuen zufällig
    for _ in range(1, population_size):
        sources = [(spacing * i, 950) for i in range(5)]  # 5 Quellen pro Individuum
        population.append(sources)

    best_solution = None
    best_fitness = -np.inf

    # Video Setup
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Video Writer (XVID Codec und .avi Format)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_out = cv2.VideoWriter(os.path.join(output_dir, 'optimization_process.avi'), fourcc, 2.0, (1500, 1000))  # 2 fps, 500x1000 Auflösung

    # Evolution über Generationen
    for generation in range(generations):
        # Berechne Fitness für jedes 5er-Array (Individuum)
        fitness_values_gen = []
        for individual in population:
            fitness = calculate_antenna_gain(frequency,  individual)
            fitness_values_gen.append(fitness)

        # Speichern der Fitnesswerte für das Liniendiagramm
        fitness_values.append(max(fitness_values_gen))

        # Selektion: Tournament Selection (wählt 2 zufällige Individuen und das bessere wird übernommen)
        new_population = []
        for _ in range(population_size):
            # Tournament Selektion (2 zufällige Individuen)
            tournament = random.sample(population, 2)
            fitness_tournament = [calculate_antenna_gain(frequency,  individual) for individual in tournament]
            winner = tournament[np.argmax(fitness_tournament)]
            new_population.append(winner)

        # Crossover: Mischung der Quellenpositionen zweier Eltern
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = random.choice(new_population)
            parent2 = random.choice(new_population)
            child = crossover(parent1, parent2)  # Crossover der Eltern
            next_generation.append(child)

        # Mutationen auf die neue Generation anwenden
        for idx in range(len(next_generation)):
            if random.random() < mutation_rate:
                next_generation[idx] = mutate(next_generation[idx])  # Mutation anwenden

        # Elitismus: Das beste Individuum bleibt in der nächsten Generation
        best_individual_idx = np.argmax(fitness_values_gen)
        best_individual = population[best_individual_idx]
        next_generation[0] = best_individual  # Das Beste bleibt erhalten

        # Setze die neue Population
        population = next_generation

        # Visualisierung der besten Individuen
        plot_generation(frequency,  population, best_individual, generation, generations, output_dir, fitness_values)

        # Bild laden und auf Videoauflösung anpassen
        image = cv2.imread(os.path.join(output_dir, f'gen_{generation}.png'))
        image_resized = cv2.resize(image, (1500, 1000))  # Auflösung 500x1000
        video_out.write(image_resized)

        # Ausgabe der Fitness und der Quellenpositionen zur Kontrolle
        print(f"Generation {generation}: Beste Fitness = {best_fitness}")
        print(f"Beste Quellenpositionen: {best_individual}")

    # Video schließen
    video_out.release()
    print(f"Video gespeichert unter {os.path.join(output_dir, 'optimization_process.avi')}")


# Mutation angepasst auf kleine Verschiebungen entlang der Achsen
def mutate(individual):
    """Mutiert das Individuum, indem kleine Verschiebungen der Quellenpositionen vorgenommen werden."""
    mutated_individual = individual.copy()
    
    # Wähle eine zufällige Quelle aus, die verschoben werden soll
    source_to_mutate = random.randint(0, len(mutated_individual) - 1)
    
    # Kleine Verschiebung entlang der X-Achse (positive oder negative Verschiebung)
    x_shift = random.randint(-15, 15)  # Verschiebung in X-Richtung
    y_shift = random.randint(-15, 15)  # Verschiebung in Y-Richtung
    
    # Wende die Verschiebung an
    sx, sy = mutated_individual[source_to_mutate]
    new_source = (max(0, min(sx + x_shift, 500)), max(900, min(sy + y_shift, 1000)))  # Begrenzungen auf das Gitter
    
    mutated_individual[source_to_mutate] = new_source
    
    return mutated_individual



# Crossover: Mischung der Quellenpositionen zweier Eltern
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child



# Plot für die Generationen und Fitnesswerte
def plot_generation(frequency,  population, best_individual, generation, generations, output_dir, fitness_values):
    size_x = 500  # Breite des Gitters
    size_y = 1000  # Höhe des Gitters
    c = 1500  # Schallgeschwindigkeit in m/s

    # Gitter (mit der größeren y-Achse)
    x = np.linspace(0, size_x, size_x)
    y = np.linspace(0, size_y, size_y)
    X, Y = np.meshgrid(x, y)

    # Berechnung des Schalldrucks für jedes Individuum
    pressure = np.zeros_like(X)
    for individual in population:
        for source in individual:
            sx, sy = source
            distance = np.sqrt((X - sx) ** 2 + (Y - sy) ** 2)
            pressure += np.sin(2 * np.pi * frequency * distance / c)

    # Visualisierung: Erstelle den Hauptplot
    fig = plt.figure(figsize=(15, 10))

    # GridSpec für Subplots
    gs = fig.add_gridspec(2, 2, height_ratios=[0.8, 0.2], width_ratios=[0.5, 0.5])  # 2 Zeilen, 2 Spalten

    # Interferenzmuster im ersten Subplot (links oben)
    ax0 = fig.add_subplot(gs[:, 0])
    ctf = ax0.contourf(X, Y, pressure, levels=100, cmap='viridis')
    ax0.set_title(f'Interferenzmuster - Generation {generation}')
    ax0.set_xlabel('X-Position')
    ax0.set_ylabel('Y-Position')

    # Colorbar für den Schalldruckpegel
    cbar = plt.colorbar(ctf, ax=ax0)
    cbar.set_label('Schalldruckpegel')

    # Markiere alle Quellenpositionen (rote Punkte für das beste Individuum)
    for individual in population:
        source_x, source_y = zip(*individual)  # x und y Koordinaten der Quellen extrahieren
        if individual == best_individual:  # Beste Quelle in roter Farbe (Punkte)
            ax0.scatter(source_x, source_y, color='red', marker='o', s=100, label='Bestes Individuum', edgecolor='black')
        else:  # Andere Quellen in Kreuzform (grün)
            ax0.scatter(source_x, source_y, color='green', marker='x', s=100, label='Andere Individuen', alpha=0.5)

    # Polarplot für das beste Individuum (rechts oben)
    best_sources = best_individual
    angles = np.linspace(0, 2 * np.pi, 360)  # 360 Winkel für den Polarplot
    intensities = np.zeros_like(angles)

    for idx, angle in enumerate(angles):
        # Berechne die Intensität entlang des gegebenen Winkels
        intensity = 0
        for sx, sy in best_sources:
            # Berechne die Position der Quelle im Polarwinkel
            distance = np.sqrt(sx**2 + sy**2)
            projected_distance = np.sqrt(sx**2 + sy**2) * np.cos(angle - np.arctan2(sy, sx))
            intensity += np.abs(np.sin(2 * np.pi * frequency * projected_distance / c))
        intensities[idx] = intensity

    # Polarplot erstellen
    ax_polar = fig.add_subplot(gs[0, 1], polar=True)  # Position des Polarplots oben rechts
    ax_polar.set_theta_direction(-1)  # Drehen der Winkelrichtung im Uhrzeigersinn
    ax_polar.set_theta_offset(np.pi / 2)  # 0° auf den oberen Rand setzen
    ax_polar.plot(angles, intensities, color='purple', linewidth=1.5)
    ax_polar.set_title(f'Polarplot - Beste Quelle - Generation {generation}')
    ax_polar.set_xlabel('Winkel (radians)')
    ax_polar.set_ylabel('Intensität')

    # Liniendiagramm für die Fitnesswerte im zweiten Subplot (links unten)
    ax1 = fig.add_subplot(gs[1, 1])  # Fitness-Plot über beide Spalten (gesamte Breite)
    ax1.plot(range(generation + 1), fitness_values, color='blue', marker='o')
    ax1.set_title('Fitness-Entwicklung über die Generationen')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Fitness')
    ax1.set_xlim(0, generations - 1)  # X-Achse über alle Generationen anpassen

    # Manuelle Anpassung des Layouts (kein tight_layout)
    fig.subplots_adjust(hspace=0.4, wspace=0.3)

    # Speichern des Plots
    filename = f'gen_{generation}.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()



# Beispielaufruf des genetischen Algorithmus für verschiedene Frequenzen und Abstandsfaktoren
frequency = 10  # Frequenz in kHz, festgelegt

genetic_algorithm(frequency)
