import os, shutil

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

root = os.path.join('E:', 'Tree')

def rename(city):
	base = os.path.join(root, city)
	os.mkdir(base)
	def rename(year):
		dir = os.path.join(base, str(year))
		os.mkdir(dir)
		for (i, (x, y)) in enumerate(points()):
			sourcename = 'year%d-%06d.idf' % (year, i + 1)
			destname = 'house and tree %d-%d %d year.idf' % (x, y, year)
			source = os.path.join(city, str(year), sourcename)
			dest = os.path.join(dir, destname)
			shutil.copyfile(source, dest)
			print sourcename, '>', destname
	map(rename, range(2, 43))

if __name__ == '__main__':
	city = open(os.path.join('Base', 'city')).read().strip()
	rename(city)
