from PyQt6 import QtWidgets, QtCore, QtGui
import sys
import os
import re
import codecs
import subprocess

def set_dark_theme(app):
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(42, 42, 42))
    palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor(66, 66, 66))
    palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase, QtCore.Qt.GlobalColor.white)
    palette.setColor(QtGui.QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)
    palette.setColor(QtGui.QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
    palette.setColor(QtGui.QPalette.ColorRole.Dark, QtGui.QColor(35, 35, 35))
    palette.setColor(QtGui.QPalette.ColorRole.Shadow, QtGui.QColor(20, 20, 20))
    palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
    palette.setColor(QtGui.QPalette.ColorRole.BrightText,
                     QtCore.Qt.GlobalColor.red)
    palette.setColor(QtGui.QPalette.ColorRole.Highlight,
                     QtGui.QColor(42,
                                  130,
                                  218))
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText,
                     QtCore.Qt.GlobalColor.white)

    app.setPalette(palette)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Inizializza file_path come stringa vuota
        self.file_path = ""

        self.setWindowTitle("GUI per gestire le operazioni di input")

        # Crea il box per la selezione dei file
        self.file_selector = QtWidgets.QPushButton("Seleziona file o cartella")
        self.file_selector.clicked.connect(self.select_file)
        self.file_selector.setStyleSheet("background-color: #2A2A2A; color: #FFFFFF")

        # Crea il box per mostrare il percorso del file selezionato
        self.file_path_display = QtWidgets.QLineEdit()
        self.file_path_display.setReadOnly(False)
        self.file_path_display.setStyleSheet("background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #404040")

        # Crea il box per l'output del terminale
        self.terminal_output = QtWidgets.QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("background-color: #2A2A2A; color: #FFFFFF; border: 1px solid #404040")

        # Crea il pulsante di avvio
        self.start_button = QtWidgets.QPushButton("Avvia")
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setStyleSheet("background-color: #2A2A2A; color: #FFFFFF")

        # Crea il layout
        self.layout = QtWidgets.QVBoxLayout()

        # Crea un layout orizzontale per la selezione dei file e il display del percorso
        self.file_layout = QtWidgets.QHBoxLayout()
        self.file_layout.addWidget(self.file_selector)
        self.file_layout.addWidget(self.file_path_display)

        self.layout.addLayout(self.file_layout)

        self.layout.addWidget(self.terminal_output)
        self.layout.addWidget(self.start_button)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        # Ridimensiona la finestra a 720x480 pixel
        self.resize(600, 360)

    def select_file(self):
        file_dialog = QtWidgets.QFileDialog()
        self.file_path = file_dialog.getOpenFileName()[0]  # Usa self.file_path invece di file_path

        # Mostra il percorso del file nel box di testo
        self.file_path_display.setText(self.file_path)

    def start_processing(self):
        if os.path.isdir(self.file_path):
            # Trova tutti i file .ass nella cartella
            ass_files = [filename for filename in os.listdir(self.file_path) if filename.endswith(".ass")]
            output_folder = self.file_path
            for ass_filename in ass_files:
                    ass_filepath = os.path.join(self.file_path, ass_filename)
                    self.ass_mod(output_folder, ass_filepath)
                    self.terminal_output.append(f"Modificato il file {ass_filename}")
        else:
            ass_filepath = self.file_path
            output_folder = os.path.dirname(ass_filepath)
            self.ass_mod(output_folder, ass_filepath)
            self.terminal_output.append(f"Modificato il file {os.path.basename(ass_filepath)}")

    def ass_mod(self, output_folder, ass_filepath):
            # Leggi il file .ass
        with codecs.open(ass_filepath, "r", "utf-8") as f:
            lines = f.readlines()

        # Inserisci le righe modificate nel file .ass
        lines.insert(15, "YCbCr Matrix: TV.709\n")
        lines.insert(16, "ScaledBorderAndShadow: yes\n")

        new_lines = []
        for line in lines:
            if "PlayResX:" in line or "PlayResY:" in line:
                if "PlayResX:" in line:
                    new_lines.append("PlayResX: 1920\n")
                if "PlayResY:" in line:
                    new_lines.append("PlayResY: 1080\n")
            elif line.startswith("Style:"):
                parts = line.split(",")
                if len(parts) > 3 and parts[0] == "Default" or "Default Top" or "Italics" or "Italics Top" or "Narrator" or "Narrator Top" or "Overlap" or "Internat" or "Internal Top" or "Flashback" or "Flashback Internal" or "Flashback - Top" or "Flashback - Inception" :
                    parts[2] = str(int(round(float(parts[2]) * 3.27)))
                    parts[16] = str(int(round(float(parts[16]) * 1.77)))
                    parts[19] = str(int(int(parts[19]) * 17.7))
                    parts[20] = str(int(int(parts[20]) * 17.7))
                    parts[21] = str(int(int(parts[21]) * 3))
                else:
                    parts[2] = str(int(round(float(parts[2]) * 3.27)))
                    parts[16] = str(int(round(float(parts[16]) * 3.27)))
                    parts[19] = str(int(round(float(parts[19]) * 3.27)))
                    parts[20] = str(int(round(float(parts[20]) * 3.27)))
                    parts[21] = str(int(int(parts[21]) * 3))
                new_line = ",".join(parts)
                new_lines.append(new_line)       
            elif line.startswith("Dialogue:"):
                new_line = re.sub(r'\\fs([\d]+)', lambda x: f"\\fs{str(int(round(float(x.group(1)) * 3.27)))}", line)
                new_line = re.sub(r'\\pos\(([\d.]+),([\d.]+)\)', lambda x: f"\\pos({str(round(float(x.group(1)) * 3.01, 2))},{str(round(float(x.group(2)) * 3.01, 2))})", new_line)
                parts = line.split(",")
                if line.startswith("Dialogue:") and "Top" in parts[3] or " Top" in parts[3]:
                    parts[3] = parts[3].replace("Top", "").replace(" Top", "")
                    parts[9] = "{\\an8}" + parts[9]
                    new_line = ",".join(parts)
                if line.startswith("Dialogue:") and "Italics" in parts[3]:
                    parts[3] = parts[3].replace("Italics", "Default")
                    parts[9] = "{\\i1}" + parts[9]
                    new_line = ",".join(parts)
                new_lines.append(new_line)
            else:
                new_lines.append(line)

                

            # Scrivi le nuove righe nel file di output

            output_filename = os.path.join(output_folder, os.path.basename(ass_filepath))
            with codecs.open(output_filename, 'w', encoding='utf-8-sig') as f:
                f.writelines(new_lines)

app = QtWidgets.QApplication(sys.argv)
set_dark_theme(app) # Applica il tema scuro

window = MainWindow()
window.show()

app.exec()