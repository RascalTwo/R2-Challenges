import string

import unittest

from typing import Callable

class TestChallenge(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		self.solver: Callable = kwargs.pop('solver')
		super().__init__(*args, **kwargs)

	def test_letter(self):
		"""Characters are letters"""
		password = self.solver(6)
		self.assertEqual(len(password), 6)

		for char in password:
			self.assertTrue(char.isalpha())

	def test_randomized(self):
		"""Passwords are randomized"""
		password = self.solver(6)
		self.assertNotEqual(password, sorted(password))
		self.assertNotEqual(password, sorted(password, reverse=True))

	def test_numbers(self):
		"""Numbers generate entire password"""
		password = self.solver(6, 6)
		self.assertEqual(len(password), 6)

		for char in password:
			self.assertTrue(char.isnumeric())

	def test_number_half(self):
		"""Numbers generate only half password"""
		password = self.solver(6, 3)
		self.assertEqual(len(password), 6)

		# [ num, str ]
		counts = [3, 3]
		for char in password:
			index = int(char.isalpha())
			counts[index] -= 1

		self.assertEqual(counts, [0, 0])

	def test_specials(self):
		"""Specials generate"""
		password = self.solver(6, 0, 6)
		self.assertEqual(len(password), 6)

		for char in password:
			self.assertIn(char, string.punctuation)

	def test_mixed(self):
		"""All three types generate"""
		password = self.solver(9, 3, 3)
		self.assertEqual(len(password), 9)

		# [ num, punct, str ]
		counts = [3, 3, 3]
		for char in password:
			index = 0 if char.isnumeric() else int(char.isalpha()) + 1
			counts[index] -= 1

		self.assertEqual(counts, [0, 0, 0])

	def test_length(self):
		"""Password is limited to length"""
		password = self.solver(5, 10)
		self.assertEqual(len(password), 5)

	def test_empty_conflicting(self):
		"""Empty password with conflicting counts passes"""
		self.assertEqual(self.solver(0, 3, 3), '')
		self.assertEqual(self.solver(0, 0, 1), '')

	def test_conflicting(self):
		"""Conflicting counts of characters raises exception"""
		with self.assertRaisesRegex(Exception, 'Cannot add 2 digit and 3 special characters to a 1 character long password'):
			self.solver(1, 2, 3)
