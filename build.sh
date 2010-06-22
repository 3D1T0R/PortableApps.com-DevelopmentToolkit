#!/bin/sh

pyrcc4 graphics/graphics.qrc -o ui/graphics_rc.py
pyuic4 ui/mainwindow.ui -o ui/mainwindow.py
