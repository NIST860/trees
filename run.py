import os, subprocess

def run(city):
	for year in range(2, 43):
		os.chdir(os.path.join(city, str(year)))
		exe = os.path.join('..', '..', 'parametricpreprocessor.exe')
		file = 'year%d.idf' % year
		print year
		subprocess.call([exe, file])
		os.chdir(os.path.join('..', '..'))

if __name__ == '__main__':
	city = open(os.path.join('Base', 'city')).read().strip()
	run(city)
