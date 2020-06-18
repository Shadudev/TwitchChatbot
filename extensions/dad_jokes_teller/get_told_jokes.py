def main():
	with open('jokes.txt') as f:
		all_jokes = set(eval(f.read()))

	with open('Jokes\\jokes.txt') as f:
		untold_jokes = set(eval(f.read()))

	print('\n\n'.join(all_jokes.difference(untold_jokes)))


if __name__ == "__main__":
	main()
