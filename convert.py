import os

def points():
	steps = range(0, 113, 7)
	first = filter(lambda s: s <= 21, steps)
	middle = filter(lambda s: 21 < s < 91, steps)
	last = filter(lambda s: 91 <= s, steps)

	for column in first:
		for row in steps:
			yield column, row
	for column in middle:
		for row in first:
			yield column, row
		for row in last:
			yield column, row
	for column in last:
		for row in steps:
			yield column, row

def convert(source, dest):
	file, output = open(source), open(dest, 'w')
	lines = iter(file)

	xs = 'Parametric:SetValueForRun,\n    $dx,\n'
	ys = 'Parametric:SetValueForRun,\n    $dy,\n'
	for (x, y) in points():
		xs += '    %d,\n' % x
		ys += '    %d,\n' % y
	xs = xs.rstrip(',\n') + ';\n\n'
	ys = ys.rstrip(',\n') + ';\n\n'
	output.write(xs)
	output.write(ys)

	def update(var, last=False):
		line = next(lines)
		num, rest = line.split(',')
		output.write('    =$%s + %s,%s' % (var, num, rest))

	for line in lines:
		if line.strip() == 'Shading:Building:Detailed,':
			output.write(line)
			# Consume Name and Transmittance
			output.write(next(lines))
			output.write(next(lines))
			# Get the number of verticies
			count = next(lines)
			output.write(count)
			count = int(count.split(',')[0])
			for i in range(count):
				update('dx')
				update('dy')
				output.write(next(lines))
		else:
			output.write(line)

	file.close()
	output.close()

if __name__ == '__main__':
	city = open(os.path.join('Base', 'city')).read().strip()
	for year in range(2, 43):
		os.mkdir(os.path.join(city, str(year)))
		source = os.path.join('Base', 'house and tree 0-0 %d year.idf' % year)
		dest = os.path.join(city, str(year), 'year%d.idf' % year)
		convert(source, dest)
		print year
