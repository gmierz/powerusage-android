import datetime
import time

from data_saver import DataSaver
from adb_utils import (
	disable_charging,
	enable_charging,
	get_battery_info,
	parse_battery_info
)
from utils import (
	finish_same_line,
	write_same_line
)

OUTPUT = '/home/sparky/Documents/mozwork/'
RESOLUTION = 4 # time between data points in seconds
SAVERINTERVAL = 5 # seconds
FINALLEVEL = 5


def main():
	print("Running OS baseline test.\n")
	print("Make sure you have no apps running in the background.")
	print("Make sure that there is a wakelock app running.")
	print("Charging is disabled and enabled automatically when we reach 5%.")

	_ = input("Press enter when ready...")
	ds = DataSaver(OUTPUT)
	ds.start()

	print("Disabling charging...")
	disable_charging()
	input("Is it disabled?")
	print("Start time: {}".format(datetime.datetime.utcnow()))

	try:
		level = 1000
		prevcharge = 0
		prevlevel = 0
		prevtemp = 0
		while level != FINALLEVEL:
			start = time.time()

			info = parse_battery_info(get_battery_info())
			info['timestamp'] = time.time()
			ds.add(info, 'batterydata')
			level = int(info['level'])

			if prevcharge != info['Charge counter'] or \
			   prevlevel != level or prevtemp != info['temperature']:
				finish_same_line()
			write_same_line("{} | Current capacity: {}%, {}, Temp: {}".format(
				datetime.datetime.utcnow(), str(level),
				info['Charge counter'], info['temperature']
			))

			prevlevel = level
			prevcharge = info['Charge counter']
			prevtemp = info['temperature']

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
	ds.stop_running()
	print("Done.")


if __name__=="__main__":
	main()