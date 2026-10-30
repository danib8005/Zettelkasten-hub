---
type: Export profile
translation_of: templates/export-profile.md   # Übersetzung, nicht massgebend; beim Kopieren entfernen
name: arbeit
folders: [40_Sources, 70_Tools]
visibility: [team, public]
include: []
exclude: []
strip-quotes: false
leak-terms: 95_System/personen-schluessel.md
---
# Export-Profil: [Ziel, z. B. Arbeitslaptop]

Aufruf: `python tools/export.py BUNDLE_DIR DIESE_DATEI -o OUT_DIR` (zuerst mit `--dry-run`). Das Frontmatter oben ist das Profil; dieser Text ist für Menschen.

## Was die Schlüssel bedeuten
- `folders`: Notiz-Ordner, aus denen genommen wird. Eine Notiz braucht `visibility:` mit einem der genannten Werte; ohne den Schlüssel ist sie privat.
- `include`: Pfade oder Globs, die du ausdrücklich freigibst, z. B. `65_Consulting/projekt-a/**`. Diese Notizen brauchen kein `visibility:`; eine als `private` markierte Notiz wird nie exportiert.
- `exclude`: Pfade oder Globs, die nie rausgehen, was auch sonst dafür spricht.
- `strip-quotes`: `true` entfernt Blockzitate und Loc./S.-Angaben (für Kopien, die andere lesen).
- `leak-terms`: Datei im Bundle mit Namen, die in der Kopie nicht vorkommen dürfen (Tabelle mit Spalte «Name» oder ein Begriff pro Zeile). Sie wird nie exportiert.

## Warum dieses Ziel bekommt, was es bekommt
[Ein oder zwei Sätze: welches Gerät oder Werkzeug, wer sieht es, was bleibt bewusst draussen.]

---

## Review-Status
- **Erstellt:** [JJJJ-MM-TT] von [Kürzel]
- **Letztes Review:** [JJJJ-MM-TT] von [Kürzel]
- **Review-Status:** ✓ Aktuell / ⚠️ Veraltet / 🔄 In Überarbeitung
