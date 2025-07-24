#!/bin/bash

# Zielordner für vestrum
INSTALL_DIR="$HOME/vestrum"

# Ordner anlegen, falls nicht vorhanden
mkdir -p "$INSTALL_DIR"

# Dateien kopieren
cp -r ./vestrum-bar.py "$INSTALL_DIR/"
cp -r ./icons "$INSTALL_DIR/"

# Virtuelle Umgebung einrichten
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install --upgrade pip
pip install PyQt5 pynput

# Start-Skript erstellen
cat > start-vestrum.sh <<'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python vestrum-bar.py
EOF

chmod +x start-vestrum.sh

# Symlink setzen (sudo nötig)
sudo ln -sf "$INSTALL_DIR/start-vestrum.sh" /usr/local/bin/vestrum

echo "Vestrum wurde installiert! Starte mit dem Befehl: vestrum"

#!/bin/bash

# Kompaktes Installationsskript für Vestrum
set -e
INSTALL_DIR="$HOME/vestrum"
mkdir -p "$INSTALL_DIR"
cp -r ./vestrum-bar.py ./icons "$INSTALL_DIR/"
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install PyQt5 pynput
cat > start-vestrum.sh <<'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python vestrum-bar.py
EOF
chmod +x start-vestrum.sh
sudo ln -sf "$INSTALL_DIR/start-vestrum.sh" /usr/local/bin/vestrum
echo "Vestrum wurde installiert! Starte mit: vestrum"