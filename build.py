from tree import Node

CLASS = 'class'

def grow_tree(records, attributes, default = ''):
	if stopping_condition(records, attributes):
		label = classify(records)

		if label is None:
			label = default

		return Node(label = label)

	else:
		i, condition = find_best_split(records, attributes)
		default = classify(records)

		attributes[-1], attributes[i] = attributes[i], attributes[-1]
		name, v, values = attributes.pop()

		if v != False:
			root = Node(label = name + '<=' + str(v), test = condition)
			values = [True, False]
		
		else:
			root = Node(label = name, test = condition)

		for value in values:
			new_records = filter(lambda r: condition(r) == value, records)
			child = grow_tree(new_records, attributes, default)
			root.add_branch(value)
			root.add_child(child)

		attributes.append( (name, v, values) )
		attributes[-1], attributes[i] = attributes[i], attributes[-1]

		return root

def attribute_ocurrences(records, attribute_name):
	values = []
	sizes = []

	for record in records:
		try:
			i = values.index( record[attribute_name] )

		except:
			values.append( record[attribute_name] )
			sizes.append(1)

		else:
			sizes[i] += 1

	return values, sizes

def stopping_condition(records, attributes):
	if attributes == []:
		return True

	else:
		for record in records:
			if records[0][CLASS] != record[CLASS]:
				return False

		return True

def classify(records):
	if records == []:
		return None

	classes, sizes = attribute_ocurrences(records, CLASS)
	max = 0

	for i, size in enumerate(sizes):
		if size > sizes[max]:
			max = i

	return classes[max]

def find_best_split(records, attributes):
	def gini_attribute(attribute):
		name, continuous, values = attribute
		add = lambda x, y: x + y

		values, sizes = attribute_ocurrences(records, name)
		total = len(records)
		
		if continuous != False:
			values.sort()
			n = len(values)

			if n == 1:
				return 0, lambda r: r[name] <= values[0], [True, False]

			midpoints = [ float(values[i - 1] + values[i]) / 2 for i in range(1, n) ]
			classes, greater_sizes = attribute_ocurrences(records, CLASS)
			lesser_sizes = map(lambda x: 0, classes)
			copy = records[:]
			v = midpoints[0]
			total_g = total
			total_l = 0
			min = 1

			for midpoint in midpoints:
				lesser_records = filter(lambda r: r[name] <= midpoint, copy)

				for record in lesser_records:
					i = classes.index( record[CLASS] )
					greater_sizes[i] -= 1
					lesser_sizes[i] += 1

					copy.remove(record)
					total_g -= 1
					total_l += 1

				squared_ps_g = map(lambda n: (float(n) / total_g) ** 2, greater_sizes)
				squared_ps_l = map(lambda n: (float(n) / total_l) ** 2, lesser_sizes)
				gini_g = 1 - reduce(add, squared_ps_g)
				gini_l = 1 - reduce(add, squared_ps_l)
				score = (gini_g * total_g + gini_l * total_l) / total

				if score < min:
					v = midpoint
					min = score

			return min, lambda r: r[name] <= v, v

		else:
			score = 0

			for value, size in zip(values, sizes):
				subrecords = filter(lambda r: r[name] == value, records)
				c, ns = attribute_ocurrences(subrecords, CLASS)
				squared_ps = map(lambda n: (float(n) / total) ** 2, ns)
				gini = 1 - reduce(add, squared_ps)
				score += gini * size / total

			return score, lambda r: r[name], None

	results = map(gini_attribute, attributes)
	min = 0

	for i, result in enumerate(results):
		score, f, vs = result
		if score < results[min][0]:
			min = i

	if attributes[min][1] != False:
		name, continuous, values = attributes.pop(min)
		attributes.insert(min, (name, results[min][2], values))

	return min, results[min][1]