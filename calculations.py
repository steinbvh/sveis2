import math
from data_handling import InputPakke, OutputPakke

def calculations(data: InputPakke):
    N = data.N 
    V = data.V
    M = data.M
    L = data.L
    a = data.a
    fu = data.fu
    Bw = data.Bw
    Ym2 = data.Ym2

    sigma_perp = ((M * 10**6)/ ((math.sqrt(2)/12)*a*L**3)) * (L / 2) + ((N*1000) / (math.sqrt(2)*L*a))
    tau_perp = sigma_perp

    tau_para = (V * 1000) / (L * a)

    total_stress = math.sqrt(sigma_perp**2 + 3*(tau_perp**2 + tau_para**2))

    capacity = fu / (Bw * Ym2)

    utilization = round((total_stress / capacity) * 100)
    
    return OutputPakke(
        sigma_perp,
        tau_perp,
        tau_para,
        total_stress,
        capacity,
        utilization
    )

