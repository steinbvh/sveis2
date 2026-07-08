from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sveis 2")
        self.resize(800, 500)

        # main central container and layout
        main_container = QWidget()
        self.setCentralWidget(main_container)
        main_layout = QHBoxLayout(main_container)


        # input container
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)

        self.N_input = QDoubleSpinBox()
        self.N_input.setRange(0, 10000)
        self.N_input.setPrefix("N:      ")
        self.N_input.setSuffix(" kN")
        input_layout.addWidget(self.N_input)

        self.V_input = QDoubleSpinBox()
        self.V_input.setRange(0, 10000)
        self.V_input.setPrefix("V:      ")
        self.V_input.setSuffix(" kN")
        input_layout.addWidget(self.V_input)

        calc_button = QPushButton("Calculate")
        input_layout.addWidget(calc_button)
        calc_button.clicked.connect(self.calculation_pushed)

        # output container
        output_container = QWidget()
        output_layout = QVBoxLayout(output_container)

        self.N_V_output=QLabel("N + V =")
        output_layout.addWidget(self.N_V_output)


        # assemble containers
        main_layout.addWidget(input_container, stretch=1)
        main_layout.addWidget(output_container, stretch=1)

    # calculation
    def calculation(self, a, b):
        result = a + b
        return result

    def update_screen(self, result):
        self.N_V_output.setText(f"N + V =    {result}    kN")

    def calculation_pushed(self):
        result = self.calculation(self.N_input.value(), self.V_input.value())
        self.update_screen(result)
    



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()