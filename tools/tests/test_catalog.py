import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import catalog

NOTE = """---
type: Source
visibility: public
---
# Perri (2018) - Build Trap

## Bibliographische Information
**Vollständige Referenz:**
Perri, Melissa. 2018. *Escaping the Build Trap*. O'Reilly.

**Format:** Kindle

## Kernthese
Outcomes vor Outputs.

> "Everyone is so focused on shipping." (Loc. 229-230)

## Zusammenfassung
Nicht im Katalog.

## Metadaten
- **Tags:** #typ/buch
"""

class T(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "40_Sources").mkdir()
        (self.d / "40_Sources" / "perri-2018-build-trap.md").write_text(NOTE, encoding="utf-8")
        (self.d / "40_Sources" / "priv.md").write_text(NOTE.replace("visibility: public\n", ""), encoding="utf-8")
        self.m = "# Kat\n## Produkt\nScope.\n- perri-2018-build-trap\n- priv\n- fehlt\n"

    def test_entry_with_quote(self):
        files, warns = catalog.build(self.d, self.m)
        c = files["catalog-produkt.md"]
        self.assertIn("Outcomes vor Outputs", c)
        self.assertIn("(Loc. 229-230)", c)
        self.assertIn("Perri, Melissa. 2018", c)
        self.assertNotIn("Nicht im Katalog", c)
        self.assertNotIn("Kindle", c)
        self.assertIn("/40_Sources/perri-2018-build-trap.md", c)
        self.assertTrue(any("priv" in w for w in warns) and any("fehlt" in w for w in warns))

    def test_strip_and_private(self):
        files, _ = catalog.build(self.d, self.m, strip=True, include_private=True)
        c = files["catalog-produkt.md"]
        self.assertNotIn("Loc.", c)
        self.assertEqual(c.count("### "), 2)

if __name__ == "__main__":
    unittest.main()
