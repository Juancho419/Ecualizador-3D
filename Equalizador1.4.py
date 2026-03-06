import tkinter as tk
from tkinter import messagebox

def analizar_proyecto():
    try:
        # Parámetros generales del proyecto
        episodios = int(entry_episodios.get())
        duracion_episodio = int(entry_duracion.get())  # en segundos
        assets = int(entry_assets.get())
        props = int(entry_props.get())
        personajes = int(entry_personajes.get())
        environments = int(entry_environments.get())
        reuso = float(entry_reuso.get()) / 100  # convertir porcentaje a decimal
        dificultad = int(entry_dificultad.get())
        costo_diario = float(entry_costo.get())

        # Sección de artistas (distribución por áreas)
        # Pre-producción: Concept, Modelador, Rigger (mínimo total 3)
        pre_concept = int(entry_pre_concept.get())
        pre_modelador = int(entry_pre_modelador.get())
        pre_rigger = int(entry_pre_rigger.get())
        pre_total = pre_concept + pre_modelador + pre_rigger

        # Producción: Storyboard y Animadores (mínimo 1 + 3 = 4)
        prod_storyboard = int(entry_prod_storyboard.get())
        prod_animadores = int(entry_prod_animadores.get())
        prod_total = prod_storyboard + prod_animadores

        # Postproducción: Set up render, Render y Compo (mínimo 2 + 1 + 2 = 5)
        post_setup = int(entry_post_setup.get())
        post_render = int(entry_post_render.get())
        post_compo = int(entry_post_compo.get())
        post_total = post_setup + post_render + post_compo

        # Valores mínimos requeridos (para determinar el factor de reducción, si se agregan más artistas se reduce el tiempo)
        pre_min = 3
        prod_min = 4
        post_min = 5

        factor_pre = pre_min / pre_total if pre_total > 0 else 1
        factor_prod = prod_min / prod_total if prod_total > 0 else 1
        factor_post = post_min / post_total if post_total > 0 else 1

        # Factor global: Promedio de los tres factores (si hay más artistas en alguna área, el factor baja)
        global_factor = (factor_pre + factor_prod + factor_post) / 3

        # Cálculo base del tiempo para un episodio (en días) a partir de parámetros de contenido.
        # Se suman:
        # - Assets: cada uno suma 1.5 días.
        # - Props: cada uno suma 0.75 días.
        # - Personajes: cada uno suma 2 días.
        # - Environments: cada uno suma 6 días (triple que un personaje).
        # - La duración del episodio (dividida por 10) añade días adicionales.
        # - Se resta un valor proporcional al porcentaje de reuso.
        base_time = (assets * 1.5 + props * 0.75 + personajes * 2 + environments * 6 + (duracion_episodio / 10) - (reuso * 5))
        
        # Aplicar el efecto de la dificultad: 
        # En este modelo, si la dificultad es mayor a 7 se suma un 5% extra a los tiempos (y por ende, a los costos).
        if dificultad > 7:
            base_time *= 1.05

        # El tiempo por episodio se reduce en función del factor global derivado de la distribución de artistas
        tiempo_por_episodio = base_time * global_factor
        if tiempo_por_episodio < 1:
            tiempo_por_episodio = 1  # al menos 1 día por episodio

        # Tiempo total del proyecto
        tiempo_total_dias = episodios * tiempo_por_episodio
        tiempo_total_semanas = tiempo_total_dias / 5  # asumiendo 5 días laborables por semana
        tiempo_total_meses = tiempo_total_semanas / 4  # aproximado

        # Estimación de personal (solo suma artistas en áreas que afectan producción)
        personal_estimado = pre_total + prod_total + post_total

        # Costo total: se multiplica el tiempo total (en días) por el costo diario y la cantidad de artistas (roles fijos no inciden)
        costo_total = tiempo_total_dias * costo_diario * personal_estimado

        resultado = (
            f"Tiempo Estimado del Proyecto:\n"
            f"  {tiempo_total_dias:.1f} días\n"
            f"  {tiempo_total_semanas:.1f} semanas\n"
            f"  {tiempo_total_meses:.1f} meses\n\n"
            f"Costo Estimado: ${costo_total:.2f}\n\n"
            f"Factor Global de Reducción (por personal): {global_factor:.2f}"
        )
        messagebox.showinfo("Análisis de Proyecto", resultado)
    except Exception as e:
        messagebox.showerror("Error", f"Error en el análisis: {e}")

root = tk.Tk()
root.title("Ecualizador de Proyectos 3D - Análisis Detallado")

row = 0
# Campos generales
fields_overall = [
    ("Cantidad de Episodios:", "1"),
    ("Duración del Episodio (segundos):", "120"),
    ("Cantidad de Assets:", "100"),
    ("Cantidad de Props:", "30"),
    ("Cantidad de Personajes:", "30"),
    ("Cantidad de Environments:", "10"),
    ("Porcentaje de Reuso (%):", "0"),
    ("Dificultad del Proyecto (1-10):", "5"),
    ("Costo diario por artista ($):", "150")
]
entries_overall = {}
for text, default in fields_overall:
    tk.Label(root, text=text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entry.insert(0, default)
    entries_overall[text] = entry
    row += 1

entry_episodios = entries_overall["Cantidad de Episodios:"]
entry_duracion = entries_overall["Duración del Episodio (segundos):"]
entry_assets = entries_overall["Cantidad de Assets:"]
entry_props = entries_overall["Cantidad de Props:"]
entry_personajes = entries_overall["Cantidad de Personajes:"]
entry_environments = entries_overall["Cantidad de Environments:"]
entry_reuso = entries_overall["Porcentaje de Reuso (%):"]
entry_dificultad = entries_overall["Dificultad del Proyecto (1-10):"]
entry_costo = entries_overall["Costo diario por artista ($):"]

# Sección: Pre-producción (mínimo: 1 Concept, 1 Modelador, 1 Rigger => Total 3)
tk.Label(root, text="--- Pre-Producción ---", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,5))
row += 1
fields_pre = [
    ("Concept Artists (mínimo 1):", "1"),
    ("Modelador Artists (mínimo 1):", "1"),
    ("Riggers (mínimo 1):", "1")
]
entries_pre = {}
for text, default in fields_pre:
    tk.Label(root, text=text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entry.insert(0, default)
    entries_pre[text] = entry
    row += 1

entry_pre_concept = entries_pre["Concept Artists (mínimo 1):"]
entry_pre_modelador = entries_pre["Modelador Artists (mínimo 1):"]
entry_pre_rigger = entries_pre["Riggers (mínimo 1):"]

# Sección: Producción (mínimo: 1 Storyboard + 3 Animadores = 4)
tk.Label(root, text="--- Producción ---", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,5))
row += 1
fields_prod = [
    ("Storyboard (mínimo 1):", "1"),
    ("Animadores (mínimo 3):", "3")
]
entries_prod = {}
for text, default in fields_prod:
    tk.Label(root, text=text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entry.insert(0, default)
    entries_prod[text] = entry
    row += 1

entry_prod_storyboard = entries_prod["Storyboard (mínimo 1):"]
entry_prod_animadores = entries_prod["Animadores (mínimo 3):"]

# Sección: Postproducción (mínimo: 2 Set up render, 1 Render, 2 Compo = 5)
tk.Label(root, text="--- Postproducción ---", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=(10,5))
row += 1
fields_post = [
    ("Set up render (mínimo 2):", "2"),
    ("Render (mínimo 1):", "1"),
    ("Compo (mínimo 2):", "2")
]
entries_post = {}
for text, default in fields_post:
    tk.Label(root, text=text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1, padx=5, pady=5)
    entry.insert(0, default)
    entries_post[text] = entry
    row += 1

entry_post_setup = entries_post["Set up render (mínimo 2):"]
entry_post_render = entries_post["Render (mínimo 1):"]
entry_post_compo = entries_post["Compo (mínimo 2):"]

# Información adicional: Roles fijos (Coordinador, Supervisor, Directores) no afectan la reducción de tiempo.
tk.Label(root, text="(Roles fijos: Coordinador, Supervisor, Director de Proyecto y Director de Producción)").grid(row=row, column=0, columnspan=2, pady=(10,5))
row += 1

# Botón para analizar el proyecto
btn_analizar = tk.Button(root, text="ANALIZAR", command=analizar_proyecto)
btn_analizar.grid(row=row, column=0, columnspan=2, pady=10)

root.mainloop()
