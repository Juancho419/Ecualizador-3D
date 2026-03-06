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

