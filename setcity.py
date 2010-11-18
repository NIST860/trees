import sys, os, re

flags = re.DOTALL | re.MULTILINE
location = re.compile(r'^\s*Site:Location,.*?;.*?\n', flags)
design = re.compile(r'^\s*SizingPeriod:DesignDay,.*?;.*?\n', flags)
temperature = re.compile(r'^\s*Site:GroundTemperature:BuildingSurface,.*?;.*?\n', flags)

def setcity(city):
	file = open(os.path.join('Base', 'city'), 'w')
	file.write(city)
	file.close()
	with open(os.path.join(city, 'baseline.idf')) as baseline:
		data = baseline.read()
		l = '\n'.join(location.findall(data))
		d = '\n'.join(design.findall(data))
		t = '\n'.join(temperature.findall(data))
		if not all((l, d, t)):
			raise Exception(l, d, t)
		for year in range(2, 43):
			path = os.path.join('Base', 'house and tree 0-0 %d year.idf' % year)
			with open(path) as basefile:
				text = basefile.read()
			text = location.sub('\n', text)
			text = design.sub('\n', text)
			text = temperature.sub('\n', text)
			text = '\n'.join((text, l, d, t))
			with open(path, 'w') as basefile:
				basefile.write(text)
			print year


if __name__ == '__main__':
	setcity(sys.argv[1] if len(sys.argv) > 1 else 'Boulder')
