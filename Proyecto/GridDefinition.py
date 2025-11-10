### Librerias ###
import pandas as pd
import numpy as np
import pandapower as pp
from pandapower.plotting import simple_plotly, pf_res_plotly
import math
import datetime
import os

#### DEFINITION OF GRID ###
# New net
project_net = pp.create_empty_network()

# creating HV buses
pp.create_bus(project_net, name="Terrasa", vn_kv=110, geodata=(2.01787, 41.56681))
pp.create_bus(project_net, name="Manresa", vn_kv=110, geodata=(1.81685, 41.72396))
pp.create_bus(project_net, name="Tarrega", vn_kv=110, geodata=(1.13954, 41.64687))
pp.create_bus(project_net, name="Montblanc", vn_kv=110, geodata=(1.16178, 41.37478))
pp.create_bus(project_net, name="Vandellos", vn_kv=110, geodata=(0.87562, 40.95624))
pp.create_bus(project_net, name="Lleida", vn_kv=110, geodata=(0.61613, 41.61538))
pp.create_bus(project_net, name="Igualada", vn_kv=110, geodata=(1.61912, 41.58074))
pp.create_bus(project_net, name="El Perellos", vn_kv=110, geodata=(0.71262, 40.87541))
pp.create_bus(project_net, name="Agramunt", vn_kv=110, geodata=(1.08664, 41.79154))
pp.create_bus(project_net, name="Valls", vn_kv=110, geodata=(1.24764, 41.28434))
pp.create_bus(project_net, name="Falset", vn_kv=110, geodata=(0.82771, 41.14390))
pp.create_bus(project_net, name="Conesa", vn_kv=110, geodata=(1.27159, 41.50215))

# creating MV buses
pp.create_bus(project_net, name="Manresa_LV", vn_kv=20, geodata=(1.81210, 41.71518))
pp.create_bus(project_net, name="Tarrega_LV", vn_kv=20, geodata=(1.15177, 41.64157))
pp.create_bus(project_net, name="Montblanc_LV", vn_kv=20, geodata=(1.15398, 41.37473))
pp.create_bus(project_net, name="Lleida_LV", vn_kv=20, geodata=(0.61427, 41.61262))

# creating Tranformers
pp.create_transformer_from_parameters(project_net, hv_bus = 1, lv_bus = 12, sn_mva = 100, 
                                      vn_hv_kv = 110, vn_lv_kv = 20, vk_percent = 12, 
                                      vkr_percent = 0.26, pfe_kw = 55, i0_percent = 0.06, name = 'Trafo_Manresa')

pp.create_transformer_from_parameters(project_net, hv_bus = 2, lv_bus = 13, sn_mva = 100, 
                                      vn_hv_kv = 110, vn_lv_kv = 20, vk_percent = 12, 
                                      vkr_percent = 0.26, pfe_kw = 55, i0_percent = 0.06, name = 'Trafo_Tarrega')

pp.create_transformer_from_parameters(project_net, hv_bus = 3, lv_bus = 14, sn_mva = 100, 
                                      vn_hv_kv = 110, vn_lv_kv = 20, vk_percent = 12, 
                                      vkr_percent = 0.26, pfe_kw = 55, i0_percent = 0.06, name = 'Trafo_Montblanc')

pp.create_transformer_from_parameters(project_net, hv_bus = 5, lv_bus = 15, sn_mva = 100, 
                                      vn_hv_kv = 110, vn_lv_kv = 20, vk_percent = 12, 
                                      vkr_percent = 0.26, pfe_kw = 55, i0_percent = 0.06, name = 'Trafo_Lleida')

# Creating lines
kg = 0.809
r_cond = (30.42/2)/1000 #mm -> m
r01_km = 0.062 #ohm/km
max_i_ka = 0.9 # A
print(f"##INFO - r01_km lines: {r01_km}")

## Single Lines

a = 10 #m
b = 4 #m
d_ab = np.sqrt((a/2)**2 + b**2)
d_bc = d_ab
d_ac = a

GMD = (d_ab * d_bc * d_ac) ** (1/3)
GMR = kg * r_cond

x_km = 0.2*np.log(GMD/GMR)
c_nf_km = 1000 / (18*np.log(GMD/r_cond))
x_km = 0.402
c_nf_km = 8.64
print(f"##INFO - x_km Single line: {x_km}")
print(f"##INFO - c_nf_km Single line: {c_nf_km}")

pp.create_line_from_parameters(project_net, from_bus = 5, to_bus = 2, length_km = 44, r_ohm_per_km = r01_km, x_ohm_per_km = x_km, c_nf_per_km = c_nf_km, max_i_ka = max_i_ka, name='Lleida-Tarrega')
pp.create_line_from_parameters(project_net, from_bus = 2, to_bus = 6, length_km = 40, r_ohm_per_km = r01_km, x_ohm_per_km = x_km, c_nf_per_km = c_nf_km, max_i_ka = max_i_ka, name='Tarrega-Igualada')
pp.create_line_from_parameters(project_net, from_bus = 1, to_bus = 0, length_km = 23, r_ohm_per_km = r01_km, x_ohm_per_km = x_km, c_nf_per_km = c_nf_km, max_i_ka = max_i_ka, name='Manresa-Terrasa')

## Double Lines
kg = 0.809
r_cond = (30.42/2)/1000 #mm -> m
r01_km = 0.062 #ohm/km
max_i_ka = 1.8 # A

def dist(p1, p2): 
    return np.linalg.norm(p1 - p2)

n_bundled_conductors = 2
d_bundle = 0

a = 7 #m
b = 9 #m
c = a #m
d = 7.5 #m
e = d #m

### Cordenadas A1, B1, C1, C2, B2, A2 (centrado en centro)
A1 = np.array([-a/2, d+e])
A2 = np.array([ c/2, 0])
B1 = np.array([-b/2, e])
B2 = np.array([ b/2, e])
C1 = np.array([-c/2, 0])
C2 = np.array([ a/2, d+e])

#### GMR
d_A1A2 = dist(A1,A2)
d_B1B2 = dist(B1,B2)
d_C1C2 = dist(C1,C2)

GMR_A = np.sqrt(kg * r_cond * d_A1A2)
GMR_B = np.sqrt(kg * r_cond * d_B1B2)
GMR_C = np.sqrt(kg * r_cond * d_C1C2)

GMR_eq = (GMR_A * GMR_B * GMR_C) ** (1/3)

#### GMD
D_AB = (dist(A1,B1)*dist(A1,B2)*dist(A2,B1)*dist(A2,B2))**0.25
D_BC = (dist(B1,C1)*dist(B1,C2)*dist(B2,C1)*dist(B2,C2))**0.25
D_CA = (dist(C1,A1)*dist(C1,A2)*dist(C2,A1)*dist(C2,A2))**0.25

GMD = (D_AB * D_BC * D_CA) ** (1/3)

x_km = 0.2*(np.log(GMD/GMR_eq))
c_nf_km = 1000 / (18*np.log(GMD/r_cond))
x_km = 0.198
c_nf_km = 8.3
print(f"##INFO - x_km Dobule line: {x_km}")
print(f"##INFO - c_nf_km Dobule line: {c_nf_km}")

pp.create_line_from_parameters(project_net, from_bus = 4, to_bus = 3, length_km = 52, r_ohm_per_km = r01_km/2, x_ohm_per_km = x_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, parallel = 1, name='Vandellos-Montblanc')
pp.create_line_from_parameters(project_net, from_bus = 3, to_bus = 2, length_km = 30, r_ohm_per_km = r01_km/2, x_ohm_per_km = x_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, parallel = 1, name='Montblanc-Tarrega')
pp.create_line_from_parameters(project_net, from_bus = 2, to_bus = 1, length_km = 58, r_ohm_per_km = r01_km/2, x_ohm_per_km = x_km, c_nf_per_km = c_nf_km , max_i_ka = max_i_ka, parallel = 1, name='Tarrega-Manresa')


# Creating loads 

def get_reactive(p_mw, pf):
    Q = p_mw *math.tan(math.acos(pf))
    return Q

PF = 0.98
p_mw = 65
q_mvar= get_reactive(p_mw, PF)
pp.create_load(project_net, 12, p_mw, q_mvar = q_mvar, name="type I load - Manresa", scaling=1.0, in_service=True, type="wye")
pp.create_load(project_net, 15, p_mw, q_mvar = q_mvar, name="type I load - Lleida", scaling=1.0, in_service=True, type="wye")
pp.create_load(project_net, 14, p_mw, q_mvar = q_mvar, name="type I load - Montblanc", scaling=1.0, in_service=True, type="wye")

PF = 0.98
p_mw = 115
q_mvar= get_reactive(p_mw, PF)
pp.create_load(project_net, 13, p_mw, q_mvar = q_mvar, name="type II load - Tarrega", scaling=1.0, in_service=True, type="wye")


# Creating generators
pp.create_gen(project_net, bus=4, p_mw=215, vm_pu=1.0, name="Vandellos 215 MW")
#pp.create_sgen(project_net, 9, 1, name="Valls 215 MW")
#pp.create_sgen(project_net, 10, 1, name="Falset 215 MW")
#pp.create_sgen(project_net, 11, 1, name="Conesa 215 MW")
#pp.create_sgen(project_net, 7, 1, name="Perello 215 MW")
#pp.create_sgen(project_net, 8, 1, name="Agramunt 215 MW")

# Adding SLACK
pp.create_ext_grid(net=project_net, bus = 0, vm_pu = 1.0, va_degree = 0.0, name = 'External Grid')

## GUardar
base_dir = os.path.dirname(os.path.abspath(__file__))
directorio = os.path.join(base_dir, "Project_net.xlsx")
pp.to_excel(project_net, directorio)

# Presentation:
print()
print(project_net)
print()
print(project_net.line)
print()
print(project_net.sgen)
print()
print(project_net.bus)
print()
print(project_net.load)
print()
print(project_net.trafo)
