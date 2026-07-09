from PySide6.QtWidgets import * 
from PySide6.QtCore import Signal 
from data_handling import InputPakke, OutputPakke 
from calculations import calculations 

# =====================================================================
# 1. INPUT-SEKSJONEN (Eget brukergrensesnitt-element)
# =====================================================================
class InputSection(QWidget):
    """
    Klasse som kun har ansvar for input-siden av programmet.
    Den tar imot tall fra brukeren, pakker dem inn og sender dem videre.
    """
    # Definerer et egendefinert signal på klassenivå.
    # Dette signalet skal bære med seg et objekt av typen InputPakke.
    calculation_requested = Signal(InputPakke)

    def __init__(self):
        super().__init__()
        # Lager en vertikal layout slik at inputfeltene stables oppå hverandre
        layout = QVBoxLayout(self)
        
        # Konfigurerer inputfeltet for normalkraft (N)
        self.N_input = QDoubleSpinBox()
        self.N_input.setRange(0, 10000)
        self.N_input.setPrefix("N: ")
        self.N_input.setSuffix(" kN")
        layout.addWidget(self.N_input)
        
        # Konfigurerer inputfeltet for skjærkraft (V)
        self.V_input = QDoubleSpinBox()
        self.V_input.setRange(0, 10000)
        self.V_input.setPrefix("V: ")
        self.V_input.setSuffix(" kN")
        layout.addWidget(self.V_input)
        
        # Lager knappen som brukeren trykker på for å starte beregningen
        self.calc_button = QPushButton("Calculate")
        layout.addWidget(self.calc_button)
        
        # KNYTTING AV INTERN LOGIKK:
        # Når knappen trykkes, kjøres den interne metoden 'samle_data'.
        # InputSection håndterer dette selv uten at hovedvinduet trenger å vite om det.
        self.calc_button.clicked.connect(self.samle_data)

    def samle_data(self):
        """Henter verdiene fra skjermen, pakker dem inn og skyter ut signalet."""
        # Oppretter datapakke-objektet med de gjeldende verdiene fra spinboksene
        data_pakke = InputPakke(
            N = self.N_input.value(), 
            V = self.V_input.value()
        )
        # Emitterer (sender) signalet ut av denne modulen.
        # Hvem som helst på utsiden (f.eks. MainWindow) kan nå lytte på dette.
        self.calculation_requested.emit(data_pakke)


# =====================================================================
# 2. OUTPUT-SEKSJONEN (Eget brukergrensesnitt-element)
# =====================================================================
class OutputSection(QWidget):
    """
    Klasse som kun har ansvar for output-siden av programmet.
    Den vet ingenting om beregninger eller input, den bare viser det den får beskjed om.
    """
    def __init__(self):
        super().__init__()
        # Vertikal layout for eventuelle fremtidige utvidelser av resultatsiden
        layout = QVBoxLayout(self)
        
        # Tekstfeltet som skal vise resultatet til brukeren
        self.N_V_output = QLabel("N + V =")
        layout.addWidget(self.N_V_output)

    def vis_resultat(self, output: OutputPakke):
        """
        Offentlig metode som andre klasser kan kalle på for å dytte 
        nye resultater inn på skjermen.
        """
        # Formaterer strengen og oppdaterer teksten i QLabel-feltet
        self.N_V_output.setText(f"N + V = {output.N_V} kN")


# =====================================================================
# 3. HOVEDVINDUET (Arkitekten / Limet i programmet)
# =====================================================================
class MainWindow(QMainWindow):
    """
    Hovedvinduet som fungerer som en overordnet sjef.
    Dets eneste oppgaver er å plassere input/output på skjermen, 
    og dirigere trafikken (signaler) mellom dem.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sveis 2")
        self.resize(800, 500)
        
        # Sentral widget og horisontal layout for å dele vinduet i to (venstre/høyre)
        main_container = QWidget()
        self.setCentralWidget(main_container)
        main_layout = QHBoxLayout(main_container)
        
        # Instansierer de to uavhengige komponentene våre
        self.input_section = InputSection()
        self.output_section = OutputSection()
        
        # Plasserer dem side om side i hovedlayouten med lik breddevekt (stretch=1)
        main_layout.addWidget(self.input_section, stretch=1)
        main_layout.addWidget(self.output_section, stretch=1)
        
        # --- SENTRALBORDET (Signal- og eventkobling) ---
        # Hovedvinduet lytter på input-seksjonen. 
        # NÅR input_section sier "calculation_requested", SÅ kjører vi 'orchestrator'.
        self.input_section.calculation_requested.connect(self.orchestrator)

    def orchestrator(self, data_pakke: InputPakke):
        """Mottar data fra input, trigger ingeniørlogikken, og sender svar til output."""
        # 1. Kjører den tunge, eksterne beregningsfunksjonen med innsamlet data
        calculations_done = calculations(data_pakke)
        
        # 2. Sender det ferdige resultatet rett over til metoden i output-seksjonen
        self.output_section.vis_resultat(calculations_done)


# =====================================================================
# 4. PROGRAMSTART
# =====================================================================
if __name__ == "__main__":
    app = QApplication([])      # Initialiserer Qt-rammeverket
    window = MainWindow()       # Bygger og kobler sammen hele vinduet vårt
    window.show()               # Gjør vinduet synlig for brukeren
    app.exec()                  # Starter hendelsesløkken (venter på klikk)