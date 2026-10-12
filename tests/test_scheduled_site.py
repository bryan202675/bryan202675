import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_scheduled_site import INTERVAL_SECONDS, generate, slot_datetime, slot_for


class GeneratorTests(unittest.TestCase):
    def test_waits_until_next_five_hour_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            start = slot_datetime(slot_for(datetime(2026, 10, 12, tzinfo=timezone.utc)))
            self.assertEqual(len(generate(root, start)), 1)
            self.assertEqual(generate(root, start + timedelta(hours=4, minutes=59)), [])
            self.assertEqual(len(generate(root, start + timedelta(hours=5))), 1)
            self.assertEqual(len(json.loads((root / "catalog.json").read_text())), 2)

    def test_backfills_each_missed_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            start = slot_datetime(slot_for(datetime(2026, 10, 12, tzinfo=timezone.utc)))
            generate(root, start)
            created = generate(root, start + timedelta(hours=16))
            self.assertEqual(len(created), 3)
            self.assertEqual([item["slot"] for item in created], list(range(slot_for(start) + 1, slot_for(start) + 4)))

    def test_output_has_no_gradients_and_is_responsive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generate(root, datetime(2026, 10, 12, tzinfo=timezone.utc))
            css = (root / "styles.css").read_text()
            html = (root / "index.html").read_text()
            self.assertNotIn("gradient", css.lower())
            self.assertIn("@media(max-width:820px)", css)
            self.assertIn('name="viewport"', html)
            self.assertEqual(INTERVAL_SECONDS, 18000)


if __name__ == "__main__":
    unittest.main()
