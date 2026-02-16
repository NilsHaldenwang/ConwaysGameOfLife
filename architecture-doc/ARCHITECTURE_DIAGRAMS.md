# Architektur-Diagramme - Conway's Game of Life

Diese Dokumentation erklärt die verschiedenen Architektur-Diagramme für das Conway's Game of Life Projekt.

## 📊 Verfügbare Diagramme

### 1. **architecture_diagram.mermaid** - MVC Übersicht
Zeigt die grundlegende MVC-Architektur und die Hauptkomponenten.

**Komponenten:**
- 🔵 **Controller** (Blau): Koordiniert alles
- 🟢 **Model/Engine** (Grün): Spiellogik mit NumPy
- 🟠 **View** (Orange): PyGame Visualisierung
- ❌ Gestrichelte Linien: Keine direkte Kommunikation (Separation of Concerns)

### 2. **component_diagram.mermaid** - Detaillierte Komponenten
Zeigt die internen Komponenten jeder Schicht.

**Komponenten:**
- **Engine**: Grid State, Rules, Neighbor Counting, Pattern Loader
- **View**: Grid Renderer, UI Renderer, Event Detection, Display
- **Controller**: Event Handler, State Manager, Coordinator

### 3. **sequence_diagram.mermaid** - Interaktionsablauf
Zeigt die zeitliche Abfolge von Benutzeraktionen.

**Dargestellte Szenarien:**
1. Pattern laden
2. Simulation starten
3. Simulation läuft (Loop)
4. Simulation pausieren
5. Zelle manuell togglen
6. Grid löschen

### 4. **dataflow_diagram.mermaid** - Datenfluss
Zeigt wie Daten durch das System fließen.

**Datenfluss-Schritte:**
1. User Input → Events
2. Events → Commands
3. Commands → Grid Manipulation
4. Grid → Neighbor Calculation (NumPy)
5. Neighbors → Rule Application
6. New Grid → Rendering
7. Rendering → Visual Output

## 🎨 Farbcodierung (in allen Diagrammen konsistent)

- **🔵 Blau** = Controller-Komponenten
- **🟢 Grün** = Model/Engine-Komponenten  
- **🟠 Orange** = View-Komponenten
- **🔴 Rot** = User/External
- **🟣 Lila** = External Resources (Dateien)

## 📖 Diagramme anzeigen

### In Markdown-Viewer (z.B. GitHub, VS Code)
Die `.mermaid` Dateien werden automatisch gerendert in:
- GitHub
- GitLab
- VS Code (mit Mermaid Extension)
- Obsidian
- Notion

### Online Viewer
Oder kopieren Sie den Inhalt in:
- https://mermaid.live/
- https://mermaid-js.github.io/mermaid-live-editor/

### In Präsentation einbinden
- Screenshot von Mermaid Live erstellen
- In PowerPoint/Google Slides einfügen
- Oder: Mermaid Plugin für Reveal.js nutzen

## � Design-Entscheidungen

### Warum MVC?
- ✅ **Testbarkeit**: Jede Komponente isoliert testbar
- ✅ **Wartbarkeit**: Änderungen in einer Schicht beeinflussen andere nicht
- ✅ **Erweiterbarkeit**: Neue Features leicht hinzufügbar
- ✅ **Team-Arbeit**: Verschiedene Entwickler an verschiedenen Schichten

### Warum kein direkter Model-View Zugriff?
- ❌ **Verhindert**: Enge Kopplung
- ✅ **Ermöglicht**: UI-Austausch (z.B. PyGame → Tkinter)
- ✅ **Ermöglicht**: Engine-Austausch (z.B. andere Regelsets)

### Warum NumPy im Model?
- 🚀 **Performance**: 50-100x schneller als Python-Loops
- 📊 **Klarheit**: Code ist lesbar trotz Effizienz
- 🔬 **Standard**: Wissenschaftlicher Python-Standard

## 📚 Literatur zu den Patterns

**MVC Pattern:**
- Krasner & Pope (1988): "A Description of the Model-View-Controller User Interface Paradigm"
- Gamma et al. (1994): "Design Patterns" - Observer Pattern

**Separation of Concerns:**
- Dijkstra (1974): "On the role of scientific thought"
- Martin (2008): "Clean Code" - Single Responsibility Principle

**Data Flow Architecture:**
- Shaw & Garlan (1996): "Software Architecture: Perspectives on an Emerging Discipline"

