#!/bin/bash

# Installationsordner
INSTALL_DIR="$HOME/vestrum"

# Ordner anlegen, falls nicht vorhanden
mkdir -p "$INSTALL_DIR"

# Alle Dateien in INSTALL_DIR kopieren (inkl. icons etc.)
cp -r ./* "$INSTALL_DIR/"

cd "$INSTALL_DIR"

# Virtuelle Umgebung erstellen, falls nicht vorhanden
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Venv aktivieren und Pakete installieren
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Startskript erstellen (start-vestrum.sh)
cat > start-vestrum.sh <<'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python vestrum-bar.py
EOF

chmod +x start-vestrum.sh

# Symlink in /usr/local/bin (sudo nötig)
sudo ln -sf "$INSTALL_DIR/start-vestrum.sh" /usr/local/bin/vestrum

echo "Vestrum wurde installiert! Du kannst jetzt mit 'vestrum' starten."
