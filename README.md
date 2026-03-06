# 3D Animation Project Estimator

A desktop tool for estimating production time and costs for 3D animation projects, built with Python and tkinter.

## Current Version: 1.5

### What's new in v1.5
- Full pipeline modeled: Script Breakdown → Pre-production → Animatic → Layout → Spline → Online
- Animation calculated from real frame data (159 frames/animator/day at 25fps)
- Cost per team: each department is billed only for their active days, not the full project duration
- Animation teams are configurable (number of teams × animators per team)
- Client feedback rounds included: 2 rounds per phase × 3 days each
- Pre-production coefficients locked by default, editable via checkbox
- Assets entered directly by type (props, characters, environments)

## Requirements
- Python 3.13+
- tkinter (included with Python)

## How to run
```
python Equalizador1.5.py
```

## Pipeline model

| Phase | Detail |
|-------|---------|
| Script breakdown | 3 days per block of 2 episodes |
| Pre-production | Based on assets × coefficients |
| Animatic | V1 + Client FL(3d) + V2 + Client FL(3d) |
| Layout | L + Client FL(3d) |
| Spline | S1 + Client FL(3d) + S2 + Client FL(3d) |
| Online | O1 + Client FL(3d) + O2 + Client FL(3d) |

## Team entry schedule

| Team | Starts | Ends |
|------|--------|------|
| Pre-production | Day 0 | When assets are done |
| Animatic | Day 10 | When their phase ends |
| Animators | After 2 approved animatic blocks | After last Spline V2 |
| Online | When O1 starts | After last approval |

## Real production metrics used
- 159 frames per animator per day (based on real project data)
- 5.2 days per episode for Animatic V1
- 15 days per episode for Online (team of 3)
- Layout quota: 40% less than animation
- Blocks of 2 simultaneous episodes throughout production


# ESPAÑOL

# Ecualizador de Proyectos 3D

Herramienta de estimación de tiempos y costos para proyectos de animación 3D.

## Versión actual: 1.5

### Cambios respecto a versiones anteriores
- Pipeline completo: Guión → Pre-producción → Animatic → Layout → Spline → Online
- Cálculo de animación basado en frames reales (159 frames/animador/día a 25fps)
- Costo por equipo: cada área cobra solo sus días activos, no el total del proyecto
- Equipos de animación configurables (número de equipos × animadores por equipo)
- Revisiones de cliente incluidas: 2 rondas por fase × 3 días cada una
- Coeficientes de pre-producción bloqueados por defecto, editables con checkbox
- Assets ingresados directamente por tipo (props, personajes, environments)

## Requisitos
- Python 3.13+
- tkinter (incluido en Python)

## Cómo ejecutar
```
python Equalizador1.5.py
```

## Pipeline modelado
| Fase | Detalle |
|------|---------|
| Desglose guión | 3 días por bloque de 2 episodios |
| Pre-producción | Según assets × coeficientes |
| Animatic | V1 + FL(3d) + V2 + FL(3d) |
| Layout | L + FL(3d) |
| Spline | S1 + FL(3d) + S2 + FL(3d) |
| Online | O1 + FL(3d) + O2 + FL(3d) |
```

