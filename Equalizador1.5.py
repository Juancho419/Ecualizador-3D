import tkinter as tk
from tkinter import messagebox
from math import ceil

# ─────────────────────────────────────────────
# CONSTANTES DEL PIPELINE
# ─────────────────────────────────────────────
FRAMES_POR_ANIMADOR_DIA  = 159    # Métrica real
FACTOR_LAYOUT            = 0.60   # Layout = 60% cuota animación
DIAS_ANIMATIC_V1         = 5.2    # Métrica real por episodio
DIAS_ONLINE_POR_EP       = 15     # Métrica real: equipo de 3
DIAS_DESGLOSE_GUION      = 3      # Por bloque de 2 episodios
DIAS_FL_CLIENTE          = 3      # Ronda de feedback cliente
EPISODIOS_EN_PARALELO    = 2      # Bloques simultáneos
ARTISTAS_ONLINE_BASE     = 3      # Equipo estándar online
DIAS_ENTRADA_ANIMATIC    = 10     # Animatic entra 2 semanas después de pre-pro
BLOQUES_PARA_ANIMADORES  = 2      # Animadores entran con 2 bloques animatic aprobados


# ─────────────────────────────────────────────
# FUNCIONES DE CÁLCULO POR FASE
# ─────────────────────────────────────────────

def calc_guion(episodios):
    bloques = ceil(episodios / EPISODIOS_EN_PARALELO)
    return bloques * DIAS_DESGLOSE_GUION


def calc_preproduccion(props, personajes, environments,
                       dias_prop, dias_personaje, dias_environment,
                       modeladores, riggers):
    artistas = modeladores + riggers
    if artistas == 0:
        return 0
    dias_trabajo = (
        props        * dias_prop +
        personajes   * dias_personaje +
        environments * dias_environment
    )
    return dias_trabajo / artistas


def calc_animatic(episodios):
    """V1 → FL(3d) → V2(50%) → FL(3d) por bloque."""
    bloques = ceil(episodios / EPISODIOS_EN_PARALELO)
    trabajo = bloques * (DIAS_ANIMATIC_V1 + DIAS_ANIMATIC_V1 * 0.50)
    fl      = bloques * 2 * DIAS_FL_CLIENTE
    return trabajo, fl, trabajo + fl


def calc_layout(episodios, duracion_seg, animadores_total):
    """Layout → FL(3d). Usa el total de animadores."""
    if animadores_total == 0:
        return 0, 0, 0
    frames  = duracion_seg * 25 * episodios
    trabajo = frames / (FRAMES_POR_ANIMADOR_DIA * FACTOR_LAYOUT * animadores_total)
    bloques = ceil(episodios / EPISODIOS_EN_PARALELO)
    fl      = bloques * DIAS_FL_CLIENTE
    return trabajo, fl, trabajo + fl


def calc_spline(episodios, duracion_seg, animadores_total):
    """S1 → FL(3d) → S2(50%) → FL(3d) por bloque."""
    if animadores_total == 0:
        return 0, 0, 0
    frames  = duracion_seg * 25 * episodios
    s1      = frames / (FRAMES_POR_ANIMADOR_DIA * animadores_total)
    s2      = s1 * 0.50
    trabajo = s1 + s2
    bloques = ceil(episodios / EPISODIOS_EN_PARALELO)
    fl      = bloques * 2 * DIAS_FL_CLIENTE
    return trabajo, fl, trabajo + fl


def calc_online(episodios, artistas_online):
    """O1 → FL(3d) → O2(50%) → FL(3d) = approval."""
    if artistas_online == 0:
        return 0, 0, 0
    factor        = ARTISTAS_ONLINE_BASE / artistas_online
    o1_por_bloque = DIAS_ONLINE_POR_EP * factor
    o2_por_bloque = o1_por_bloque * 0.50
    bloques       = ceil(episodios / EPISODIOS_EN_PARALELO)
    trabajo       = bloques * (o1_por_bloque + o2_por_bloque)
    fl            = bloques * 2 * DIAS_FL_CLIENTE
    return trabajo, fl, trabajo + fl


# ─────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────

def analizar_proyecto():
    try:
        # ── Parámetros ──
        episodios    = int(entry_episodios.get())
        duracion_seg = int(entry_duracion.get())
        props        = int(entry_props.get())
        personajes   = int(entry_personajes.get())
        environments = int(entry_environments.get())
        costo_diario = float(entry_costo.get())
        dias_prop        = float(entry_dias_prop.get())
        dias_personaje   = float(entry_dias_personaje.get())
        dias_environment = float(entry_dias_environment.get())
        modeladores       = int(entry_modeladores.get())
        riggers           = int(entry_riggers.get())
        artistas_animatic = int(entry_animatic.get())
        equipos_anim      = int(entry_equipos_anim.get())
        anim_por_equipo   = int(entry_anim_por_equipo.get())
        artistas_online   = int(entry_online.get())

        # Total de animadores = equipos × animadores por equipo
        animadores_total = equipos_anim * anim_por_equipo

        # ── Cálculo por fase ──
        dias_guion   = calc_guion(episodios)
        dias_pre     = calc_preproduccion(
            props, personajes, environments,
            dias_prop, dias_personaje, dias_environment,
            modeladores, riggers
        )

        anim_trab,   anim_fl,   anim_total   = calc_animatic(episodios)
        layout_trab, layout_fl, layout_total = calc_layout(episodios, duracion_seg, animadores_total)
        spline_trab, spline_fl, spline_total = calc_spline(episodios, duracion_seg, animadores_total)
        online_trab, online_fl, online_total = calc_online(episodios, artistas_online)

        # ── Timeline total ──
        overlap      = min(DIAS_ENTRADA_ANIMATIC, dias_pre)
        dias_totales = (
            dias_guion   +
            dias_pre     +
            anim_total   +
            layout_total +
            spline_total +
            online_total -
            overlap
        )
        semanas = dias_totales / 5
        meses   = semanas / 4

        # ── Costo por equipo (solo días activos) ──
        costo_pre = dias_pre * (modeladores + riggers) * costo_diario

        costo_animatic = anim_total * artistas_animatic * costo_diario

        bloques = ceil(episodios / EPISODIOS_EN_PARALELO)
        dias_por_bloque_animatic = anim_total / bloques
        dias_espera_animadores   = BLOQUES_PARA_ANIMADORES * dias_por_bloque_animatic
        dias_activos_animadores  = max(0, (anim_total - dias_espera_animadores) + layout_total + spline_total)
        costo_animadores = dias_activos_animadores * animadores_total * costo_diario

        costo_online = online_total * artistas_online * costo_diario

        costo_total = costo_pre + costo_animatic + costo_animadores + costo_online

        # ── Resultado ──
        resultado = (
            f"TIMELINE POR FASE\n"
            f"{'─'*46}\n"
            f"  Desglose guión:           {dias_guion:.1f} días\n"
            f"  Pre-producción:           {dias_pre:.1f} días\n"
            f"  Animatic (V1+FL+V2+FL):   {anim_total:.1f} días\n"
            f"    trabajo: {anim_trab:.1f}d  |  FL cliente: {anim_fl:.1f}d\n"
            f"  Layout (+FL):             {layout_total:.1f} días\n"
            f"    trabajo: {layout_trab:.1f}d  |  FL cliente: {layout_fl:.1f}d\n"
            f"  Spline (S1+FL+S2+FL):     {spline_total:.1f} días\n"
            f"    trabajo: {spline_trab:.1f}d  |  FL cliente: {spline_fl:.1f}d\n"
            f"  Online (O1+FL+O2+FL):     {online_total:.1f} días\n"
            f"    trabajo: {online_trab:.1f}d  |  FL cliente: {online_fl:.1f}d\n"
            f"  Overlap animatic/pre-pro: -{overlap:.1f} días\n"
            f"{'─'*46}\n"
            f"TIEMPO TOTAL\n"
            f"  {dias_totales:.1f} días laborables\n"
            f"  {semanas:.1f} semanas\n"
            f"  {meses:.1f} meses\n\n"
            f"ASSETS A PRODUCIR\n"
            f"  Props: {props}  |  Personajes: {personajes}  |  Environments: {environments}\n\n"
            f"EQUIPO DE ANIMACIÓN\n"
            f"  {equipos_anim} equipos × {anim_por_equipo} animadores = {animadores_total} animadores en total\n\n"
            f"COSTO POR EQUIPO\n"
            f"{'─'*46}\n"
            f"  Pre-producción ({modeladores+riggers} artistas):    ${costo_pre:>10,.2f}\n"
            f"  Animatic ({artistas_animatic} artistas):             ${costo_animatic:>10,.2f}\n"
            f"  Animadores ({animadores_total} en {equipos_anim} equipos):   ${costo_animadores:>10,.2f}\n"
            f"  Online ({artistas_online} artistas):                ${costo_online:>10,.2f}\n"
            f"{'─'*46}\n"
            f"  TOTAL:                    ${costo_total:>10,.2f} USD"
        )
        messagebox.showinfo("Análisis de Proyecto", resultado)

    except ValueError:
        messagebox.showerror("Error", "Verifica que todos los campos tengan valores numéricos válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")


# ─────────────────────────────────────────────
# INTERFAZ
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("Ecualizador de Proyectos 3D v1.5")
root.resizable(False, False)

def seccion(texto, fila):
    tk.Label(root, text=texto, font=("Arial", 10, "bold"), fg="#333").grid(
        row=fila, column=0, columnspan=2, pady=(12, 4), sticky="w", padx=10
    )

def campo(etiqueta, default, fila):
    tk.Label(root, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=10, pady=3)
    entry = tk.Entry(root, width=10)
    entry.grid(row=fila, column=1, padx=10, pady=3, sticky="w")
    entry.insert(0, default)
    return entry

row = 0

# ── Proyecto ──
seccion("PROYECTO", row); row += 1
entry_episodios = campo("Cantidad de episodios:", "12", row); row += 1
entry_duracion  = campo("Duración por episodio (segundos):", "120", row); row += 1

# ── Assets ──
seccion("ASSETS A PRODUCIR POR EL ESTUDIO", row); row += 1
entry_props        = campo("Props:", "8", row); row += 1
entry_personajes   = campo("Personajes:", "4", row); row += 1
entry_environments = campo("Environments:", "3", row); row += 1

# ── Costo ──
seccion("COSTO", row); row += 1
entry_costo = campo("Costo diario por artista (USD $):", "100", row); row += 1

# ── Coeficientes (bloqueados por defecto) ──
var_editar = tk.BooleanVar(value=False)
seccion("COEFICIENTES PRE-PRODUCCIÓN (días por unidad)", row); row += 1

frame_chk = tk.Frame(root)
frame_chk.grid(row=row, column=0, columnspan=2, sticky="w", padx=10)
tk.Label(frame_chk, text="✎ Editar coeficientes", fg="#2c6fad",
         font=("Arial", 9, "underline")).pack(side="left")
tk.Checkbutton(frame_chk, variable=var_editar).pack(side="left")
row += 1

entry_dias_prop        = campo("Días por prop:", "0.75", row); row += 1
entry_dias_personaje   = campo("Días por personaje:", "2.0", row); row += 1
entry_dias_environment = campo("Días por environment:", "6.0", row); row += 1

def toggle_coeficientes(*args):
    state = "normal" if var_editar.get() else "disabled"
    for e in [entry_dias_prop, entry_dias_personaje, entry_dias_environment]:
        e.config(state=state, disabledbackground="#f0f0f0")

var_editar.trace_add("write", toggle_coeficientes)
toggle_coeficientes()

# ── Personal ──
seccion("PERSONAL POR ÁREA", row); row += 1
entry_modeladores    = campo("Modeladores:", "2", row); row += 1
entry_riggers        = campo("Riggers:", "1", row); row += 1
entry_animatic       = campo("Artistas de Animatic:", "2", row); row += 1

# Animadores: dos campos separados
tk.Label(root, text="Equipos de animación:", ).grid(row=row, column=0, sticky="w", padx=10, pady=3)
entry_equipos_anim = tk.Entry(root, width=10)
entry_equipos_anim.grid(row=row, column=1, padx=10, pady=3, sticky="w")
entry_equipos_anim.insert(0, "2")
row += 1

tk.Label(root, text="Animadores por equipo:").grid(row=row, column=0, sticky="w", padx=10, pady=3)
entry_anim_por_equipo = tk.Entry(root, width=10)
entry_anim_por_equipo.grid(row=row, column=1, padx=10, pady=3, sticky="w")
entry_anim_por_equipo.insert(0, "3")
row += 1

# Label dinámico que muestra el total
lbl_total_anim = tk.Label(root, text="→ Total animadores: 6", fg="#2c6fad", font=("Arial", 9))
lbl_total_anim.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 4))
row += 1

def actualizar_total_anim(*args):
    try:
        total = int(entry_equipos_anim.get()) * int(entry_anim_por_equipo.get())
        lbl_total_anim.config(text=f"→ Total animadores: {total}")
    except ValueError:
        lbl_total_anim.config(text="→ Total animadores: -")

entry_equipos_anim.bind("<KeyRelease>", actualizar_total_anim)
entry_anim_por_equipo.bind("<KeyRelease>", actualizar_total_anim)

entry_online = campo("Artistas Online (lighting/compo/render):", "3", row); row += 1

tk.Label(root, text="* Coordinación, supervisión y dirección no incluidos",
         font=("Arial", 8), fg="#888").grid(
    row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 4))
row += 1

# ── Botón ──
tk.Button(
    root, text="ANALIZAR PROYECTO",
    command=analizar_proyecto,
    font=("Arial", 10, "bold"),
    bg="#2c6fad", fg="white", padx=10, pady=6
).grid(row=row, column=0, columnspan=2, pady=15)

root.mainloop()