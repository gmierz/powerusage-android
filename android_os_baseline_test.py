import os
import json
import time
import subprocess
from threading import Thread

from adb_utils import (
	disable_charging,
	enable_charging,
	get_battery_info
)

from utils import (
	finish_same_line,
	write_same_line
)

OUTPUT = '/home/sparky/Documents/mozwork/'
RESOLUTION = 4 # time between data points in seconds
SAVERINTERVAL = 5 # seconds
FINALLEVEL = 99


class DataSaver(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.output = os.path.join(OUTPUT, 'osbaseline' + str(int(time.time())))
		os.mkdir(os.path.join(OUTPUT, 'osbaseline' + str(int(time.time()))))
		self.queue = []
		self.stop = False

	def add(self, info, name):
		if not self.stop:
			self.queue.append({'info': info, 'name': name})

	def stop(self):
		self.stop = True
		while self.queue:
			print("{} items left in queue".format(str(len(self.queue))))
			time.sleep(SAVERINTERVAL)

	def run(self):
		while (not self.stop) or self.queue:
			if not self.queue:
				time.sleep(SAVERINTERVAL)
				continue
			el = self.queue.pop(0)
			with open(os.path.join(self.output, el['name'] + str(int(time.time())) + '.json'), 'w+') as f:
				json.dump(el['info'], f)


def parse_battery_info(batinfo):
	'''
	Parses an entry such as:
		Current Battery Service state:
		AC powered: false\n
		USB powered: true\n
		Wireless powered: false\n
		Max charging current: 3000000\n
		Max charging voltage: 5000000\n
		Charge counter: 3991656\n
		status: 2\n
		health: 2\n
		present: true\n
		level: 96\n
		scale: 100\n
		voltage: 4387\n
		temperature: 300\n
		technology: Li-ion\n

	'''
	info = {}
	lines = batinfo.decode("ascii").split('\n')
	for line in lines[1:]: # Ignore the first line
		if line == '':
			continue
		name, val = line.split(':')
		name = name.strip()
		val = val.strip()
		info[name] = val
	return info


def main():
	print("Running OS baseline test.\n")
	print("Make sure you have no apps running in the background.")
	print("Make sure that there is a wakelock app running.")
	print("Charging is disabled and enabled automatically when we reach 5%.")

	_ = input("Press enter when ready...")
	ds = DataSaver()
	ds.start()

	print("Disabling charging...")
	disable_charging()
	input("Is it disabled?")

	try:
		level = 1000
		while level != FINALLEVEL:
			start = time.time()

			info = parse_battery_info(get_battery_info())
			level = int(info['level'])
			ds.add(info, 'batterydata')
			write_same_line("Current capacity: {}%, {}".format(
				str(level), info['Charge counter']
			))

			end = time.time()
			telapsed = end - start

			if telapsed < RESOLUTION:
				time.sleep(RESOLUTION - telapsed)
	except Exception as e:
		enable_charging()
		raise

	finish_same_line()

	print("Enabling charging...")
	enable_charging()

	print("Stopping data saver...")
	ds.stop()
	print("Done.")


if __name__=="__main__":
	main()