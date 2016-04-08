#! /usr/bin/python

from build import CLASS, grow_tree, Node

def parse(line):
	first_space = False
	words = ['']

	if line[-1] == '\n':
		line = line[:-1]

	for char in line:
		if char != ' ':
			words[-1] += char
			first_space = True

		elif first_space:
			words.append('')
			first_space = False

	if words[-1] == '':
		words.pop()

	return words

def calculate_accuracy(records, tree):
	total = len(records)
	misclassified = 0

	for record in records:
		if record[CLASS] != tree.classify(record):
			misclassified += 1

	return (1 - float(misclassified) / total) * 100

def main(files):
	attributes = []
	training = []
	testing = []

	if len(files) == 2:
		attribute_filename, train_filename  = files
		test_filename = None

	else:
		attribute_filename, train_filename, test_filename = files

	try:
		try:
			with open(attribute_filename) as file:
				for line in file:
					words = parse(line)
					attributes.append( (words[0], words[1] == 'continuous', words[1:]) )
		except:
				raise Exception('Cannot read records without knowing their attributes. ' + attribute_filename + ' could not be opened.')

		class_name, continuous, values = attributes.pop()
		attributes.append( (CLASS, continuous, values) )

		for filename, records in [(train_filename, training), (test_filename, testing)]:
			try:
				with open(filename) as file:
					for line in file:
						record = {}

						for attribute, value in zip(attributes, parse(line)):
							name, continuous, values = attribute

							if continuous:
								record[name] = float(value)

							else:
								record[name] = value

						records.append(record)

			except:
				if records is training:
					raise Exception('Cannot build a decision tree without training records. ' + training_filename + ' could not be opened.')

	except Exception, e:
		print(e)

	else:
		attributes.pop()
		tree = grow_tree(training, attributes)

		print(tree)
		print('Accuracy on training set: ' + str( calculate_accuracy(training, tree) )  + '%')
		if testing != []:
			print('Accuracy on testing set: ' + str( calculate_accuracy(testing, tree) )  + '%')

if __name__ == '__main__':
	from sys import argv

	if len(argv) == 2:
		main( [ argv[1] + end for end in ['-attr.txt', '-train.txt', '-test.txt'] ] )

	elif 3 <= len(argv) <= 4:
		main( argv[1:] )

	else:
		print('Usage: ' + argv[0] + ' name')
		print('       ' + argv[0] + ' attribute_file training_file [test_file]\n')
		print('       name: attribute file, training file and an optional test file are, respectively, name-attr.txt, name-train.txt and name-test.txt')