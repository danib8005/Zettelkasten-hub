---
type: System
translation_of: docs/workbench.md
---
<!-- Deutsche Übersetzung, nicht massgebend. Massgebend ist docs/workbench.md. -->
# Werkbank

Eine Werkbank ist ein zweites Bundle für das, was du tust, neben dem Notizen-Bundle für das, was du weisst. Das Notizen-Bundle hält Wissen: Quellen, Konzepte, Synthesen, eigene Texte. Die Werkbank hält **Vorhaben**: Projekte, Aufträge, Workshops, Vorbereitungen. Der entscheidende Unterschied fürs Teilen: Ein Vorhaben gehört zu einem Ort und einem Kreis von Menschen, ein Konzept nicht.

## Warum trennen
- **Vertraulichkeit durch Struktur, nicht durch Listen.** Ohne Werkbank liegen Projektnotizen in den Notizen, und jeder Export braucht eine Liste, was gehen darf. Mit Werkbank ist ein Vorhaben, das auf einem Gerät bleiben muss, im anderen Bundle schlicht nicht vorhanden.
- **Jedes Bundle liegt dort, wo es hingehört.** Die Notizen lassen sich auf mehrere Geräte kopieren (siehe [Architektur](architecture.md), §7); eine Werkbank bleibt dort, wo ihre Vorhaben hingehören, etwa eine auf dem Arbeitsnotebook und eine auf dem privaten Computer.
- **Eine Richtung der Abhängigkeit.** Vorhaben bauen auf Wissen auf; Wissen darf nicht von einem Vorhaben abhängen, das vielleicht nicht da ist.

## Aufbau
```
Notes/          das Notizen-Bundle (alle Geräte, die es brauchen; anderswo erzeugte Kopien)
Workbench/      eine Werkbank pro Vertraulichkeitskreis, z. B. Workbench-Work, Workbench-Private
```
Die Bundles liegen nebeneinander. **Der Notizen-Ordner heisst auf jedem Gerät gleich**, weil Vorhaben ihn per relativem Pfad verlinken.

In einer Werkbank:
```
00_Inbox/         Unverarbeitetes
10_Undertakings/  ein Ordner pro Vorhaben, darin undertaking.md (Vorlage: templates/undertaking.md); auch 10_Vorhaben ist erlaubt
20_Material/      Folien, PDFs, Rohdaten (kein Frontmatter nötig)
30_Decisions/     Entscheide mit Begründung, die über ein Vorhaben hinaus gelten
95_System/        Vorlagen, Systemnotizen
```
Eine Werkbank wird in ihrer `perspective.md` markiert: `kind: workbench`.

## Regeln
1. **Ein Zuhause pro Vorhaben.** Ein Gerät, eine Vertraulichkeitsstufe. Reicht ein Vorhaben in zwei Kreise (etwa Arbeit und Forschung), werden es zwei Vorhaben, die sich in `counterpart:` als Text nennen. Zwischen Werkbänken wird nichts synchronisiert.
2. **Links laufen in eine Richtung.** Von der Werkbank in die Notizen, als relativer Pfad zum Geschwister-Ordner: `[Konzept](../Notes/10_Concepts/x.md)`. Die Notizen verlinken nie in eine Werkbank. `tools/check.py` meldet beide Fehler.
3. **Wissen kommt nur durch Beförderung zurück.** Was ein Vorhaben dich gelehrt hat und auch ohne es gilt, wird als allgemeine, anonymisierte Notiz im Notizen-Bundle neu geschrieben, zuerst als Entwurf. Dateien werden nie aus einem Vorhaben in die Notizen verschoben oder kopiert. Der Abschnitt «Kann eine Notiz werden» der Vorlage sammelt die Kandidaten.
4. **Eine gemischte Datei wird getrennt, nicht synchronisiert.** Der Teil, der nur wegen des Vorhabens existiert, bleibt; der allgemeine Teil wird eine Notiz.
5. **Aus einer Werkbank wird nichts exportiert.** `tools/export.py` verweigert ein Bundle mit `kind: workbench`; `visibility:` hat dort keine Bedeutung (`tools/check.py` meldet es).
6. **Reflexionen bleiben aus Arbeitswerkzeugen.** Persönliche Reflexionen (Erlebnislog, Feedbackberichte, Notizen zu Personen) gehören in eine private Werkbank oder die privaten Notizen, auch wenn sie von der Arbeit handeln.
7. **Personen mit Rolle.** Rolle oder vereinbartes Kürzel, wie in `AGENTS.md`.

## Prüfung
`python tools/check.py Workbench --workbench` (oder nur der Pfad, wenn `perspective.md` `kind: workbench` sagt). Prüft Struktur und Review-Status wie bei Notizen, erlaubt Links `../<Notizen-Ordner>/…` und meldet `visibility:`.

## Noch nicht gebaut
- Ein Beförderungs-Skill (Vorhaben → Notiz-Entwurf, mit Anonymisierungs-Prüfung).
- Skills rund um Vorhaben: Briefing, To-dos, Plan, Präsentation.
- Eine Backup-Regel für eine Werkbank, die nur auf einem Gerät liegt: das entscheidet die Besitzerin oder der Besitzer.
