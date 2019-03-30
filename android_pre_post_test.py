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
TESTTIME = 20 # minutes


def wait_for_drop():
	dropped = False
	level = parse_battery_info(get_battery_info())['level']
	while not dropped:
		currlevel = parse_battery_info(get_battery_info())['level']
		if level != currlevel:
			dropped = True
			break
		time.sleep(5)


def main():
	print("Running Android Pre/Post test.\n")
	print("Make sure you have no extra apps running in the background.")
	print("Make sure that there is a wakelock app running (if going passed 30 minutes of testing).")
	print("Charging is disabled and enabled automatically when we reach 5%.")

	_ = input("Press enter when ready...")
	ds = DataSaver(OUTPUT)
	ds.start()

	print("Disabling charging...")
	disable_charging()
	input("Is it disabled?")

	input("When the test is ready, start the recording by pressing enter...")

	print("Waiting for a percentage drop...")
	#wait_for_drop()
	print("Drop detected, starting test")
	print("Start time: {}".format(datetime.datetime.utcnow()))

	info = parse_battery_info(get_battery_info())
	info['timestamp'] = time.time()
	starttime = info['timestamp']
	ds.add(info, 'batterydata')

	print("Starting values:")
	for k, v in info.items():
		print("{}: {}".format(k, v))

	currtime = 0
	testtime_seconds = TESTTIME * 60
	while currtime - starttime < testtime_seconds:
		time.sleep(5)
		currtime = time.time()
		write_same_line("Elapsed time (seconds): {}".format(str(currtime-starttime)))
	finish_same_line()

	info = parse_battery_info(get_battery_info())
	info['timestamp'] = time.time()
	ds.add(info, 'batterydata')

	print("End time: {}".format(datetime.datetime.utcnow()))
	print("Final values:")
	for k, v in info.items():
		print("{}: {}".format(k, v))

	print("Enabling charging...")
	enable_charging()

	print("Stopping data saver...")
	ds.stop_running()
	print("Done.")


if __name__=="__main__":
	main()