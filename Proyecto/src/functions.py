# This file have extra functions needed in the main 

import pandapower as pp
import pandas as pd

def test():
    return("hello test function")

def evaluar_N_menos1(net, vmin=0.9, vmax=1.1, max_load=80):
    results = []

    for elementos in net.line.index:
        net.line.at[elementos, "in_service"] = False # desactivar linea

        # Run simulation
        pp.runpp(net)
        success = net["converged"]

        if success:
            # Buses con tensión fuera de rango
            V_violated_buses = net.res_bus.index[
                ~net.res_bus.vm_pu.between(vmin, vmax)
            ].tolist()

            # Líneas sobrecargadas
            P_violated_lines = net.res_line.index[
                net.res_line.loading_percent > max_load
            ].tolist()
        else:
            print(f"Simulation did not converge for line {elementos}")
            V_violated_buses = []
            P_violated_lines = []

        passes = success and not V_violated_buses and not P_violated_lines

        results.append({
            "line": elementos,
            "success": success,
            "passes_N-1": passes,
            "V_violated_buses": V_violated_buses,
            "P_violated_lines": P_violated_lines
        })

        net.line.at[elementos, "in_service"] = True #Activar linea

    return pd.DataFrame(results)