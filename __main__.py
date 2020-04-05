import os
import io
import sys
import importlib
import unittest
from datetime import datetime

from typing import Iterable, NamedTuple, List, Callable, Any, Tuple


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


def import_challenges(root: str, solutions_dir: str) -> Iterable:
	"""Import challenge and solutions from directory"""
	import_root = root.replace(os.sep, ".")

	for directory in sorted(os.listdir(root)):
		dir_path = os.path.join(root, directory)

		# filename[:-3] removes ".py" extension
		for filename in (filename[:-3] for filename in os.listdir(dir_path) if filename.endswith('.py')):
			with open(os.path.join(dir_path, 'INSTRUCTIONS.md'), 'r') as instructions:
				challenge_name = instructions.readline().split('#')[1].strip()

			challenge = Challenge(
				int(directory),
				challenge_name,
				importlib.import_module(f'{import_root}.{directory}.{filename}').TestChallenge,
				[]
			)

			for user_filename in (user_filename[:-3] for user_filename in os.listdir(os.path.join(dir_path, solutions_dir)) if user_filename.endswith('.py')):
				solutions = importlib.import_module(f'{import_root}.{directory}.{solutions_dir}.{user_filename}').SOLUTIONS
				challenge.solutions.append(Solutions(user_filename, solutions))

			yield challenge

def main(verbose=False):
	"""Collect challenges and run solutions through tests"""
	# Stream to throw away end-of-test messages and total-time spent
	runner_stream = io.StringIO()

	for challenge in import_challenges('challenges', 'solutions'):
		test_names = unittest.defaultTestLoader.getTestCaseNames(challenge.testcase)

		print(f'Challenge #{challenge.number} - {challenge.name}')
		for solutions in challenge.solutions:
			# Username's solution OR Username's X solutions
			print(f'\n  {solutions.username}\'s {"solution" if len(solutions.solvers) <= 1 else str(len(solutions.solvers)) + " solutions"}\n')

			for solver in solutions.solvers:
				print('    ' + solver.__name__)
				suite = unittest.TestSuite()
				for test_name in test_names:
					suite.addTest(challenge.testcase(solver=solver, methodName=test_name))

				result = unittest.TextTestRunner(stream=runner_stream, verbosity=int(verbose) + 1, resultclass=FullResult).run(suite)

				for decor, name in (('-', 'failures'), ('=', 'errors')):
					results: List[Tuple[unittest.TestCase, str]] = getattr(result, name)
					if not results:
						continue

					print(f'{decor * 10}{name.upper()}{decor * 10}')
					for test, traceback in results:
						print(test)
						print(traceback)
					print(f'{decor * 10}{decor * len(name)}{decor * 10}')

if __name__ == '__main__':
	main('verbose' in sys.argv)
