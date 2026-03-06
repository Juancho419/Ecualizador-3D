import tkinter as tk
from tkinter import messagebox

def analizar_proyecto():
    try:
        # Obtener valores ingresados
        episodios = int(entry_episodios.get())
        duracion_episodio = int(entry_duracion.get())  # en segundos
        assets = int(entry_assets.get())
        props = int(entry_props.get())
        personajes = int(entry_personajes.get())
        reuso = float(entry_reuso.get()) / 100  # convertir de porcentaje a decimal
        calidad = int(entry_calidad.get())
        costo_diario = float(entry_costo.get())

        # Parámetros base
        dias_semana = 5

        # Estimación base para UN episodio:
        # Por ejemplo, asumimos:
        # - Cada asset suma 1.5 días de trabajo.
        # - Cada prop suma 0.75 días.
        # - Cada personaje suma 2 días.
        # - La duración del episodio (en segundos) se divide por 10 para obtener días adicionales.
        # - El porcentaje de reuso reduce el tiempo (reuso * 5 días).
        # - Se divide por la calidad (mayor calidad reduce el tiempo, en este ejemplo).
        tiempo_por_episodio = (assets * 1.5 + props * 0.75 + personajes * 2 + (duracion_episodio / 10) - (reuso * 5)) / calidad
        if tiempo_por_episodio < 1:
            tiempo_por_episodio = 1  # mínimo de 1 día por episodio

        # Tiempo total del proyecto
        tiempo_total_dias = episodios * tiempo_por_episodio
        tiempo_total_semanas = tiempo_total_dias / dias_semana
        tiempo_total_meses = tiempo_total_semanas / 4  # aproximación

        # Estimar personal requerido (ejemplo: 1 artista por cada 10 elementos, mínimo 1)
        personal_estimado = max(1, int((assets + props + personajes) / 10))

        # Costo total = tiempo total en días * costo diario * cantidad de artistas
        costo_total = tiempo_total_dias * costo_diario * personal_estimado

        # Mostrar resultados
        resultado = (
            f"Tiempo Estimado del Proyecto:\n"
            f"  {tiempo_total_dias:.1f} días\n"
            f"  {tiempo_total_semanas:.1f} semanas\n"
            f"  {tiempo_total_meses:.1f} meses\n\n"
            f"Costo Estimado: ${costo_total:.2f}"
        )
        messagebox.showinfo("Análisis de Proyecto", resultado)
    except Exception as e:
        messagebox.showerror("Error", f"Error en el análisis: {e}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Ecualizador de Proyectos 3D - Análisis Detallado")

# Lista de campos a solicitar
labels_text = [
    "Cantidad de Episodios:",
    "Duración del Episodio (segundos):",
    "Cantidad de Assets:",
    "Cantidad de Props:",
    "Cantidad de Personajes:",
    "Porcentaje de Reuso (%):",
    "Calidad del Proyecto (1-10):",
    "Costo diario por artista ($):"
]

entries = []
for i, text in enumerate(labels_text):
    label = tk.Label(root, text=text)
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

# Asignar cada entrada a una variable
entry_episodios, entry_duracion, entry_assets, entry_props, entry_personajes, entry_reuso, entry_calidad, entry_costo = entries

# Valores por defecto (puedes ajustarlos según tus necesidades)
entry_episodios.insert(0, "1")
entry_duracion.insert(0, "120")         # 120 segundos = 2 minutos
entry_assets.insert(0, "100")
entry_props.insert(0, "30")
entry_personajes.insert(0, "30")
entry_reuso.insert(0, "0")
entry_calidad.insert(0, "5")
entry_costo.insert(0, "150")

# Botón para analizar el proyecto
btn_analizar = tk.Button(root, text="ANALIZAR", command=analizar_proyecto)
btn_analizar.grid(row=len(labels_text), column=0, columnspan=2, padx=5, pady=10)

root.mainloop()
