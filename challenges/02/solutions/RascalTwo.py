import random
import string

def generate_password(length: int, digits: int = 0, specials: int = 0) -> str:
	"""Generate password of length with digits and specials"""
	if length and digits and specials and digits + specials > length:
		raise Exception(f'Cannot add {digits} digit and {specials} special characters to a {length} character long password')

	chars = (
		random.choices(string.ascii_letters, k=length - digits - specials)
		+ random.choices(string.digits, k=min(length, digits))
		+ random.choices(string.punctuation, k=min(length, specials))
	)

	random.shuffle(chars)
	return ''.join(chars)


SOLVERS = [generate_password]

if __name__ == '__main__':
	from app import run_solution_directly
	run_solution_directly(__file__)
