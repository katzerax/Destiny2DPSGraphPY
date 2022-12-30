# Destiny2DPSGraphPY

This is a python file that will produce a graph showing the destiny 2 DPS for certain weapons. It is configurable for several things, but is presuming that you are firing until your mag is empty, reloading, and immediately firing until you are out of ammo. This dps assumes the best, that you always hit the target. Co-written with my friend Roxy (https://twitter.com/rokishee), with additional support from snark.

Currently main.py requires a "weapons.json" (or alternative .json with a -rf cli arg) to input data for the graphs. It is highly recommended that you edit the currently existing weapons.json file to use with main.py.

Runs on Python 3.11.0, requires Matplotlib:

pip install matplotlib

#
![Figure_1](https://user-images.githubusercontent.com/65287118/210054539-a0629674-e846-43ed-8e1f-808482d20a66.png)

#
![Figure_1](https://user-images.githubusercontent.com/65287118/209410562-fc720bb0-fd7c-492b-8a41-7422d72d4cf2.png)
