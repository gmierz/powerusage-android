
TESTS = [
    'black-page',
    'white-page',
    'red-page'
    #'idle-foreground',
    #'idle-background'
]

TEST_COMMANDS = {
	'black-page': [
		"adb",
		"shell",
		"am start -n org.mozilla.firefox/.App " \
		"-a android.intent.action.VIEW " \
		"""-d "data:text/html;base64,PGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6YmxhY2siPg==" """ \
		"--ez showstartpane false"
	],
	'white-page': [
		"adb",
		"shell",
		"""am start -n org.mozilla.firefox/.App """ \
		"""-a android.intent.action.VIEW """ \
		"""-d "data:text/html;base64,PGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6d2hpdGUiPg==" """\
		"""--ez showstartpane false"""
	],
	'red-page': [
		"adb",
		"shell",
		"am start -n org.mozilla.firefox/.App " \
		"-a android.intent.action.VIEW " \
		"""-d "data:text/html;base64,PGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6cmVkIj4=" """ \
		"--ez showstartpane false"
	]
}
