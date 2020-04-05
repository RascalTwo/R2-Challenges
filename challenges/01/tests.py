import unittest

from typing import Callable, List, Optional, Tuple


class TestChallenge(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		self.solver: Callable[[List[int], int], Optional[Tuple[int, int]]] = kwargs.pop('solver')
		super().__init__(*args, **kwargs)

	def assertBothWays(self, first, pair):
		"""Assert result is pair or reversed pair"""
		self.assertIn(first, (pair, pair[::-1]))

	def test_first_last(self):
		"""The entire list is being searched"""
		self.assertBothWays(self.solver([10, 15, 3, 7], 70), (10, 7))

	def test_last_two(self):
		"""Values are being properly changed from their inital values"""
		self.assertBothWays(self.solver([8, 6, 3, 2], 18), (6, 3))

	def test_none(self):
		"""Returns None when no solution exists"""
		self.assertIsNone(self.solver([4, 2, 7, 6], 29))

	def test_larger(self):
		"""Handles large numbers"""
		self.assertBothWays(self.solver([26, 8, 385, 687, 9413, 587], 5496), (8, 687))

	def test_large_list(self):
		"""Handles large input list"""
		self.assertBothWays(self.solver([975, 799, 822, 927, 211, 719, 847, 925, 677, 991, 909, 939, 805, 443, 495, 611, 258, 844, 586, 772, 706, 655, 900, 642, 720, 131, 453, 737, 480, 972, 869, 168, 638, 816, 392, 509, 318, 993, 668, 952, 117, 240, 743, 208, 767, 766, 295, 931, 930, 749, 283, 387, 357, 908, 650, 181, 319, 997, 141, 612, 731, 417, 440, 832, 802, 454, 390, 322, 629, 109, 192, 429, 476, 507, 433, 441, 778, 878, 680, 462, 309, 541, 112, 648, 142, 614, 953, 175, 107, 416, 170, 503, 838, 667, 202, 697, 529, 890, 681, 652], 444012), (681, 652))
