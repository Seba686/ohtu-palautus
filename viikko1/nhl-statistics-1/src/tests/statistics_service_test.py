import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_existing_player(self):
       self.assertEqual(self.stats.search("Semenko").name, "Semenko")

    def test_search_nonexisting_player(self):
       self.assertEqual(self.stats.search("abc"), None)
    
    def test_team_search(self):
        players = self.stats.team("EDM")
        self.assertTrue(all(i.team == "EDM" for i in players))

    def test_top_by_points(self):
        correct = ["Gretzky", "Lemieux", "Yzerman"]
        compare = []
        for i in self.stats.top(3, SortBy.POINTS):
            compare.append(i.name)
        self.assertEqual(correct, compare)
    
    def test_top_by_goals(self):
        correct = ["Lemieux", "Yzerman", "Kurri"]
        compare = []
        for i in self.stats.top(3, SortBy.GOALS):
            compare.append(i.name)
        self.assertEqual(correct, compare)

    def test_top_by_assists(self):
        correct = ["Gretzky", "Yzerman", "Lemieux"]
        compare = []
        for i in self.stats.top(3, SortBy.ASSISTS):
            compare.append(i.name)
        self.assertEqual(correct, compare)