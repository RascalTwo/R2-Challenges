import unittest

from typing import Callable

class TestChallenge(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		self.solver: Callable = kwargs.pop('solver')
		super().__init__(*args, **kwargs)
