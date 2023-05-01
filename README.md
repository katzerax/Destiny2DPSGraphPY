# Destiny2DPSGraphPY

This is a GUI python program that will produce a graph showing the Destiny 2 DPS over time for certain types of weapons. It is configurable for several things, but is assuming that [insert assumptions here].

This is heavily based on the styling of [Prelapse's DPS over time graphs on YouTube](https://www.youtube.com/playlist?list=PLmMhH44rl0aVkIqWzaCr_wrYkk5EFAeIZ). The key difference is that [Prelapse manually enters every data point into a spreadsheet to graph them.](https://media.discordapp.net/attachments/1005973866075664504/1061868926239248416/image.png?width=810&height=117) In this project, this is done automatically with variables. This is fundamentally useful for automating the process, as well as allowing you to measure dps over time graphs on your own for whatever weapon you want.

YOU WILL NEED TO KNOW THE STATS FOR THE WEAPONS YOU ARE GRAPHING. That is, you'll need to know the following: [the following].

Please see the Install and Usage sections of this readme.

Lastly, feel free to edit the files on your own and contribute to forks. If you can do it better, then by all means do so.

## Install
Install [Python 3.11.0](https://www.python.org/downloads/release/python-3110/). When the option to add to PATH is shown while installing, do so. Afterwards, open command prompt and run:
```
pip install matplotlib
```
Download the [latest release](https://github.com/katzerax/Destiny2DPSGraphPY/releases/latest) in the [releases](https://github.com/katzerax/Destiny2DPSGraphPY/releases) tab (this is considered the stable release)
Unzip the file to a folder and you will be set.
Alternatively, download from the main github repo directly (this is considered the development release, which may not be stable).

## Usage
As of release 6.0, the code has been completely rewritten and overhauled to now utilize a GUI. See the instructions below.

### Settings
### Main Menu
### Importing and Exporting
### Blah blah blah

## Credits [feel free to change these and link to whatever links ya'll want for credit]
- [K](https://github.com/katzerax) (repo owner and initial programmer, code contributor)
- [vcat](https://github.com/vixicat) (initial math and calculation logic, code contributor)
- [snark](https://github.com/rare-snark) (early iteration code contributor)
- [myssto](https://github.com/Placni) (later iteration code contributor)
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

## Example graphs
![Figure_1](https://user-images.githubusercontent.com/65287118/210054539-a0629674-e846-43ed-8e1f-808482d20a66.png)
![Figure_1](https://user-images.githubusercontent.com/65287118/209410562-fc720bb0-fd7c-492b-8a41-7422d72d4cf2.png)
