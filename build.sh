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
$RCC graphics/graphics.qrc -o ui/graphics_rc.py
$UIC ui/mainwindow.ui -o ui/mainwindow.py
$UIC ui/appinfo.ui -o ui/appinfo.py
$UIC ui/validationsimple.ui -o ui/validationsimple.py

# Now change PyQt4/PySide imports to use the qt proxy.
sed -i "s/from $PYMOD import /from qt import /" \
	ui/graphics_rc.py \
	ui/mainwindow.py \
	ui/appinfo.py \
	ui/validationsimple.py

# Remove the "Created" time as it clutters commits. Unfortunately I can't yet
# figure out how to remove the new line as well.
sed -i "s/^# Created: .*//" \
	ui/graphics_rc.py \
	ui/mainwindow.py \
	ui/appinfo.py \
	ui/validationsimple.py
