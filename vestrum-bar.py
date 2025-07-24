import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QCursor
from pynput import keyboard
import threading

class Communicate(QObject):
    toggle_signal = pyqtSignal()

class VestrumBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(700, 70)
        self.setStyleSheet("background-color: black;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Icon laden (bitte Pfad anpassen!)
        self.icon_label = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icons/vestrum_icon.png")).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)
        layout.addWidget(self.icon_label)

        self.input = QLineEdit()
        self.input.setStyleSheet("color: white; font-size: 26px; background-color: black; border: none;")
        self.input.returnPressed.connect(self.on_enter)
        layout.addWidget(self.input)

        self.setLayout(layout)

        # Commands definieren
        self.commands = {
            "youtube": lambda: self.open_url("https://youtube.com"),
            "yt": lambda: self.open_url("https://youtube.com"),
            "firefox": lambda: subprocess.Popen(["firefox"]),
            "calc": lambda: subprocess.Popen(["gnome-calculator"]),
        }

        subprocess.run(["kquitapp5", "plasmashell"])
        self.hide()

        self.comm = Communicate()
        self.comm.toggle_signal.connect(self.toggle_visibility)

    def open_url(self, url):
        subprocess.Popen(["xdg-open", url])

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            pos = QCursor.pos()
            self.move(pos.x() - self.width()//2, pos.y() - self.height()//2)
            self.show()
            self.input.setFocus()

    def on_enter(self):
        text = self.input.text().strip().lower()
        if text == "exit":
            subprocess.run(["kstart5", "plasmashell"])
            self.close()
            return

        if text in self.commands:
            self.commands[text]()
            self.input.clear()
            return

        matches = []
        home_dir = os.path.expanduser("~")
        max_results = 50
        for root, dirs, files in os.walk(home_dir):
            for name in files + dirs:
                if text in name.lower():
                    full_path = os.path.join(root, name)
                    matches.append(full_path)
                    if len(matches) >= max_results:
                        break
            if len(matches) >= max_results:
                break

        if matches:
            subprocess.Popen(["xdg-open", matches[0]])
            print(f"Öffne: {matches[0]}")
        else:
            print("Nichts gefunden!")

        self.input.clear()

def listen_hotkey(comm):
    def on_press(key):
        if key == keyboard.Key.cmd:
            comm.toggle_signal.emit()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bar = VestrumBar()

    t = threading.Thread(target=listen_hotkey, args=(bar.comm,), daemon=True)
    t.start()

    sys.exit(app.exec_())
