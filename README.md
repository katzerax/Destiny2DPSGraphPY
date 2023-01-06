# Destiny2DPSGraphPY

This is a python file that will produce a graph showing the destiny 2 DPS for certain weapons. It is configurable for several things, but is presuming that you are firing until your mag is empty, reloading, and immediately firing until you are out of ammo. This dps assumes the best, that you always hit the target. Initial logic done with the help of Roxy (https://twitter.com/rokishee), with additional support from snark.

Currently main.py requires a "weapons.json" (or alternative .json with a -rf cli arg) to input data for the graphs. It is highly recommended that you edit the currently existing weapons.json file to use with main.py, alternatively see the Usage section below to see how to loop user inputs through the command line.

Lastly, feel free to edit main.py and change values like x and y scale, as well as data points. I like to keep data points as a multiple of 10 of x_scale. It would probably work as a non multiple of 10, but I havent tried that so it may not work right. Also, some graphs misfunction without enough data points. 45000 is the amount currently in main.py (per weapon), which made it so everything we have tried thus far works. If something isnt looking right, again, feel free to mess around with these values.

# Install
Install Python 3.11.0 and pip, then:

pip install matplotlib

Download main.py and optionally weapons.json (which has example weapons) from the latest release in the releases tab.

# Usage
There is 2 primary ways to use this code. Through command line, or by editing weapons.json and running main.py without arguments.

By default, weapons.json contains a few weapons that will create a graph similar to the one below. Editing the weapons in this file directly should work fine.

I would highly recommend to run through the command prompt if EITHER:
1. You want to run a .json that is named anything other than "weapons.json"
2. You want to manually enter values prompted from the command prompt, instead of editing files.

The command you will need to do should look like the following (in the directory of main.py [cd {directory of main.py}] first):

python main.py [-im cli] [-rf filename.json]

--input-mode (shortened to -im) you can choose between file or cli. if you do cli, it will ask you for the inputs of the weapons until you are done inputting. Default is file, argument not needed if you just want to run from the weapons.json file.

![image](https://user-images.githubusercontent.com/65287118/210480652-d4d5aeb2-826b-472c-b432-b3870225d1ad.png)

--read-file (shortened to -rf) you can choose another file other than weapons.json to run the graph from. If you arent sure what this is then don't worry about it.

# To-Do
1. Auto install matplotlib (and maybe pip)
2. By default ask if the user wants to run the program by looping for weapon inputs or by running a .json file
3. Add functionality if #2 is implemented to run the program through cli with an arg that will allow you to skip the more beginner friendly questions implemented through #2.
4. Make the weapon input question about delay first shot be usable through true or false inputs instead of string or empty string

# Example graphs
![Figure_1](https://user-images.githubusercontent.com/65287118/210054539-a0629674-e846-43ed-8e1f-808482d20a66.png)
![Figure_1](https://user-images.githubusercontent.com/65287118/209410562-fc720bb0-fd7c-492b-8a41-7422d72d4cf2.png)
