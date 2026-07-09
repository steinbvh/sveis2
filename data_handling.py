from dataclasses import dataclass

@dataclass
class InputPakke:
    N: float
    V: float
    M: float
    L: float
    a: float
    fu: float
    Bw: float
    Ym2: float

@dataclass
class OutputPakke:
    sigma_perp: float
    tau_perp: float
    tau_para: float
    total_stress: float
    capacity: float
    utilization: float