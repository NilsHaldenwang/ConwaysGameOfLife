# Conway's Game of Life - Professionelle Implementierung

Eine didaktisch wertvolle Implementierung von Conway's Game of Life in Python, die moderne Softwareentwicklungsprinzipien und Design Patterns demonstriert.

## Installation

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

### Anwendung starten
```bash
python main.py
```

### Unit-Tests ausführen
```bash
# Alle Tests ausführen
python run_tests.py

# Oder mit unittest
python -m unittest discover -v

# Einzelne Test-Module
python test_game_of_life_engine.py
python test_game_of_life_view.py
python test_game_of_life_controller.py
```

## Bedienung

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

## Projektübersicht

Diese Implementierung demonstriert:
- **Clean Code Prinzipien** mit ausführlicher Dokumentation
- **Design Patterns**: Model-View-Controller (MVC) Architektur
- **Separation of Concerns**: Klare Trennung von Logik, Visualisierung und Steuerung
- **Effiziente numerische Berechnungen** mit NumPy
- **Professionelle Visualisierung** mit PyGame
- **Umfassende Unit-Tests** für alle Komponenten

## Architektur

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

### Vorteile dieser Architektur

1. **Testbarkeit**: Jede Komponente kann isoliert getestet werden
2. **Wartbarkeit**: Änderungen an einer Komponente beeinflussen andere nicht
3. **Erweiterbarkeit**: Neue Features können leicht hinzugefügt werden
4. **Wiederverwendbarkeit**: Engine kann mit anderer UI verwendet werden

## Projektstruktur

```
conways-game-of-life/
│
├── main.py                          # Haupteinstiegspunkt
├── game_of_life_engine.py          # Model: Spiellogik mit NumPy
├── game_of_life_view.py            # View: PyGame Visualisierung
├── game_of_life_controller.py      # Controller: Koordination & Input
│
├── test_game_of_life_engine.py     # Unit-Tests für Engine
├── test_game_of_life_view.py       # Unit-Tests für View
├── test_game_of_life_controller.py # Unit-Tests für Controller
├── run_tests.py                     # Test-Runner
│
├── patterns/                        # Beispiel-Muster
│   ├── glider.txt                  # Glider (bewegt sich)
│   ├── blinker.txt                 # Blinker (Oszillator)
│   ├── block.txt                   # Block (Still Life)
│   └── toad.txt                    # Toad (Oszillator)
│
├── requirements.txt                 # Python-Abhängigkeiten
└── README.md                        # Dokumentation
```

## Conway's Game of Life - Regeln

1. Jede lebende Zelle mit 2 oder 3 lebenden Nachbarn überlebt
2. Jede tote Zelle mit genau 3 lebenden Nachbarn wird lebendig
3. Alle anderen Zellen sterben oder bleiben tot

## Code-Qualität und Best Practices

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
# Effizient: Vektorisierte Operation
neighbors[:-1, :] += self.grid[1:, :]   # Bottom neighbors
neighbors[1:, :] += self.grid[:-1, :]   # Top neighbors
# ... etc für alle 8 Richtungen
```

Dies ist deutlich schneller als verschachtelte Schleifen (Faktor 50-100x bei großen Grids).

**Vergleich:**
```python
# Ineffizient: Verschachtelte Schleifen (nicht verwendet)
for i in range(rows):
    for j in range(cols):
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                # ...
```

### Type Hints & Documentation

```python
def count_neighbors(self) -> np.ndarray:
    """
    Count live neighbors using efficient NumPy operations.

    Returns:
        2D NumPy array with neighbor counts
    """
```

## Testabdeckung

Die Implementierung enthält umfassende Unit-Tests:

### test_game_of_life_engine.py (21 Tests)
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

## Muster-Dateien

Im Verzeichnis `patterns/` sind Beispiel-Muster enthalten:

### Still Life (stabil)
- **block.txt**: Block (2×2 Quadrat) - bleibt für immer stabil

### Oszillatoren (periodisch)
- **blinker.txt**: Blinker (Periode 2, horizontal ↔ vertikal)
- **toad.txt**: Toad (Periode 2)

### Raumschiffe (bewegen sich)
- **glider.txt**: Glider - bewegt sich diagonal

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

## Erweiterungsmöglichkeiten

Die Architektur ermöglicht folgende Erweiterungen:

1. **Pattern Editor**
   - Drag-to-draw Interface
   - Pattern-Bibliothek (Gosper Glider Gun, etc.)

2. **Statistiken**
   - Populations-Graph über Zeit
   - Stabilitätserkennung
   - Generationszähler

3. **Verschiedene Regelsets**
   - Day & Night
   - HighLife
   - Seeds
   - Andere zelluläre Automaten

4. **Performance-Optimierungen**
   - Hashlife-Algorithmus
   - GPU-Beschleunigung (CUDA)

5. **Export/Import**
   - RLE-Format (Run Length Encoded)
   - GIF-Animation-Export
   - Screenshot-Funktion

6. **UI-Verbesserungen**
   - Zoom-Funktionalität
   - Step-by-Step Modus
   - Verschiedene Farbschemata

## Literatur

### Design Patterns und Software-Architektur
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.
- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.

### Conway's Game of Life
- Gardner, M. (1970). "Mathematical Games: The fantastic combinations of John Conway's new solitaire game 'life'". *Scientific American*, 223(4), 120-123.
- Berlekamp, E. R., Conway, J. H., & Guy, R. K. (1982). *Winning Ways for Your Mathematical Plays, Volume 2*. Academic Press.

### Online-Ressourcen
- ConwayLife.com Wiki - Umfassende Muster-Sammlung
- LifeWiki Pattern Collection - Dokumentation bekannter Muster

## Technische Details

**Entwicklungsumgebung:**
- Python 3.8+
- NumPy für numerische Berechnungen
- PyGame für Visualisierung
- unittest für Testframework

**Performance:**
- Grid-Größe: bis zu 100×100 Zellen flüssig
- Update-Rate: konfigurierbar (Standard: 10 FPS)
- Speicher-Effizienz: NumPy Arrays mit dtype=int8
