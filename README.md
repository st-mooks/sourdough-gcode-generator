# Sourdough gcode generator

## Problem
I wanted to start a sourdough starter during winter. Sourdough starter needs a temp range of about (22-25)C to be active.

## Solution
Several methods to keep the starter warm are available online, but I wanted to attempt to use my 3d printer to keep it warm during the cold winter. I created a python script to customise the temperature, duration, and wakeup intervals, and then compile it into gcode.

## Result
The tool creates gcode that behaves as expected, and more importantly, my sourdough starter is creating delicious loaves 🫓.

## What can be improved
* Position the hotend somewhere relevant (e.g. at sourdough level) and use the thermocouple to read the ambient temp to adjust the hotbed temp to reach desired level.
* Experiment with agitation.
* Play custom tunes at start/end instead of generic beeping.
