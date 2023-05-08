# Destiny2DPSGraphPY

This is a GUI python program that will produce a graph showing the Destiny 2 DPS over time for certain types of weapons. It is configurable for several things, but is assuming that you are consistently landing critical hits, reloading as soon as the magazine is empty, and preparing perks for dps phases (Bait n Switch, Overflow, etc.)

The critical hits assumption also includes weapons that don't necessarily 'crit' such as rockets and grenade launchers, as these weapons don't come with perks that require crits.

This is heavily based on the styling of [Prelapse's DPS over time graphs on YouTube](https://www.youtube.com/playlist?list=PLmMhH44rl0aVkIqWzaCr_wrYkk5EFAeIZ). The key difference is that [Prelapse manually enters every data point into a spreadsheet to graph them.](https://media.discordapp.net/attachments/1005973866075664504/1061868926239248416/image.png?width=810&height=117) In this project, this is done automatically with variables. This is fundamentally useful for automating the process, as well as allowing you to measure dps over time graphs on your own for whatever weapon you want. The goal of this project is to be able to simulate weapons within a reasonable degree to bypass needs to manually test and calculate damage.

It is a requirement to know some fundamentals of the weapon that is being tested, which includes: Rate of Fire in RPM, Reload Time in Seconds, Damage per Shot/Hit, Magazine Capacity, and the Total Ammount of Ammo (reserves + magazine).

Other optional variables include: Perks, Enhancing Perks, Buffs, Ammo Type (Primary, Special, etc), Elemental Type (Kinetic, Solar, etc), Burst/Pulse Weapon, and Fusion Type Weapon.

Please see the Install and Usage sections of this readme.

Lastly, feel free to edit the files on your own and contribute to forks. If you can do it better, then by all means do so.

## Install
Install [Python 3.11.0](https://www.python.org/downloads/release/python-3110/). When the option to add to PATH is shown while installing, do so.
Download the [latest release](https://github.com/katzerax/Destiny2DPSGraphPY/releases/latest) in the [releases](https://github.com/katzerax/Destiny2DPSGraphPY/releases) tab (this is considered the stable release)
Unzip the file to a folder, then open a command prompt to the project directory and run:
```
pip install requirements.txt
```
Alternatively, download from the main github repo directly (this is considered the development release, which may not be stable).
```
git clone https://github.com/katzerax/Destiny2DPSGraphPY.git
cd Destiny2DPSGraphPY
pip install requirements.txt
```
6.0 and greater will be packaged into a zip file. Unzip the contents to a directory that works well. There should be several python files including main, perks, backend, etc. There should also be a settings.ini file, and if not it will generate one for you.

## Usage
As of release 6.0, the code has been completely rewritten and overhauled to now utilize a GUI. See the instructions below.
To start the gui, double click main.py OR open a command prompt to the project directory and run:
```
python main.py
```

### Graph Menu 
![Figure_1](https://media.discordapp.net/attachments/1103555681635799102/1105219855285764238/image.png?width=810&height=413)

This is the menu you will be utilizing to create and export graphs. At the top there is a dropdown for the number of weapons to compare, and the number of weapons you select there will indicate how many weapon dropdowns there will be. Select which weapons you have already generated, up to 10, and hit generate graph. It will take a moment to calculate for every weapon, and then display a graph like the one pictured above. You can make weapons in the weapons menu.

### Weapons Creation Menu 
The weapons creation menu allows you to well, create weapons. You will need to find the following stats:
stat + how to find
stat + how to find
stat + how to find
stat + how to find
Check the applicable checkboxes at the bottom, if it is a burst weapon fill in the bullets per burst additionally, and then click create weapon. If all went well, the log should say weapon created with code 0. If there was an error, it will tell you what it thinks the issue is.

### Options Menu
[new image for the options menu AFTER the removal of the test_func button]

Here is where you can configure the program options. The graph elements are configurable, as well as the app theme and how it handles logs. This is also the menu where you would handle importing and exporting. If you export your weapons as a json, it makes for easily shareable files with other people. If you export as pickle, you can enable auto saving and loading by setting the auto save path to the directory of said pickle file. Once you have selected the settings that you wish to apply, press Apply Settings. This will restart the application with the settings you have enabled. If you want to reset settings, there is a Reset Settings button also. 

### Log menu 
![image](https://user-images.githubusercontent.com/65287118/236922026-34ed8448-1dc2-41e6-8b40-ff1c941e9812.png)

If you choose your log mode to be in app, or both, the console output will be located here.

## Credits
- [K](https://github.com/katzerax) (repo owner and initial programmer, code contributor)
- [vcat](https://github.com/vixicat) (initial math and calculation logic, code contributor)
- [snark](https://github.com/rare-snark) (early iteration code contributor)
- [myssto](https://github.com/myssto) (later iteration code contributor)
- [jade](https://twitter.com/iamjade4_) (code logic fix suggestions)

## Acknowledgements
- A few months into our development of this project, [a reddit post appeared on r/DestinyTheGame](https://www.reddit.com/r/DestinyTheGame/comments/11d2f0g/i_created_a_new_dps_testing_tool/) which initially appeared to function similarly to the project we were programming. In some regards it is similar, but several parts of the logic as far as we can tell are very different, and so we produce different graphs. We still recommend  you check it out at https://www.hitthecrit.com/weapons.

## To-Do

1. cleaning up comments
2. finishing up GUI and backend
3. create more graphs to use on the readme
4. update the readme
5. create instructions for how to obtain every stat to use for the program
6. QA test the whole program before a public announcement

## UI Images
### Main Screen
![Figure_1](https://media.discordapp.net/attachments/1099105715051823144/1104598556788142110/image.png)
### Weapons Menu
![Figure_1](https://media.discordapp.net/attachments/1099105715051823144/1104598617572003910/image.png)
### Options
![Figure_1](https://media.discordapp.net/attachments/1099105715051823144/1104598701000884244/image.png)


