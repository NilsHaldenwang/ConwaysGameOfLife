# Präsentations-Checkliste - Conway's Game of Life Vortrag

## Vor dem Vortrag

### Technische Vorbereitung
- [ ] Python 3.8+ installiert
- [ ] Abhängigkeiten installiert (`pip install -r requirements.txt`)
- [ ] Demo einmal durchlaufen (alle Funktionen testen)
- [ ] Tests ausführen (`python run_tests.py`)
- [ ] Beispiel-Muster geladen und getestet
- [ ] Bildschirm-Auflösung geprüft (ist alles gut sichtbar?)
- [ ] Code-Editor vorbereitet (Syntax-Highlighting, große Schrift)

### Inhaltliche Vorbereitung
- [ ] MVC-Diagramm vorbereitet (z.B. auf Whiteboard oder Folie)
- [ ] Code-Snippets markiert die gezeigt werden sollen
- [ ] Zeitplanung gemacht (Architektur, Code, Demo, Diskussion)

## Während des Vortrags

### Teil 1: Einführung (2 Min)
- [ ] Conway's Game of Life kurz erklären
- [ ] 4 Regeln vorstellen
- [ ] Warum interessant für Informatik?

### Teil 2: Architektur (8 Min)
- [ ] MVC-Pattern erklären
  - [ ] Model = game_of_life_engine.py
  - [ ] View = game_of_life_view.py
  - [ ] Controller = game_of_life_controller.py
- [ ] Separation of Concerns demonstrieren
- [ ] Projektstruktur zeigen (File-Tree)

### Teil 3: Code-Walkthrough (12 Min)

**Engine (game_of_life_engine.py)**
- [ ] `count_neighbors()` Methode zeigen
  - [ ] NumPy Vektorisierung erklären
  - [ ] Vergleich zu verschachtelten Schleifen
- [ ] `step()` Methode zeigen
  - [ ] Regelanwendung mit Boolean Arrays
- [ ] `load_pattern_from_file()` zeigen
  - [ ] Dateiformat erklären

**View (game_of_life_view.py)**
- [ ] Nur Rendering, keine Logik
- [ ] `draw_grid()` Methode kurz zeigen
- [ ] Button-System erklären

**Controller (game_of_life_controller.py)**
- [ ] Event-Handling zeigen
- [ ] Koordination zwischen Model und View

### Teil 4: Live-Demo (10 Min)
- [ ] Anwendung starten
- [ ] **Glider** laden
  - [ ] Erklären: "Raumschiff" - bewegt sich
  - [ ] Laufen lassen, Bewegung zeigen
- [ ] **Blinker** laden
  - [ ] Erklären: Oszillator mit Periode 2
  - [ ] Ein paar Generationen laufen lassen
- [ ] **Block** laden
  - [ ] Erklären: Still Life - völlig stabil
  - [ ] Zeigen dass sich nichts ändert
- [ ] Pause und manuelle Zell-Manipulation
  - [ ] Neue Zellen setzen
  - [ ] Reaktion zeigen
- [ ] Tests ausführen
  - [ ] `python run_tests.py`
  - [ ] Zeigen: 21/21 Tests bestanden

### Teil 5: Code-Qualität (5 Min)
- [ ] Type Hints zeigen
- [ ] Docstrings zeigen
- [ ] Unit-Test Beispiel zeigen
  - [ ] z.B. `test_step_oscillator_blinker()`
  - [ ] Zeigen wie Test funktioniert

### Teil 6: Diskussion & Fragen (8 Min)
- [ ] Design-Entscheidungen diskutieren
- [ ] Alternativen erwähnen
- [ ] Erweiterungsmöglichkeiten
- [ ] Fragen beantworten

## Nach dem Vortrag

### Follow-up
- [ ] Code verfügbar machen (USB-Stick, Repository, Email)
- [ ] Auf Fragen reagieren
- [ ] Feedback einholen

## Notizen & Backup-Antworten

### "Warum MVC statt einfacher Lösung?"
**Antwort**: Bei kleinen Projekten mag es übertrieben wirken, aber:
1. Zeigt professionelle Arbeitsweise
2. In echten Projekten unverzichtbar
3. Macht Code testbar und wartbar
4. Ermöglicht Team-Arbeit

### "Ist NumPy wirklich so viel schneller?"
**Antwort**: Ja! Demo vorbereiten:
- Naive Implementierung: O(n²) für jeden Schritt
- NumPy: Vektorisierte Operationen, C-optimiert
- Faktor 50-100x schneller bei großen Grids

### "Warum Python und nicht C++/Java?"
**Antwort**:
- Python: Rapid Prototyping, klarer Code
- NumPy: C-Performance wo nötig
- Für Produktion: Performance-kritische Teile in C/Cython
- Zeigt: "Right tool for the job"

### "Was sind die größten Herausforderungen?"
**Antwort**:
1. Effiziente Nachbar-Zählung (gelöst mit NumPy)
2. Separation of Concerns beibehalten
3. Ausführliche Tests schreiben
4. Benutzerfreundliche UI

## Technische Probleme - Lösungen

### "Demo startet nicht"
- Dependencies prüfen
- Python-Version prüfen
- Backup: Code zeigen statt Demo

### "Muster laden funktioniert nicht"
- Pfad prüfen
- Dateiformat zeigen
- Backup: Manuell Zellen setzen

### "Tests schlagen fehl"
- PyGame installiert?
- Backup: Engine-Tests zeigen (funktionieren immer)

## Zeitmanagement

Gesamt: 45 Minuten

- Einführung: 2 Min
- Architektur: 8 Min  (Total: 10 Min)
- Code: 12 Min        (Total: 22 Min)
- Demo: 10 Min        (Total: 32 Min)
- Qualität: 5 Min     (Total: 37 Min)
- Diskussion: 8 Min   (Total: 45 Min)

**Puffer einplanen!** Besser 5 Min zu früh fertig als überzogen.

## Wichtigste Botschaften

1. ✨ **Design Patterns sind wertvoll** - nicht nur Theorie
2. 🚀 **Performance matters** - aber erst nach Korrektheit
3. 🧪 **Tests sind essentiell** - speziell bei Refactoring
4. 📚 **Code-Qualität** - Lesbarkeit > Cleverness
5. 🎯 **Separation of Concerns** - macht alles einfacher

Viel Erfolg! 🍀
