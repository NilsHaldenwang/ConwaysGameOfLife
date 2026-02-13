# Conway's Game of Life - Didaktische Demo

Eine professionelle, didaktisch wertvolle Implementierung von Conway's Game of Life in Python für eine Professur in Wirtschaftsinformatik.

## 📋 Übersicht

Diese Implementierung demonstriert:
- **Clean Code Prinzipien** mit ausführlicher Dokumentation
- **Design Patterns**: Model-View-Controller (MVC) Architektur
- **Separation of Concerns**: Klare Trennung von Logik, Visualisierung und Steuerung
- **Effiziente numerische Berechnungen** mit NumPy
- **Professionelle Visualisierung** mit PyGame
- **Umfassende Unit-Tests** für alle Komponenten

## 🏗️ Architektur

Die Anwendung folgt dem **Model-View-Controller (MVC)** Pattern:

### Model (game_of_life_engine.py)
- Enthält die komplette Spiellogik
- Nutzt NumPy für effiziente Berechnungen
- Komplett unabhängig von Visualisierung
- Verantwortlich für:
  - Zustandsverwaltung des Spielfeldes
  - Anwendung der Game of Life Regeln
  - Laden von Mustern aus Dateien
  - Nachbarn-Zählung mit vektorisierten Operationen

### View (game_of_life_view.py)
- PyGame-basierte Visualisierung
- Ausschließlich für Darstellung zuständig
- Keinerlei Spiellogik
- Verantwortlich für:
  - Zeichnen des Spielfeldes
  - UI-Elemente (Buttons, Status-Anzeige)
  - Hover-Effekte und visuelle Rückmeldung
  - Erkennung von Maus-Interaktionen

### Controller (game_of_life_controller.py)
- Koordiniert Model und View
- Verarbeitet Benutzereingaben
- Verwaltet Anwendungszustand
- Verantwortlich für:
  - Event-Handling (Maus, Tastatur)
  - Simulation-Steuerung (Start/Pause)
  - Orchestrierung zwischen Model und View

## 🎮 Conway's Game of Life Regeln

1. Jede lebende Zelle mit 2 oder 3 lebenden Nachbarn überlebt
2. Jede tote Zelle mit genau 3 lebenden Nachbarn wird lebendig
3. Alle anderen Zellen sterben oder bleiben tot

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Installation der Abhängigkeiten
```bash
pip install -r requirements.txt
```

Oder manuell:
```bash
pip install numpy pygame
```

## ▶️ Ausführung

### Anwendung starten
```bash
python main.py
```

### Unit-Tests ausführen
```bash
# Alle Tests ausführen
python -m unittest discover -v

# Einzelne Test-Module
python test_game_of_life_engine.py
python test_game_of_life_view.py
python test_game_of_life_controller.py
```

## 🎯 Bedienung

### Maus-Steuerung
- **Start-Button**: Simulation starten
- **Pause-Button**: Simulation anhalten
- **Load-Button**: Muster aus Datei laden
- **Clear-Button**: Spielfeld leeren
- **Klick auf Zellen** (nur im Pause-Modus): Zellen aktivieren/deaktivieren

### Tastatur-Shortcuts
- **Leertaste**: Simulation starten/pausieren
- **C**: Spielfeld leeren
- **L**: Muster laden
- **ESC**: Simulation pausieren

## 📁 Muster-Dateien

Im Verzeichnis `patterns/` sind Beispiel-Muster enthalten:
- **glider.txt**: Glider (bewegt sich diagonal)
- **blinker.txt**: Blinker (Oszillator mit Periode 2)
- **block.txt**: Block (Still Life - bleibt stabil)
- **toad.txt**: Toad (Oszillator mit Periode 2)

### Format der Muster-Dateien
- Textdatei mit n Zeilen für ein n×n Spielfeld
- Jede Zeile enthält n Zeichen (0 oder 1)
- `0` = tote Zelle
- `1` = lebende Zelle
- Keine Leerzeichen oder andere Zeichen

Beispiel (3×3):
```
010
111
010
```

## 🧪 Testabdeckung

Die Implementierung enthält umfassende Unit-Tests:

### test_game_of_life_engine.py
- Initialisierung und Dimensionen
- Zell-Manipulation (set/get)
- Nachbar-Zählung (corner cases, edge cases)
- Regelanwendung (Überleben, Sterben, Geburt)
- Bekannte Muster (Still Life, Oszillatoren)
- Datei-Laden (gültige/ungültige Formate)

### test_game_of_life_view.py
- View-Initialisierung
- Button-Erkennung
- Maus-zu-Grid-Konvertierung
- Hover-State-Management
- Rendering (ohne Fehler)

### test_game_of_life_controller.py
- Controller-Initialisierung
- Zustandsverwaltung (Start/Pause/Clear)
- Event-Handling (Maus, Tastatur)
- Integration Model-View

## 🔍 Code-Qualität

### Design Patterns
- **MVC (Model-View-Controller)**: Klare Trennung der Verantwortlichkeiten
- **Separation of Concerns**: Jede Klasse hat eine klar definierte Aufgabe
- **Dependency Injection**: Controller erhält Model und View

### Best Practices
- **Ausführliche Kommentare**: Jede Methode ist dokumentiert
- **Type Hints**: Verwendung von Python Type Hints
- **Descriptive Naming**: Sprechende Variablen- und Funktionsnamen
- **DRY (Don't Repeat Yourself)**: Keine Code-Duplikation
- **SOLID Principles**: Besonders Single Responsibility Principle

### NumPy Optimierung
Die Engine nutzt vektorisierte NumPy-Operationen für maximale Effizienz:
```python
# Effiziente Nachbar-Zählung durch Array-Slicing
neighbors[:-1, :] += self.grid[1:, :]   # Bottom neighbors
neighbors[1:, :] += self.grid[:-1, :]   # Top neighbors
# ... etc für alle 8 Richtungen
```

Dies ist deutlich schneller als verschachtelte Schleifen!

## 📚 Verwendung für den Vortrag

### Didaktische Aspekte
1. **Design Patterns demonstrieren**: MVC-Architektur zeigen
2. **NumPy-Effizienz**: Vergleich zu naiver Implementierung
3. **Testing**: Importance of comprehensive unit tests
4. **Code-Organisation**: Wie man ein Projekt strukturiert

### Demonstration
1. Verschiedene Muster laden (Glider, Oszillatoren, Still Lifes)
2. Regeln erklären und beobachten
3. Manuelle Zell-Manipulation im Pause-Modus
4. Performance bei großen Grids zeigen

### Erweitungsmöglichkeiten (für Diskussion)
- Weitere Muster (Gosper Glider Gun, etc.)
- Verschiedene Regelsets (andere zelluläre Automaten)
- Statistiken (Population, Stabilitätserkennung)
- Export von Mustern
- Zoom-Funktionalität
- Step-by-Step Modus

## 📖 Literatur zu Design Patterns

- Gamma, E., et al. (1994). Design Patterns: Elements of Reusable Object-Oriented Software
- Martin, R. C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship
- Martin, R. C. (2017). Clean Architecture

## 👤 Autor

Erstellt für eine Professur in Wirtschaftsinformatik
Demonstriert professionelle Softwareentwicklung mit Python

## 📄 Lizenz

Dieses Projekt dient ausschließlich didaktischen Zwecken.
