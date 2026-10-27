import tempfile
import unittest
from pathlib import Path

import tidy


class TidyTests(unittest.TestCase):
    def make_folder(self, names):
        folder = Path(tempfile.mkdtemp())
        for name in names:
            (folder / name).write_text("x")
        return folder

    def test_category_for(self):
        self.assertEqual(tidy.category_for(Path("photo.JPG")), "Images")
        self.assertEqual(tidy.category_for(Path("report.pdf")), "Documents")
        self.assertEqual(tidy.category_for(Path("mystery.xyz")), "Other")
        self.assertEqual(tidy.category_for(Path("noextension")), "Other")

    def test_preview_moves_nothing(self):
        folder = self.make_folder(["a.png", "b.pdf"])
        tidy.tidy(folder, apply=False)
        self.assertTrue((folder / "a.png").exists())
        self.assertFalse((folder / "Images").exists())

    def test_apply_moves_files(self):
        folder = self.make_folder(["a.png", "b.pdf", "c.xyz"])
        tidy.tidy(folder, apply=True)
        self.assertTrue((folder / "Images" / "a.png").exists())
        self.assertTrue((folder / "Documents" / "b.pdf").exists())
        self.assertTrue((folder / "Other" / "c.xyz").exists())

    def test_never_overwrites(self):
        folder = self.make_folder(["a.png"])
        (folder / "Images").mkdir()
        (folder / "Images" / "a.png").write_text("existing")
        tidy.tidy(folder, apply=True)
        self.assertEqual((folder / "Images" / "a.png").read_text(), "existing")
        self.assertTrue((folder / "Images" / "a (1).png").exists())

    def test_ignores_hidden_files_and_folders(self):
        folder = self.make_folder([".hidden.png"])
        (folder / "subdir").mkdir()
        self.assertEqual(tidy.plan_moves(folder), [])


if __name__ == "__main__":
    unittest.main()
