# Design Tool for Multi-Modal Robot Communication

This project provides a prototyping tool for designing communicative (expressive) behaviors for social robots. The current version is compatible with the [Pepper Robot](https://www.ald.softbankrobotics.com/en/robots/pepper).

The tool was successfully tested on ***MAC*** and ***Linux***.

## Requirements
[![Python 2.7](https://img.shields.io/badge/Python-2.7.14-yellow.svg)](https://www.python.org/downloads/)
[![NAOqi 2.5](https://img.shields.io/badge/NAOqi-2.5-blue.svg)](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)
[![PyNAOqi 2.5](https://img.shields.io/badge/PyNaoqi-2.5.5.5-green.svg)](http://doc.aldebaran.com/2-5/dev/community_software.html#retrieving-software)
[![qi 1.7.2](https://img.shields.io/badge/qi-1.7.2-orange)](https://pypi.org/project/qi/)
[![PyQt 5.13.x](https://img.shields.io/badge/PyQt-5.x.x-brightgreen.svg)](https://pypi.org/project/PyQt5/5.9.2/)
[![PyYAML 5.x](https://img.shields.io/badge/PyYAML-5.x-blue)](https://github.com/yaml/pyyaml)
[![Spotipy 2.9.x](https://img.shields.io/badge/Spotipy-2.9.0-blue)](https://pypi.org/project/spotipy/)

To use the tool you need to do the following:

  * **A.** Install the requirements as described in [Section I](#i-installation-guide).

  * **B.** Clone the repository (e.g., in the Documents folder)

`$ cd ~/Documents`

`$ git clone https://github.com/ES-TUDelft/robot-interaction-tool.git`

  * **C.** Launch the interface as follows:

`$ cd ~/Documents/robot-interaction-tool`

`$ python main.py`

  * ***Note***: This repository is being updated on a regular basis. Use ***git pull*** to integrate the latest changes.

<div align="center">
  <img src="interaction_manager/ui/ui_view.png" width="500px" />
</div>

---

## Content

**I.** [Installation Guide](#i-installation-guide)

**II.** [Setting up Spotify](#ii-setting-up-spotify)

**III.** [User Manual](#iii-user-manual)

**IV.** [Design Guidelines](#iv-design-guidelines)

**V.** [Quick Start](#v-quick-start)

**VI.** [Citation](#vi-citation)

---

## I. Installation Guide

To use the tool on [Linux](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md#i-linux-installation-guide), [Mac](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md#iii-mac-installation-guide) or [Windows](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md#ii-windows-installation-guide) platforms, refer to the [installation document](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md) found in [docs/INSTALLATION.md](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md)

---

## II. Setting up Spotify

* To [setup Spotify](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md#ii-setting-up-spotify), refer to the [installation document](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/INSTALLATION.md#iv-setting-up-spotify).

* Once you're connected to **Spotify**, you'll be able to see your playlists and tracks.

* To play a song (e.g., using the test button or the mini-player panel in the main interface), you will need an active device (i.e., a Spotify Player) that is running on either your browser or PC/Phone.

* ***NOTE:*** When the player is not able to start a song, it means the device is not active. Just refresh your Spotify Player browser or the desktop app. 

* When playing music, you can set the robot to do some animations as follows:
  
  * Make one (or more) list of animations using the default ones available for the [Pepper robot](http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#pepp-pepper-list-of-animations-available-by-default).
  
  * Add your list of animations to [/interaction_manager/properties/animations.yaml](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/interaction_manager/properties/animations.yaml) (Note that the animations.json file is now deprecated!).
  
  * Create a music action (i.e., using the Action block) and enable the "animation" check box in the edit panel. 

---

## III. User Manual

A [user manual](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/user-manual/MANUAL.md) describing the main features of the UI can be found in [docs/user-manual/MANUAL.md](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/user-manual/MANUAL.md).

---

## IV. Design Guidelines

To help you in designing a successful human-robot interaction, we put together a list of [design guidelines](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/GUIDELINES.md) which can be found in [docs/GUIDELINES.md](https://github.com/ES-TUDelft/robot-interaction-tool/blob/master/docs/GUIDELINES.md).

---

## V. Quick Start

To quickly test the tool, import one of the [examples](https://github.com/ES-TUDelft/robot-interaction-tool/tree/master/examples) and run the simulator or connect to a physical robot and test the interaction.

---

## VI. Citation
Please cite our work when you use this tool in your studies:

 * Elie Saad, Joost Broekens and Mark A. Neerincx (2020): An Iterative Interaction-Design Method for Multi-Modal Robot Communication. In *Proceedings of the IEEE International Conference on Robot and Human Interactive Communication (RO-MAN)*, Italy, Sep. 2020, pp. 1-8, *IN PRESS*.

       @InProceedings{Saad2020,
         author    = {Elie Saad and Joost Broekens and Mark A. Neerincx},
         booktitle = {IEEE International Conference on Robot and Human Interactive Communication (RO-MAN)},
         title     = {An Iterative Interaction-Design Method for Multi-Modal Robot Communication},
         year      = {2020},
         address   = {Italy},
         month     = Sep,
         pages     = {1--8},
         publisher = {InPRESS},
       }
