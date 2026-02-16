# Architektur-Diagramme - Conway's Game of Life

Diese Dokumentation erklärt das MVC-Architektur-Diagramm für das Conway's Game of Life Projekt.

## 📊 architecture_diagram.mermaid - MVC Übersicht
Zeigt die grundlegende MVC-Architektur und die Hauptkomponenten.

**Komponenten:**
- 🔵 **Controller** (Blau): Koordiniert alles
- 🟢 **Model/Engine** (Grün): Spiellogik mit NumPy
- 🟠 **View** (Orange): PyGame Visualisierung
- ❌ Gestrichelte Linien: Keine direkte Kommunikation (Separation of Concerns)

## 🎨 Farbcodierung

- **🔵 Blau** = Controller-Komponenten
- **🟢 Grün** = Model/Engine-Komponenten  
- **🟠 Orange** = View-Komponenten
- **🔴 Rot** = User/External
- **🟣 Lila** = External Resources (Dateien)

## 📖 Diagramm anzeigen

### In Markdown-Viewer (z.B. GitHub, VS Code)
Die `.mermaid` Datei wird automatisch gerendert in:
- GitHub
- GitLab
- VS Code (mit Mermaid Extension)
- Obsidian
- Notion

### Online Viewer
Oder kopieren Sie den Inhalt in:
- https://mermaid.live/
- https://mermaid-js.github.io/mermaid-live-editor/


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

