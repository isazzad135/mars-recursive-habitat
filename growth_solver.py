"""
MARS ADAPTIVE HABITAT SOLVER (v1.0)
-----------------------------------
Author: Md Sazzad Islam
Context: Research for "Adaptive and Recursive Modular Habitats for Sustainable Growth on Mars"
License: MIT License

Description:
    An iterative agent-based solver that generates habitat configurations based on
    environmental heuristics. The algorithm mimics biological growth (morphogenesis)
    by evaluating local terrain conditions and solar alignment.

Key Constraints:
    1. Slope Safety: Modules cannot be placed on terrain > 30 degrees.
    2. Collision: Maintains a buffer zone (min_dist) between modules.
    3. Heliotropism: Growth direction is weighted by alignment with the solar vector.
    4. Branching: Implements stochastic backtracking when growth is blocked.
"""

import Rhino.Geometry as rg
import math
import random

def run_simulation(terrain_mesh, seed_point, max_modules=147):
    # --- 1. CONFIGURATION & HEURISTICS ---
    # Global constraints derived from DRA 5.0 and structural limits
    PARAMS = {
        "max_slope_deg": 30.0,      # Maximum traversable slope for modules
        "min_dist": 3.0,            # Module diameter/spacing
        "step_size": 3.5,           # Arm length for connection
        "sun_vec": rg.Vector3d(0, -3, 0.5) # Normalized later
    }
    
    # Initialize Vectors
    PARAMS["sun_vec"].Unitize()
    
    # Hexagonal Search Directions (60-degree increments)
    growth_directions = []
    for i in range(6):
        angle = math.radians(i * 60)
        vec = rg.Vector3d(math.cos(angle), math.sin(angle), 0)
        vec *= PARAMS["step_size"]
        growth_directions.append(vec)

    # --- 2. INITIALIZATION ---
    terrain_mesh.Normals.ComputeNormals()
    
    # Snap seed to terrain
    mp = terrain_mesh.ClosestMeshPoint(seed_point, 1000000.0)
    current = mp.Point if mp else seed_point
    
    modules = [current]
    iterations = [0]
    
    print("Initialize: Growth cycle started from seed {}.".format(current))

    # --- 3. MAIN GROWTH LOOP ---
    # Algorithm type: Greedy Best-First Search with Stochastic Backtracking
    for i in range(1, max_modules + 1):
        
        candidates = []
        
        # A. SENSING (Check all 6 neighbors)
        for d in growth_directions:
            test_pt = rg.Point3d(current)
            test_pt.Transform(rg.Transform.Translation(d))
            
            # Project candidate to Mesh (Grounding)
            mp_check = terrain_mesh.ClosestMeshPoint(test_pt, 1000.0)
            
            if mp_check:
                cand_pt = mp_check.Point
                
                # B. CONSTRAINT CHECKING
                
                # Crit 1: Slope Analysis
                normal = terrain_mesh.NormalAt(mp_check)
                slope_rad = rg.Vector3d.VectorAngle(normal, rg.Vector3d.ZAxis)
                if math.degrees(slope_rad) > PARAMS["max_slope_deg"]:
                    continue # Slope too steep
                
                # Crit 2: Collision Detection (Distance Check)
                collision = False
                for existing in modules:
                    if cand_pt.DistanceTo(existing) < (PARAMS["min_dist"] - 0.1):
                        collision = True
                        break
                if collision: 
                    continue
                    
                candidates.append(cand_pt)

        # C. DECISION MAKING
        
        # State: Blocked -> Trigger Backtracking (Biomimetic Branching)
        if not candidates:
            # Randomly select a previous module to branch from (simulating lateral budding)
            current = random.choice(modules)
            continue

        # State: Open -> Optimize for Solar Gain (Heliotropism)
        best_cand = None
        best_score = -999.0

        for cand in candidates:
            # Calculate growth vector
            growth_dir = cand - current
            growth_dir.Unitize()
            
            # Dot Product determines alignment (1.0 = perfect alignment)
            score = growth_dir * PARAMS["sun_vec"]
            
            if score > best_score:
                best_score = score
                best_cand = cand

        # D. EXECUTION
        if best_cand:
            modules.append(best_cand)
            iterations.append(i)
            current = best_cand

    print("Simulation Complete. Final Colony Size: {} modules.".format(len(modules)))
    return modules

# --- ENTRY POINT (For Grasshopper) ---
# Assuming 'activate' is a boolean toggle input in GH
if activate:
    A = run_simulation(terrain_mesh, seed_point)