import tkinter as tk
from tkinter import messagebox

# Función para calcular tiempo de producción y costo
def analizar_proyecto():
    try:
        # Obtener valores ingresados por el usuario
        assets = int(entry_assets.get())
        props = int(entry_props.get())
        personajes = int(entry_personajes.get())
        reuso = float(entry_reuso.get()) / 100  # Convertir porcentaje a decimal
        calidad = int(entry_calidad.get())  # Rango de 1 a 10
        duracion_segundos = int(entry_duracion.get())  # Duración en segundos
        
        # Parámetros base
        horas_dia = 7.5
        dias_semana = 5
        semanas_mes = 4
        
        # Fórmula de estimación de tiempo (ajustar según el tipo de producción)
        tiempo_estimado_dias = (
            (assets * 1.5) + (props * 0.75) + (personajes * 2) +
            (duracion_segundos / 10) - (reuso * 5)
        ) / calidad

        if tiempo_estimado_dias < 1:
            tiempo_estimado_dias = 1  # Mínimo 1 día de producción
        
        tiempo_estimado_semanas = tiempo_estimado_dias / dias_semana
        tiempo_estimado_meses = tiempo_estimado_semanas / semanas_mes
        
        # Costo estimado (ejemplo: $150 por artista por día)
        costo_diario_por_artista = 150
        personal_estimado = max(1, int((assets + props + personajes) / 10))  # Mínimo 1 persona
        
        costo_total = tiempo_estimado_dias * costo_diario_por_artista * personal_estimado
        
        # Mostrar resultados
        resultado = f"""
        📌 Tiempo Estimado:
        - {round(tiempo_estimado_dias, 1)} días
        - {round(tiempo_estimado_semanas, 1)} semanas
        - {round(tiempo_estimado_meses, 1)} meses
        
        💰 Costo Estimado: ${round(costo_total, 2)}
        """
        messagebox.showinfo("Análisis de Proyecto", resultado)
    
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Crear interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Ecualizador de Proyectos 3D")

# Campos de entrada
tk.Label(root, text="Cantidad de Assets:").pack()
entry_assets = tk.Entry(root)
entry_assets.pack()

tk.Label(root, text="Cantidad de Props:").pack()
entry_props = tk.Entry(root)
entry_props.pack()

tk.Label(root, text="Cantidad de Personajes:").pack()
entry_personajes = tk.Entry(root)
entry_personajes.pack()

tk.Label(root, text="Porcentaje de Reuso (%):").pack()
entry_reuso = tk.Entry(root)
entry_reuso.pack()

tk.Label(root, text="Calidad del Proyecto (1-10):").pack()
entry_calidad = tk.Entry(root)
entry_calidad.pack()

tk.Label(root, text="Duración del Episodio (segundos):").pack()
entry_duracion = tk.Entry(root)
entry_duracion.pack()

# Botón para analizar el proyecto
btn_analizar = tk.Button(root, text="ANALIZAR", command=analizar_proyecto)
btn_analizar.pack()

# Ejecutar interfaz gráfica
root.mainloop()
