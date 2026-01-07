# Adaptive and Recursive Modular Habitats for Mars

**Researcher:** Md Sazzad Islam  
**Paper Status:** In preparation (2026)  
**Tools:** Python (GhPython), Rhino 3D, Grasshopper

## Overview
This repository contains the core **Growth Solver algorithm** developed for the research paper *"Adaptive and Recursive Modular Habitats for Sustainable Growth on Mars."* The script creates a self-organizing habitat cluster that adapts to Martian terrain (derived from HiRISE data) in real-time. It mimics biological morphogenesis, prioritizing solar exposure while strictly adhering to safety constraints.

## The Algorithm
The solver is an **Iterative Agent-Based System** that operates on three primary heuristics:

1.  **Terrain Analysis:** Checks surface normals to ensure slope < 30° (rover/module limit).
2.  **Heliotropism (Solar Seeking):** Uses Vector Dot Products to weigh potential growth directions against the incident solar angle.
3.  **Stochastic Branching:** Implements a backtracking routine. When a "branch" of modules hits an obstacle (steep slope or collision), the agent randomly reactivates a previous module to start a new branch, similar to auxiliary budding in plants.

## Usage
1.  Open `src/mars_habitat.gh` in Rhino 7/8.
2.  Input a Mesh into the "Terrain" parameter.
3.  Toggle the boolean to `True` to run the Python solver.

## Citation
If you use this logic in your work, please cite:
> Islam, M. S. (2026). *Adaptive and Recursive Modular Habitats for Sustainable Growth on Mars* [Source code]. GitHub. https://github.com/isazzad135/mars-recursive-habitat
