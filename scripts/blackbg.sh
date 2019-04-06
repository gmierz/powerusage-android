#!/bin/bash

# The following "test" is directly from https://bugzilla.mozilla.org/show_bug.cgi?id=1511350#c0:

adb shell am start -n org.mozilla.firefox/.App -a android.intent.action.VIEW -d "'data:text/html;base64,PGJvZHkgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6YmxhY2siPg=='" --ez showstartpane false
