#!/usr/bin/env python3

import os
import io
import sys
import importlib
import unittest
from datetime import datetime

from typing import Iterable, NamedTuple, List, Callable, Any, Tuple
from types import ModuleType


class FullResult(unittest.TestResult):
	def __init__(self, stream, descriptions, verbosity: int) -> None:
		super().__init__(stream, descriptions, verbosity)
		self.verbosity = verbosity

	test_to_prefix = staticmethod(lambda test: f'      "{test._testMethodName}"')

	def startTest(self, test: unittest.TestCase):
		"""Record start time and output if verbose"""
		super().startTest(test)
		test._r2_started = datetime.now()

		if self.verbosity >= 2:
			print(self.test_to_prefix(test) + '...\r', end='', flush=True)

	def stopTest(self, test):
		"""Record end time and output timings"""
		super().stopTest(test)
		test._r2_ended = datetime.now()

		delta = test._r2_ended - test._r2_started
		# Show seconds if any, otherwise show only microseconds
		took_str = f'{delta.seconds}.0000{delta.microseconds}s' if delta.seconds else f'{delta.microseconds}mu'

		if self.verbosity < 2:
			print(f'      {took_str}\t', end='', flush=True)
		else:
			print(f'{self.test_to_prefix(test)} took {took_str}')

	def stopTestRun(self):
		"""If not verbose, add required newline"""
		if self.verbosity < 2:
			print()


class Solutions(NamedTuple):
	"""User-submitted solutions"""
	username: str
	solvers: List[Callable[..., Any]]

class Challenge(NamedTuple):
	number: int
	name: str
	testcase: unittest.TestCase
	solutions: List[Solutions]


def import_module_from_file(abspath: str) -> ModuleType:
	"""Import module from absolute filepath"""
	spec = importlib.util.spec_from_file_location('module.name', abspath)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def import_challenge(abspath: str, number: int) -> Challenge:
	"""Import a Challenge from a abspath"""
	with open(os.path.join(abspath, 'INSTRUCTIONS.md'), 'r') as instructions:
		challenge_name = instructions.readline().split('#')[1].strip()

	challenge = Challenge(
		number,
		challenge_name,
		import_module_from_file(os.path.join(abspath, 'tests.py')).TestChallenge,
		[]
	)

	for user_filename in (user_filename[:-3] for user_filename in os.listdir(os.path.join(abspath, 'solutions')) if user_filename.endswith('.py')):
		solvers = import_module_from_file(os.path.join(abspath, 'solutions', user_filename + '.py')).SOLVERS
		challenge.solutions.append(Solutions(user_filename, solvers))

	return challenge


def test_solvers(testcase: unittest.TestCase, solvers: List[Callable], verbose=False, stream=None) -> None:
	test_names = unittest.defaultTestLoader.getTestCaseNames(testcase)

	for solver in solvers:
		print('    ' + solver.__name__)
		suite = unittest.TestSuite()
		for test_name in test_names:
			suite.addTest(testcase(solver=solver, methodName=test_name))

		result = unittest.TextTestRunner(stream=stream or io.StringIO(), verbosity=int(verbose) + 1, resultclass=FullResult).run(suite)

		for decor, name in (('-', 'failures'), ('=', 'errors')):
			results: List[Tuple[unittest.TestCase, str]] = getattr(result, name)
			if not results:
				continue

			print(f'{decor * 10}{name.upper()}{decor * 10}')
			for test, traceback in results:
				print(test)
				print(traceback)
			print(f'{decor * 10}{decor * len(name)}{decor * 10}')


def run_solution_directly(solution_filepath: str) -> None:
	"""Run a single solution by absolute filepath"""
	challenge_directory = '/'.join(solution_filepath.split('/')[:-2])
	username = solution_filepath.split('/')[-1][:-3]

	challenge = import_challenge(challenge_directory, challenge_directory.split('/')[-1])
	solution = next(solution for solution in challenge.solutions if solution.username == username)

	test_solvers(challenge.testcase, solution.solvers, 'verbose' in sys.argv)


def main(verbose=False):
	"""Collect challenges and run solutions through tests"""
	# Stream to throw away end-of-test messages and total-time spent
	runner_stream = io.StringIO()

	for directory in sorted(os.listdir('challenges')):
		challenge = import_challenge(os.path.join('challenges', directory), int(directory))
		print(f'\nChallenge #{challenge.number} - {challenge.name}')

		for solutions in challenge.solutions:
			# Username's solution OR Username's X solutions
			print(f'\n  {solutions.username}\'s {"solution" if len(solutions.solvers) <= 1 else str(len(solutions.solvers)) + " solutions"}\n')

			test_solvers(challenge.testcase, solutions.solvers, verbose, runner_stream)

if __name__ == '__main__':
	main('verbose' in sys.argv)
