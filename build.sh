#!/bin/bash

if [ $# -eq 0 -o "$1" = "pyside" ]; then
	RCC="pyside-rcc"
	UIC="pyside-uic"
	PYMOD="PySide"
elif [ "$1" = "pyqt4" ]; then
	RCC="pyrcc4"
	UIC="pyuic4"
	PYMOD="PyQt4"
else
	echo Invalid build target, leave blank or specify "pyside" or "pyqt4".
	exit 1
fi

# Generate the files
$RCC resources/graphics.qrc -o frontend/guiqt/ui/graphics_rc.py
$UIC frontend/guiqt/ui/mainwindow.ui -o frontend/guiqt/ui/mainwindow.py
$UIC frontend/guiqt/ui/appinfo.ui -o frontend/guiqt/ui/appinfo.py
$UIC frontend/guiqt/ui/validationsimple.ui -o frontend/guiqt/ui/validationsimple.py

# Now change PyQt4/PySide imports to use the qt proxy.
sed -i "s/from $PYMOD import /from qt import /" \
	frontend/guiqt/ui/graphics_rc.py \
	frontend/guiqt/ui/mainwindow.py \
	frontend/guiqt/ui/appinfo.py \
	frontend/guiqt/ui/validationsimple.py

# Remove the "Created" time as it clutters commits. Unfortunately I can't yet
# figure out how to remove the new line as well.
sed -i "s/^# Created: .*//" \
	frontend/guiqt/ui/graphics_rc.py \
	frontend/guiqt/ui/mainwindow.py \
	frontend/guiqt/ui/appinfo.py \
	frontend/guiqt/ui/validationsimple.py
