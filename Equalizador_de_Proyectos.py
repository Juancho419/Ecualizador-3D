import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definir parámetros detallados
parametros = {
    "Modelado": 5,
    "Rigging": 5,
    "Animación": 5,
    "Assets": 5,
    "Librerías": 5,
    "Tiempo": 5,
    "Equipo": 5,
    "Cliente": 5,
    "Render": 5
}

# Función para actualizar gráfico
def actualizar_grafico():
    valores = [sliders[key].get() for key in parametros]
    etiquetas = list(parametros.keys())

    # Crear figura de radar
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    
    # Cerrar la forma del gráfico
    valores += valores[:1]
    angulos += angulos[:1]

    ax.fill(angulos, valores, color='blue', alpha=0.3)
    ax.plot(angulos, valores, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas, fontsize=10)

    # Mostrar gráfico en la ventana
    canvas.figure = fig
    canvas.draw()

# Crear ventana
root = tk.Tk()
root.title("Ecualizador de Valoración de Proyectos 3D")

# Crear sliders
sliders = {}
for i, key in enumerate(parametros.keys()):
    ttk.Label(root, text=key).grid(row=i, column=0, padx=10, pady=5)
    sliders[key] = tk.Scale(root, from_=1, to=10, orient="horizontal", length=200, command=lambda x: actualizar_grafico())
    sliders[key].set(parametros[key])
    sliders[key].grid(row=i, column=1, padx=10, pady=5)

# Botón para actualizar el gráfico
ttk.Button(root, text="Actualizar Gráfico", command=actualizar_grafico).grid(row=len(parametros), column=0, columnspan=2, pady=10)

# Espacio para el gráfico
fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=len(parametros), padx=20)

# Mostrar ventana
actualizar_grafico()  # Dibujar gráfico inicial
root.mainloop()

