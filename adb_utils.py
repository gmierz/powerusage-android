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