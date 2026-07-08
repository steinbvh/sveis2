from data_handling import InputPakke, OutputPakke

def calculations(data: InputPakke):
    N_add_V = data.N + data.V
    return OutputPakke(
        N_add_V
    )

