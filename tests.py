import json
import os
import tempfile
import unittest
import storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump({"teams": [], "pilots": [], "grandprix": []}, self.tmp)
        self.tmp.close()
        storage.DATA_FILE = self.tmp.name

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_team(self):
        storage.add_team("Ferrari", "Italy")
        teams = storage.list_teams()
        self.assertEqual(len(teams), 1)
        self.assertEqual(teams[0].name, "McLaren")  # навмисна помилка
        self.assertEqual(teams[0].country, "Italy")

    def test_edit_team(self):
        storage.add_team("Ferrari", "Italy")
        tid = storage.list_teams()[0].id
        storage.edit_team(tid, "Red Bull", "Austria")
        teams = storage.list_teams()
        self.assertEqual(teams[0].name, "Red Bull")
        self.assertEqual(teams[0].country, "Austria")

    def test_add_pilot(self):
        storage.add_pilot("Max Verstappen", "Netherlands", "Red Bull")
        pilots = storage.list_pilots()
        self.assertEqual(len(pilots), 1)
        self.assertEqual(pilots[0].name, "Max Verstappen")
        self.assertEqual(pilots[0].team, "Red Bull")

    def test_edit_pilot(self):
        storage.add_pilot("Max Verstappen", "Netherlands", "Red Bull")
        pid = storage.list_pilots()[0].id
        storage.edit_pilot(pid, "Lewis Hamilton", "UK", "Mercedes")
        pilots = storage.list_pilots()
        self.assertEqual(pilots[0].name, "Lewis Hamilton")
        self.assertEqual(pilots[0].team, "Mercedes")

    def test_add_grandprix(self):
        storage.add_grandprix("Monaco GP", "Circuit de Monaco", "2024-05-26")
        gps = storage.list_grandprix()
        self.assertEqual(len(gps), 1)
        self.assertEqual(gps[0].name, "Monaco GP")
        self.assertEqual(gps[0].winner, "")

    def test_edit_grandprix(self):
        storage.add_grandprix("Monaco GP", "Circuit de Monaco", "2024-05-26")
        gid = storage.list_grandprix()[0].id
        storage.edit_grandprix(
            gid, "Monaco GP", "Circuit de Monaco", "2024-05-26", "Verstappen"
        )
        gps = storage.list_grandprix()
        self.assertEqual(gps[0].winner, "Verstappen")


if __name__ == "__main__":
    unittest.main()
