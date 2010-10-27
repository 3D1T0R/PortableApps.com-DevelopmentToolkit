#!/bin/sh

pyrcc4 graphics/graphics.qrc -o ui/graphics_rc.py
pyuic4 ui/mainwindow.ui -o ui/mainwindow.py
pyuic4 ui/appinfo.ui -o ui/appinfo.py
pyuic4 ui/validationsimple.ui -o ui/validationsimple.py
