# Copilot Instructions for Equalizador de Proyectos

## Project Overview

**Equalizador de Proyectos** is a 3D animation project estimation tool that calculates timeline and cost projections for animation productions. It uses a Tkinter GUI to collect project parameters and applies industry-standard estimation formulas based on content complexity, team composition, and production pipeline stages.

The tool estimates:
- Production time (days, weeks, months)
- Total cost based on team size and daily rates
- Resource allocation factors based on artist distribution across pre-production, production, and post-production phases

## Architecture & Key Components

### Core Estimation Model
The estimation engine uses a layered calculation approach:

1. **Base Time Calculation** ([Equalizador1.4.py](Equalizador1.4.py#L58)): Sums duration contributions from content elements
   - Assets: 1.5 days each
   - Props: 0.75 days each
   - Personajes (Characters): 2 days each
   - Environments: 6 days each
   - Episode duration (seconds/10): additional days
   - Reuse percentage: reduces time (reuso * 5 days subtracted)

2. **Difficulty Multiplier** ([Equalizador1.4.py](Equalizador1.4.py#L65-L67)): Projects with difficulty >7 add 5% overhead

3. **Team Distribution Factor** ([Equalizador1.4.py](Equalizador1.4.py#L48-L55)): Calculates efficiency gains from larger teams
   - Pre-production minimum: 3 (1 Concept, 1 Modelador, 1 Rigger)
   - Production minimum: 4 (1 Storyboard, 3 Animators)
   - Post-production minimum: 5 (2 Setup, 1 Render, 2 Compositing)
   - Global factor = average of three phase factors (adding more artists reduces time)

### Configuration Files

- [configuracion_proyecto.json](configuracion_proyecto.json): Template structure for project parameters including character types (main/secondary/incidental), environment tiers, asset categories, and global labor parameters (days/week, hours/day, contingency buffer)

### Version Evolution

- **Equalizador1.2.py**: Single episode analysis with basic asset/prop/character inputs
- **Equalizador1.3.py**: Multi-episode support and cost calculations
- **Equalizador1.4.py**: Full pipeline architecture with team role distribution and efficiency factors
- **Equalizador_de_Proyectos.py**: Radar chart visualization (different UI approach, non-parametric)

## Critical Developer Workflows

### Running the Application
```powershell
# Execute the latest version (1.4)
python Equalizador1.4.py

# Or for the radar chart variant
python Equalizador_de_Proyectos.py
```

### Adding New Estimation Parameters

1. Add field to GUI entry fields list (e.g., [lines 115-125](Equalizador1.4.py#L115-L125))
2. Create corresponding `entry_` variable assignment
3. Integrate into base_time calculation formula (line 58)
4. Update configuration template if it's a project-level parameter

### Modifying Time Coefficients

All time coefficients are hardcoded in the `base_time` calculation:
- Adjust individual multipliers (1.5 for assets, 2 for characters) for different production styles
- Contingency/difficulty multipliers compound - test edge cases (dificultad=10)
- Team factor calculation always normalizes to minimum values - changing minimums requires updates in three places (pre_min, prod_min, post_min)

## Project-Specific Patterns & Conventions

### Input Validation
- All numerical inputs require try-except blocks around `int()` and `float()` conversions
- Display errors via `messagebox.showerror()` rather than logging
- No negative values are explicitly prevented - add validation if needed

### Output Formatting
- Time displayed as: days (decimal), weeks (decimal), months (decimal)
- Currency shown as formatted string: f"${costo_total:.2f}"
- Factor values shown to 2 decimal places

### Tkinter Layout Pattern
- Grid layout with row tracking variable (`row`)
- Label in column 0, Entry in column 1
- Section headers use `font=("Arial", 10, "bold")` and `.grid(..., columnspan=2, pady=(10,5))`
- Default values inserted via `.insert(0, default_value)`

## Integration Points & Dependencies

### External Libraries
- **tkinter**: Standard GUI framework (Python bundled)
- **messagebox**: Modal dialogs for results and errors
- **numpy, matplotlib**: Required only for Equalizador_de_Proyectos.py radar charts

### No External Services
- All calculations are offline and deterministic
- No database connections or API calls
- JSON config is reference material only (not currently loaded at runtime)

## Common Maintenance Tasks

1. **Adjusting production coefficients**: Modify multipliers in base_time formula after gathering real project data
2. **Adding production phases**: Requires new team minimum constants and updates to global_factor calculation
3. **Extending for multiple seasons/series**: Current architecture supports episodios parameter - scale laterally rather than add new dimensions
4. **Validation improvements**: Wrap entry.get() calls in try-except and add range checking (0 < input < reasonable_max)

## Important Gotchas

- **Team factor behavior**: Adding MORE artists always REDUCES estimated time (counterintuitive in some scenarios). This reflects parallelization gains, not overhead.
- **Minimum values are hardcoded**: Changing team minimums in the coefficient calculation (lines 48-55) without updating the comparison logic breaks the efficiency model.
- **No persistence**: Application state is not saved between sessions. Consider implementing file I/O for saved project profiles.
