import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import board, on_shift, to_minutes

def row(agent, start, end, status):
    return {"agent": agent, "shift_start": start, "shift_end": end, "status": status}

SAMPLE = [row("Ayesha Khan", "08:00", "16:00", "available"),
          row("Bilal Ahmed", "08:00", "16:00", "busy"),
          row("Sara Malik", "09:00", "17:00", "available"),
          row("Omar Farooq", "14:00", "22:00", "available"),
          row("Hina Raza", "08:00", "12:00", "on-break"),
          row("Danish Ali", "22:00", "06:00", "available")]

class TestAvailabilityBoard(unittest.TestCase):
    def test_grouping(self):
        groups, _ = board(SAMPLE, "10:30")
        self.assertEqual([a for a, _, _ in groups["AVAILABLE"]],
                         ["Ayesha Khan", "Sara Malik"])
        self.assertEqual([a for a, _, _ in groups["ON BREAK"]], ["Hina Raza"])
        self.assertEqual([a for a, _, _ in groups["BUSY"]], ["Bilal Ahmed"])
        self.assertEqual([a for a, _, _ in groups["OFF SHIFT"]],
                         ["Omar Farooq", "Danish Ali"])

    def test_next_on_shift(self):
        _, next_on = board(SAMPLE, "10:30")
        self.assertEqual(next_on, ("Omar Farooq", 840, "14:00"))

    def test_overnight_shift_on_shift(self):
        self.assertTrue(on_shift(1320, 360, 60))
        self.assertTrue(on_shift(1320, 360, 1380))

    def test_overnight_shift_off_shift(self):
        self.assertFalse(on_shift(1320, 360, 630))

    def test_shift_start_is_on_shift(self):
        self.assertTrue(on_shift(480, 960, 480))

    def test_shift_end_is_off_shift(self):
        self.assertFalse(on_shift(480, 960, 960))

    def test_empty_input(self):
        groups, next_on = board([], "10:30")
        self.assertEqual((groups, next_on),
                         ({"AVAILABLE": [], "ON BREAK": [], "BUSY": [], "OFF SHIFT": []}, None))

    def test_to_minutes(self):
        self.assertEqual(to_minutes("10:30"), 630)
