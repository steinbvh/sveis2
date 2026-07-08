from PySide6.QtWidgets import * 
from PySide6.QtCore import Qt, Signal 
from data_handling import InputPakke, OutputPakke 
from calculations import calculations 

class MainWindow(QMainWindow):
    # Egendefinert PySide6-signal som transporterer et InputPakke-objekt.
    # MÅ defineres på klassenivå for at Qt skal registrere det korrekt.
    do_calculation = Signal(InputPakke)

    def __init__(self):
        """Initaliserer hovedvinduet, bygger brukergrensesnittet og kobler signaler."""
        super().__init__()
        self.setWindowTitle("Sveis 2")
        self.resize(800, 500)
        
        # Hovedbeholder (Central Widget) som kreves av QMainWindow for å holde på layouten
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # Horisontal hovedlayout som deler vinduet i en venstre (input) og høyre (output) del
        main_layout = QHBoxLayout(main_container)
        
        # --- INPUT-SEKSJON (Venstre side) ---
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container) # Vertikal stabling av input-felter
        
        # Konfigurasjon av inputfelt for normalkraft (N)
        self.N_input = QDoubleSpinBox()
        self.N_input.setRange(0, 10000)
        self.N_input.setPrefix("N: ")
        self.N_input.setSuffix(" kN")
        input_layout.addWidget(self.N_input)
        
        # Konfigurasjon av inputfelt for skjærkraft (V)
        self.V_input = QDoubleSpinBox()
        self.V_input.setRange(0, 10000)
        self.V_input.setPrefix("V: ")
        self.V_input.setSuffix(" kN")
        input_layout.addWidget(self.V_input)
        
        # Knapp for å trigge beregningene
        self.calc_button = QPushButton("Calculate")
        input_layout.addWidget(self.calc_button)
        
        # --- OUTPUT-SEKSJON (Høyre side) ---
        output_container = QWidget()
        output_layout = QVBoxLayout(output_container)
        
        # Tekstfelt som viser resultatet av beregningen
        self.N_V_output = QLabel("N + V =")
        output_layout.addWidget(self.N_V_output)
        
        # --- MONTERING AV LAYOUT ---
        # Legger til venstre og høyre beholder med lik breddevekt (stretch=1)
        main_layout.addWidget(input_container, stretch=1)
        main_layout.addWidget(output_container, stretch=1)
        
        # --- SIGNAL- OG EVENTKOBLINGER ---
        # Kobler knappetrykk til metoden som samler inn data
        self.calc_button.clicked.connect(self.send_data)
        
        # Kobler det interne signalet til orkestratoren som håndterer logikken
        self.do_calculation.connect(self.orchestrator)

    def send_data(self):
        """Henter verdier fra brukergrensesnittet, pakker dem og sender signalet."""
        # Oppretter et datatypet objekt med gjeldende verdier fra spinboksene
        data_pakke = InputPakke(
            N = self.N_input.value(), 
            V = self.V_input.value()
        )
        # Emitterer (sender) signalet av gårde med datapakken som argument
        self.do_calculation.emit(data_pakke)

    def orchestrator(self, data_pakke: InputPakke):
        """Mottar datapakken, utfører ingeniørberegningene og oppdaterer skjermen."""
        # Kjører den eksterne beregningsfunksjonen
        calculations_done = calculations(data_pakke)
        # Sender resultatet videre til GUI-oppdatering
        self.update_screen(calculations_done)

    def update_screen(self, output: OutputPakke):
        """Oppdaterer tekstfeltene i brukergrensesnittet med de nye resultatene."""
        # Formaterer og skriver ut den beregnede verdien til QLabel-feltet
        self.N_V_output.setText(f"N + V = {output.N_V} kN")

# Startbetingelse for applikasjonen (kjøres kun hvis filen startes direkte)
if __name__ == "__main__":
    app = QApplication([])      # Oppretter Qt-applikasjonskonteksten
    window = MainWindow()       # Oppretter og initialiserer hovedvinduet
    window.show()               # Gjør vinduet synlig på skjermen
    app.exec()                  # Starter Qts interne hendelsesløkke (event loop)