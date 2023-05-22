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
pip install -r requirements.txt
```
Alternatively, download from the main github repo directly (this is considered the development release, which may not be stable).
```
git clone https://github.com/katzerax/Destiny2DPSGraphPY.git
cd Destiny2DPSGraphPY
pip install -r requirements.txt
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
![figure_1](https://media.discordapp.net/attachments/1103555681635799102/1105293082028691529/1683592782.8141556.png)

The weapons creation menu allows you to well, create weapons. As mentioned in the top of the readme, damage calculations assume "best case scenario" for every possible situation. It also is, at its core, a single target sustained damage calculator. This forces us to assume some unrealistic scenarios (that aren't *that* far off from in game). It means buff perks like Frenzy, One for All, and Kill Clip will assume that you are starting your 'DPS Phase' immediately with a full buff timer even if in game you would likely lose a second or so. Perks like Killing Tally will be assumed to have a full stack count *and* a full magazine even if that is not possible in game.

#### Required stats:
- Name
    - Doesn't literally have to be the name of the weapon, but this is what will show up in the graph legend
- Fire Rate
    - In rounds per minute
- Reload Time
    - The literal ammount of time it takes to reload the weapon in seconds
- Damage per Shot
    - Base damage per shot of the weapon. Go shoot Gary!
    - All calculations asume precision hits, so this should be the precision damage value for weapons that can
- Magazine Capacity
    - Base ammo available in one mag
    - DO NOT account for mag augment perks like overflow and clown cartridge, the program will do this automatically
    - DO account for mag perks like enhanced battery and extended mag, the program will not assume these
- Ammo total
    - Total reserve ammo + the current mag
    - Easiest way to get this is to look at the weapons ammo when stowed, as that is the number you are looking for

#### Non-required stats:
- Perks
- Origin Trait
- Enhanced Perks
    - Self explanatory, check these boxes if the corresponding perks are enhanced
    - For enhanced perks that do not augment a relevant stat, these checks will be ignored
- Burst Weapon
    - Enable this for any burst type weapon (ie Pulse Rifles, Aggressive Frame LFRs, etc)
    - Enabling this will create a box to enter how many bullets are fired in each burst
- Fusion Weapon
    - This is a catch all for any weapon that has a wind up before shooting (ie Bows, Fusion Rifles, LFRs)

Once you fill in all relavent information for the weapon you want, click the 'Create Weapon' button. If any required information is left out or invalid, the program will throw you an error. After a weapon is successfully created it is available for selection in the Graph Menu.

#### Edge Cases / Odd Behavior
Currently Aggressive Frame LFRs are to be treated as both 'burst weapons' and 'fusion weapons'. So the damage per shot should be entered as damage per bolt, and the magazine capacity and ammo total should be multiplied by 3. There will be further logic addressing this implemented in the future :D

Obviously kinetic / stasis / strand weapons now have infinite reserves. You can set an arbitrary ammount of ammo in the ammo total field and the calculation will calculate damage for the weapon until the theoretical reserves are empty

For cases such as Touch of Malice where there is a bottomless mag, the same logic as above is applied, except you would also use the same value for magazine size as you used for ammo total, effectively creating a bottomless mag for a given ammount of shots

### Options Menu
![figure_1](https://media.discordapp.net/attachments/1103555681635799102/1105291440139030538/1683592404.3157408.png)

(side note, settings.ini is stored in backend/ and is directly modifiable through there)
#### Graph
- Graph Title
- X Axis Name
- X Axis Upper Limit
    - X Axis on the graph will always represent simulated time elapsed
- Y Axis Name
- Y Axis Upper Limit
    - Y Axis on the graph will always represent total damage dealt

#### Import / Export
- Export As
    - Exporting currently supports: (.json, .pickle, .csv)
- Log Current Weapons
    - Prints out all current weapon settings to log
- Import From File
    - Importing currently supports: (.json, .pickle)
- Auto Save / Load
    - Enabling this will allow you to chose an exported weapon list that will automatically load on open, and save whenever changes are made to your weapon list
    - Selecting a path for Auto Save / Load will automatically import whichever list is selected, so make sure to back up any unsaved changes before doing so
    - Importing a new list while this option is enabled will overwrite your current list, but *not* your backup that is selected for Auto Save / Load

⚠️ **NOTE**: Importing and Exporting from pickle is considered an **experimental feature!** Pickle exports from any version are subject to break in any subsequent release, and as such should only be used if you believe that the benefits are worth it. If your backup is unsupported in future releases, the program will refuse to load it. You can fix this by importing it in the version it was created in, exporting it to JSON, and importing it back into the latest version to recover the list.

Benefits of pickle backups currently include:
- Faster import / export times
- Persisting any cached weapon data through restarts
    - Graph data

#### Interface
- Theme
    - Light or Dark
- Log Mode
    - App, Console, or Both
    - If you choose your log mode to be in app or both, console output will be directed to the Log Menu
- Debug Mode
    - Enabling this will enable the Debug section of the settings menu and a few other developer functions
- Print Dmg Steps
    - Enabling this will print damage information to the console every time a shot is fired during damage calculation
    - This option affects the speed at which calculations are performed because the program will hang while printing to the console. **This is entirely dependant on what terminal you use!** See: [Why is printing so slow?](https://stackoverflow.com/a/3860319/14132711) This is left off by default, but even with this option enabled calculations are still *incredibly fast*. If you would still like to enable this option, **it is recommended you use App only logs** unless you understand how your terminal handles stdout. This is technically considered to be a dubug setting, but it will be left in because it looks cool :D

### Log menu 
![image](https://user-images.githubusercontent.com/65287118/236922026-34ed8448-1dc2-41e6-8b40-ff1c941e9812.png)

If you choose your log mode to be in app, or both, the console output will be located here.

## Credits
- [K](https://github.com/katzerax) (repo owner and initial programmer, code contributor)
- [vcat](https://github.com/vixicat) (initial math and calculation logic, graphic designer, code contributor)
- [snark](https://github.com/rare-snark) (early iteration code contributor)
- [myssto](https://github.com/myssto) (later iteration code contributor)
- [jade](https://twitter.com/iamjade4_) (code logic fix suggestions)

## Acknowledgements
- A few months into our development of this project, [a reddit post appeared on r/DestinyTheGame](https://www.reddit.com/r/DestinyTheGame/comments/11d2f0g/i_created_a_new_dps_testing_tool/) which initially appeared to function similarly to the project we were programming. In some regards it is similar, but several parts of the logic as far as we can tell are very different, and so we produce different graphs. We still recommend  you check it out at https://www.hitthecrit.com/weapons.
- We are also aware of a [PvE damage calculator spreadsheet](https://docs.google.com/spreadsheets/d/1rY_iChu08CVnIMfHliZQwup10-GnmPtEu5FG0DNy8VM) that we think you should additionally check out if you are interested in this sort of statistical analysis: https://docs.google.com/spreadsheets/d/1rY_iChu08CVnIMfHliZQwup10-GnmPtEu5FG0DNy8VM

## To-Do

1. cleaning up comments
2. finishing up GUI and backend
3. create more graphs to use on the readme
4. ~~update the readme~~
    - ongoing but done for now
5. ~~create instructions for how to obtain every stat to use for the program~~
6. QA test the whole program before a public announcement
7. ~~acknowledge https://docs.google.com/spreadsheets/d/1rY_iChu08CVnIMfHliZQwup10-GnmPtEu5FG0DNy8VM/edit#gid=641183241~~
