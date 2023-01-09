# Destiny2DPSGraphPY

This is a python file that will produce a graph showing the destiny 2 DPS for certain weapons. It is configurable for several things, but is presuming that you are firing until your mag is empty, reloading, and immediately firing until you are out of ammo. This dps assumes the best, that you always hit the target. Initial logic done with the help of [Roxy](https://twitter.com/rokishee), with additional support from snark.

This is heavily based on the styling of [Prelapse's DPS overgraphs on YouTube](https://www.youtube.com/playlist?list=PLmMhH44rl0aVkIqWzaCr_wrYkk5EFAeIZ). The key difference is that Prelapse manually enters every data point into a spreadsheet to graph them. These are done automatically with variables.

Please see the Install and Usage sections of this readme.

Lastly, feel free to edit main.py and change values like x and y scale, as well as data points. I like to keep data points as a multiple of 10 of x_scale. It would probably work as a non multiple of 10, but I havent tried that so it may not work right. Also, some graphs misfunction without enough data points. 45000 is the amount currently in main.py (per weapon), which made it so everything we have tried thus far works. If something isnt looking right, again, feel free to mess around with these values. Remember that for every weapon, it does that many data points. If your computer is not very powerful then I would either limit the data points or lower the weapon count.

## Install
Install Python 3.11.0, then run:
```
pip install matplotlib
```
Download main.py and optionally weapons.json (which has example weapons) from the [latest release](https://github.com/katzerax/Destiny2DPSGraphPY/releases/latest) in the [releases](https://github.com/katzerax/Destiny2DPSGraphPY/releases) tab (this is considered the stable release), or from the main github repo directly (this is considered the development release).

## Usage
As of release 5.0, there are 2 ways to use this code. I will explain them below.

### Built in user-friendly command line prompts
This method is enabled by default when you double click the python file, and will be the most beginner friendly to use. It will walk you through every step.

### Through CLI With Args
The main command is as follows:
```
python main.py
```

To run the code without the user-friendly dialogue, use the **--dialogue (shortened to -d) [y/n]** arg (This will run the code directly from the "weapons.json" file.)
```
python main.py -d n
```

To run through cli loops but skip the user friendly dialogue, specify with the **--input-mode (shortened to -im) [cli/file]** arg. 
```
python main.py -d n -im cli
```

Additionally you can point the file to another file not labelled "weapons.json" to read from with the **--read-from (shortened to -rf) [filename.json]** arg.
```
python main.py -d n -rf yippee.json
```

## To-Do
1. maybe a whole gui. maybe installing a requirements.txt for matplotlib. dunno
2. Roxy is still working on some logic for some additional variables, apparently. So I intend to add to the code some more to support additional variables in the future. I dont personally know a whole lot about the logic behind the calculations so I dont know what is currently missing, I just put her logic into code.

## Example graphs
![Figure_1](https://user-images.githubusercontent.com/65287118/210054539-a0629674-e846-43ed-8e1f-808482d20a66.png)
![Figure_1](https://user-images.githubusercontent.com/65287118/209410562-fc720bb0-fd7c-492b-8a41-7422d72d4cf2.png)
