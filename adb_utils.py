import subprocess

def disable_charging():
	subprocess.check_output(
		["adb", "shell", "su -c 'echo 1 > /sys/class/power_supply/battery/input_suspend'"]
	)

def enable_charging():
	subprocess.check_output(
		["adb", "shell", "su -c 'echo 0 > /sys/class/power_supply/battery/input_suspend'"]
	)

def get_battery_info():
	res = subprocess.check_output(['adb', 'shell', 'dumpsys', 'battery'])
	return res

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

