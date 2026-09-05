"""Run with: python -B -m unittest test_cues -v. No hardware is used."""
import unittest
import hashlib
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from types import SimpleNamespace
from unittest.mock import patch

import Script


class RecordingDisplay:
    def __init__(self):
        self.images = []

    def Display(self, image):
        self.images.append(image)


class FakeButton:
    def __init__(self):
        self.latched = set()

    def Reset(self):
        self.latched.clear()

    def IsLatched(self, button):
        return button in self.latched


class EmptyCanvas:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def GetImage(self):
        return "empty black canvas"


class CueTests(unittest.TestCase):
    def setUp(self):
        self.cues = SimpleNamespace(Cue=object(), Cue01=object(), Cue02=object())
        self.display = RecordingDisplay()
        self.button = FakeButton()
        self.state = SimpleNamespace(ID="SELECTION", RunningTime=0, Status="")
        self.context = SimpleNamespace(
            Assets=SimpleNamespace(
                Images=SimpleNamespace(
                    Cross=object(), Stimulating=object(),
                    RatingInstruction=object(), Empty=object()),
                Cues=self.cues),
            Instruments=SimpleNamespace(ImageDisplay=self.display, Button=self.button),
            CurrentState=self.state,
            Image=SimpleNamespace(GetCanvas=lambda *args: EmptyCanvas()),
            Log=SimpleNamespace(Information=lambda *args: None))
        self.task = Script.CreateTask(self.context)

    def enter(self, state):
        self.state.ID = state
        self.state.RunningTime = 0
        self.assertTrue(self.task.Enter(None))

    def test_selection_displays_both_cues(self):
        self.enter("SELECTION")
        self.assertIs(self.cues.Cue, self.display.images[-1])

    def test_each_button_displays_its_selected_cue(self):
        for button, expected in (("1", self.cues.Cue01), ("2", self.cues.Cue02)):
            with self.subTest(button=button):
                self.enter("SELECTION")
                self.button.latched.add(button)
                self.assertEqual("DISPLAY", self.task.Update())
                self.enter("DISPLAY")
                self.assertIs(expected, self.display.images[-1])

    def test_timeout_selects_either_cue_after_four_seconds(self):
        for expected in (self.cues.Cue01, self.cues.Cue02):
            with self.subTest(cue=expected):
                self.enter("SELECTION")
                self.state.RunningTime = 4000
                self.assertEqual("*", self.task.Update())
                self.state.RunningTime = 4001
                with patch.object(Script.random, "choice", return_value=expected) as choose:
                    self.assertEqual("DISPLAY", self.task.Update())
                    choose.assert_called_once_with([self.cues.Cue01, self.cues.Cue02])
                self.enter("DISPLAY")
                self.assertIs(expected, self.display.images[-1])

    def test_new_round_shows_both_cues_and_waits_for_fresh_input(self):
        self.enter("SELECTION")
        self.button.latched.add("1")
        self.assertEqual("DISPLAY", self.task.Update())
        self.enter("DISPLAY")
        self.button.latched.add("1")
        self.enter("SELECTION")
        self.assertIs(self.cues.Cue, self.display.images[-1])
        self.assertEqual("*", self.task.Update())
        self.button.latched.add("2")
        self.assertEqual("DISPLAY", self.task.Update())
        self.enter("DISPLAY")
        self.assertIs(self.cues.Cue02, self.display.images[-1])

    def test_selected_cue_keeps_existing_display_duration(self):
        self.enter("SELECTION")
        self.button.latched.add("1")
        self.task.Update()
        self.enter("DISPLAY")
        self.state.RunningTime = 1999
        self.assertEqual("*", self.task.Update())
        self.state.RunningTime = 2000
        self.assertEqual("STIMULATION", self.task.Update())

    def test_declared_cue_assets_match_reference_and_reach_display(self):
        root = Path(__file__).resolve().parent
        definition = ET.parse(root / "intro.sequential.expx")
        asset = definition.find("./protocol/assets/file-asset[@id='Cues']")
        self.assertIsNotNone(asset)
        expected_hashes = {
            "Cue": "cda5b1aece91ac42f7447590c911646a995375a2ea2215fce56b3616a5434615",
            "Cue01": "a79eb323f016f5e9b934c7a02df7fcafc146dc0f93c859053bc32e6c037a9abd",
            "Cue02": "65ffa76bd39f01e1a5b239c024c4a0d6a11c811ecbc6861a3344f62b54e4a872",
        }
        # Original PNG bytes from TestRepository/procedures.sequential/Images.zip.
        with ZipFile(root / asset.attrib["file"]) as archive:
            self.assertEqual({name + ".png" for name in expected_hashes}, set(archive.namelist()))
            images = {}
            for name, expected_hash in expected_hashes.items():
                image = archive.read(name + ".png")
                self.assertEqual(expected_hash, hashlib.sha256(image).hexdigest())
                images[name] = image
        self.context.Assets.Cues = SimpleNamespace(**images)
        self.task = Script.CreateTask(self.context)
        self.enter("SELECTION")
        self.assertEqual(images["Cue"], self.display.images[-1])
        for button, name in (("1", "Cue01"), ("2", "Cue02")):
            self.enter("SELECTION")
            self.button.latched.add(button)
            self.assertEqual("DISPLAY", self.task.Update())
            self.enter("DISPLAY")
            self.assertEqual(images[name], self.display.images[-1])


if __name__ == "__main__":
    unittest.main()
